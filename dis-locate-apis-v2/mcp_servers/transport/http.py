"""Streamable HTTP transport: Starlette app, BearerTokenMiddleware, health endpoints."""

import contextlib
import logging
from collections.abc import AsyncIterator

from mcp.server import Server

from mcp_servers.context import _request_bearer_token

logger = logging.getLogger(__name__)

HTTP_AVAILABLE = False
try:
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Mount, Route
    from starlette.types import Receive, Scope, Send
    import uvicorn

    HTTP_AVAILABLE = True
except ImportError:
    pass


class HealthCheckFilter(logging.Filter):
    """Suppress noisy /health and /ready lines from uvicorn access log."""

    def filter(self, record: logging.LogRecord) -> bool:
        return not any(ep in record.getMessage() for ep in ["/health", "/ready"])


logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


class BearerTokenMiddleware:
    """ASGI middleware: extracts 'Authorization: Bearer <token>' from incoming
    HTTP requests and stores it in _request_bearer_token so call_tool can
    forward it to downstream Precisely API calls."""

    def __init__(self, app):
        self._app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = {k.lower(): v for k, v in scope.get("headers", [])}
            auth = headers.get(b"authorization", b"").decode("utf-8", errors="replace")
            if auth.lower().startswith("bearer "):
                scope["_bearer_token"] = auth[len("bearer "):].strip()
        await self._app(scope, receive, send)


def create_http_app(app: Server, precisely_api, tools: list) -> "BearerTokenMiddleware":
    """Build the Starlette ASGI application wrapped with BearerTokenMiddleware."""
    if not HTTP_AVAILABLE:
        raise ImportError(
            "HTTP transport requires additional dependencies. "
            "Install with: pip install starlette uvicorn sse-starlette"
        )

    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_streamable_http(scope: "Scope", receive: "Receive", send: "Send") -> None:
        bearer = scope.get("_bearer_token")
        if bearer:
            ctx_token = _request_bearer_token.set(bearer)
            try:
                await session_manager.handle_request(scope, receive, send)
            finally:
                _request_bearer_token.reset(ctx_token)
        else:
            await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(starlette_app: "Starlette") -> "AsyncIterator[None]":
        async with session_manager.run():
            logger.info("Streamable HTTP server started")
            try:
                yield
            finally:
                logger.info("Streamable HTTP server shutting down")

    async def health_check(request) -> "JSONResponse":
        """Liveness probe — returns 200 if the process is alive."""
        return JSONResponse({"status": "healthy", "service": "precisely-mcp-server", "transport": "http"})

    async def readiness_check(request) -> "JSONResponse":
        """Readiness probe — returns 200 if credentials and API are reachable."""
        try:
            precisely_api.geocode("test", country="USA")
            return JSONResponse({
                "status": "ready",
                "service": "precisely-mcp-server",
                "api_connectivity": "ok",
                "tools_count": len(tools),
            })
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return JSONResponse(
                {"status": "not_ready", "service": "precisely-mcp-server", "error": str(e)},
                status_code=503,
            )

    starlette_app = Starlette(
        debug=False,
        routes=[
            Route("/health", health_check, methods=["GET"]),
            Route("/ready", readiness_check, methods=["GET"]),
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    return BearerTokenMiddleware(starlette_app)


def run_http(app: Server, precisely_api, tools: list, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Start uvicorn serving the HTTP transport."""
    logger.info("Starting Precisely MCP Server with HTTP transport")
    logger.info(f"MCP Endpoint:     http://{host}:{port}/mcp")
    logger.info(f"Health Check:     http://{host}:{port}/health")
    logger.info(f"Readiness Check:  http://{host}:{port}/ready")
    logger.info(f"{len(tools)} tools available")

    asgi_app = create_http_app(app, precisely_api, tools)
    uvicorn.run(asgi_app, host=host, port=port, log_level="info")
