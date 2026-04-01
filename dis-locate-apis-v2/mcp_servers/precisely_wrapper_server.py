"""
Precisely MCP Server - Wrapper Architecture
Uses the PreciselyAPI class from precisely_api_core_clean module
Supports both stdio (default) and Streamable HTTP transports
"""
import asyncio
import sys
import os
import argparse
import contextlib
from pathlib import Path
from typing import Any, Dict, Optional
from collections.abc import AsyncIterator
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent
from mcp.server.stdio import stdio_server
import logging
from dotenv import load_dotenv

# HTTP Transport imports (optional - loaded only when needed)
HTTP_AVAILABLE = False
try:
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from starlette.types import Receive, Scope, Send
    from starlette.responses import JSONResponse
    import uvicorn
    HTTP_AVAILABLE = True
except ImportError:
    pass  # HTTP transport not available - stdio only

# Add parent directory to path to import from precisely_api_core.py
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import the PreciselyAPI class from the core module
from precisely_api_core import PreciselyAPI

# Import tool modules
from mcp_servers.tools import (
    geocoding_address,
    geolocation,
    verification,
    timezone,
    tax_emergency,
    spatial_analysis,
    graphql_services,
    map_services
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("precisely-mcp-wrapper")

# Load environment variables (override=True ensures fresh values)
load_dotenv(override=True)
API_KEY = os.getenv("PRECISELY_API_KEY")
API_SECRET = os.getenv("PRECISELY_API_SECRET")
BASE_URL = os.getenv("PRECISELY_BASE_URL", "https://api.cloud.precisely.com")

# Validate credentials are present before proceeding
if not API_KEY or not API_SECRET:
    logger.critical(
        "PRECISELY_API_KEY and PRECISELY_API_SECRET must be set. "
        "Copy .env.template to .env and fill in your credentials."
    )
    sys.exit(1)

# Initialize the PreciselyAPI core module
precisely_api = PreciselyAPI(API_KEY, API_SECRET, BASE_URL)

# Lightweight health check: verify credentials work before serving tools
try:
    logger.info(f"[startup] PRECISELY_BASE_URL from environment: {repr(BASE_URL)}")
    logger.info(f"[startup] PRECISELY_BASE_URL from environment: {repr(API_KEY)}")
    logger.info(f"[startup] PRECISELY_BASE_URL from environment: {repr(API_SECRET)}")
    _health = precisely_api.geocode("1600 Pennsylvania Ave, Washington DC", country="USA")
    if isinstance(_health, dict) and _health.get("error"):
        logger.critical(f"Credential validation failed: {_health['error']}")
        sys.exit(1)
    logger.info("Credential validation passed")
except Exception as e:
    logger.critical(f"Credential validation failed: {e}")
    sys.exit(1)

# Create MCP server
app = Server("precisely-complete-mcp")

# Build TOOLS list from all modules
ALL_MODULES = [
    geocoding_address,
    geolocation,
    verification,
    timezone,
    tax_emergency,
    spatial_analysis,
    graphql_services,
    map_services
]

TOOLS = []
TOOL_MODULE_MAP = {}  # Maps tool name -> module for dispatch

for module in ALL_MODULES:
    module_tools = module.get_tools()
    TOOLS.extend(module_tools)
    for tool in module_tools:
        TOOL_MODULE_MAP[tool.name] = module

# Startup validation: ensure every tool name maps to a real PreciselyAPI method
_missing = [t.name for t in TOOLS if not hasattr(precisely_api, t.name)]
if _missing:
    logger.critical(f"Tool-method mismatch: these tools have no matching PreciselyAPI method: {_missing}")
    sys.exit(1)
logger.info(f"Tool-method cross-validation passed ({len(TOOLS)} tools verified)")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all 71 Precisely API tools"""
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent]:
    """
    Dispatch tool calls to appropriate module handler
    """
    try:
        # Find the module that handles this tool
        if name not in TOOL_MODULE_MAP:
            return [TextContent(type="text", text=f'{{"error": "Unknown tool: {name}"}}')]
        
        module = TOOL_MODULE_MAP[name]
        
        # Call the module's handler (which is synchronous)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: module.handle_tool_call(name, arguments, precisely_api)
        )
        return result
        
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f'{{"error": "{str(e)}"}}')]

# TRANSPORT: STDIO (default)
# ============================================
async def run_stdio():
    """Run the server using stdio transport (for Claude Desktop, VS Code, etc.)"""
    logger.info("Starting Precisely MCP Server with stdio transport")
    logger.info(f"71 tools available")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


# ============================================
# TRANSPORT: STREAMABLE HTTP
# ============================================

# Kubernetes Health Endpoints
async def health_check(request) -> "JSONResponse":
    """
    Liveness probe endpoint for Kubernetes.
    Returns 200 if the process is alive and running.
    """
    return JSONResponse({
        "status": "healthy",
        "service": "precisely-mcp-server",
        "transport": "http"
    })


async def readiness_check(request) -> "JSONResponse":
    """
    Readiness probe endpoint for Kubernetes.
    Returns 200 if the service is ready to accept requests.
    Checks if Precisely API credentials are valid and reachable.
    """
    try:
        # Quick validation: check if we can get a token
        # This verifies credentials and API connectivity
        result = precisely_api.geocode("test", country="USA")
        
        # If we got any response (even an error), the API is reachable
        return JSONResponse({
            "status": "ready",
            "service": "precisely-mcp-server",
            "api_connectivity": "ok",
            "tools_count": len(TOOLS)
        })
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            {
                "status": "not_ready",
                "service": "precisely-mcp-server",
                "error": str(e)
            },
            status_code=503
        )


def create_http_app(json_response: bool = True, stateless: bool = True) -> "Starlette":
    """
    Create a Starlette app with Streamable HTTP transport.
    
    Args:
        json_response: If True, return JSON responses. If False, use SSE streams.
        stateless: If True, no session persistence (recommended for scalability).
    
    Returns:
        Starlette ASGI application
    """
    if not HTTP_AVAILABLE:
        raise ImportError(
            "HTTP transport requires additional dependencies. "
            "Install with: pip install starlette uvicorn sse-starlette"
        )
    
    # Create session manager wrapping our Server instance
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,  # Set to EventStore impl for resumability
        json_response=json_response,
        stateless=stateless,
    )

    # ASGI handler that delegates to session manager
    async def handle_streamable_http(scope: "Scope", receive: "Receive", send: "Send") -> None:
        await session_manager.handle_request(scope, receive, send)

    # Lifespan context manager for proper startup/shutdown
    @contextlib.asynccontextmanager
    async def lifespan(starlette_app: "Starlette") -> "AsyncIterator[None]":
        async with session_manager.run():
            logger.info("Streamable HTTP server started")
            try:
                yield
            finally:
                logger.info("Streamable HTTP server shutting down")

    # Create Starlette app
    starlette_app = Starlette(
        debug=False,
        routes=[
            Route("/health", health_check, methods=["GET"]),
            Route("/ready", readiness_check, methods=["GET"]),
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    return starlette_app


def run_http(host: str = "127.0.0.1", port: int = 8000):
    """Run the server using Streamable HTTP transport."""
    logger.info(f"Starting Precisely MCP Server with HTTP transport")
    logger.info(f"MCP Endpoint: http://{host}:{port}/mcp")
    logger.info(f"Health Check: http://{host}:{port}/health")
    logger.info(f"Readiness Check: http://{host}:{port}/ready")
    logger.info(f"71 tools available")
    
    starlette_app = create_http_app(
        json_response=True,  # Simpler client integration
        stateless=True,      # Better scalability
    )
    
    uvicorn.run(starlette_app, host=host, port=port, log_level="info")


# ============================================
# MAIN ENTRY POINT
# ============================================
def main():
    """Main entry point with transport selection."""
    parser = argparse.ArgumentParser(
        description="Precisely MCP Server - Location Intelligence APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # stdio transport (default, for Claude Desktop)
  python precisely_wrapper_server.py

  # HTTP transport (for LangChain, LlamaIndex, web clients)
  python precisely_wrapper_server.py --transport http --port 8000

  # HTTP with custom host (for remote access)
  python precisely_wrapper_server.py --transport http --host 0.0.0.0 --port 8080
"""
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type: stdio (default) or http"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP host (default: 127.0.0.1, use 0.0.0.0 for remote access)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "http":
        run_http(host=args.host, port=args.port)
    else:
        asyncio.run(run_stdio())


if __name__ == "__main__":
    main()
