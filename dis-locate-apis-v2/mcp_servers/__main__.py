"""CLI entry point: parse args, wire components, start transport.

Run as:
    python -m mcp_servers                          # stdio (default)
    python -m mcp_servers --transport http         # HTTP
    python -m mcp_servers --transport http --host 0.0.0.0 --port 8080
"""

import argparse
import logging
import sys
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Ensure the repo root (dis-locate-apis-v2/) is on sys.path so that
# `precisely_api_core` and `precisely` are importable.
sys.path.insert(0, str(Path(__file__).parent.parent))

from precisely_api_core import PreciselyAPI
from mcp_servers.config import load_config
from mcp_servers.registry import build_registry
from mcp_servers.server import create_server

# Configure logging once at application startup (not at library import time).
_log_dir = Path(__file__).parent.parent / "logs"
_log_dir.mkdir(exist_ok=True)
_log_file = _log_dir / f"app_{str(uuid.uuid4())[:8]}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(_log_file, maxBytes=10 * 1024 * 1024, backupCount=5),
    ],
)
logger = logging.getLogger("precisely-mcp")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Precisely MCP Server - Location Intelligence APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m mcp_servers                              # stdio (Claude Desktop)
  python -m mcp_servers --transport http             # HTTP on 127.0.0.1:8000
  python -m mcp_servers --transport http --host 0.0.0.0 --port 8080
""",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type: stdio (default) or http",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP host (default: 127.0.0.1, use 0.0.0.0 for remote access)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port (default: 8000)",
    )

    args = parser.parse_args()

    config = load_config()
    precisely_api = PreciselyAPI(config["api_key"], config["api_secret"], config["base_url"])
    tools, tool_module_map = build_registry(precisely_api)
    app = create_server(precisely_api, tools, tool_module_map)

    if args.transport == "http":
        from mcp_servers.transport.http import run_http
        run_http(app, precisely_api, tools, host=args.host, port=args.port)
    else:
        from mcp_servers.transport.stdio import run_stdio
        run_stdio(app)


if __name__ == "__main__":
    main()
