"""stdio transport runner."""

import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server

logger = logging.getLogger(__name__)


async def _run(app: Server) -> None:
    logger.info("Starting Precisely MCP Server with stdio transport")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def run_stdio(app: Server) -> None:
    """Block until the stdio server exits."""
    asyncio.run(_run(app))
