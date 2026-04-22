"""MCP Server: registers list_tools and call_tool handlers."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.types import CallToolResult, ImageContent, TextContent, Tool

from mcp_servers.context import _request_bearer_token

logger = logging.getLogger(__name__)


def create_server(precisely_api, tools: list, tool_module_map: dict) -> Server:
    """Create and configure the MCP Server with all tool handlers.

    Args:
        precisely_api: Authenticated PreciselyAPI instance (ApiKey auth).
        tools: Full list of Tool objects from registry.
        tool_module_map: Mapping of tool name -> module with handle_tool_call.

    Returns:
        Configured mcp.server.Server instance.
    """
    app = Server("precisely-complete-mcp")

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        """List all 68 Precisely API tools."""
        return tools

    @app.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent]:
        """Dispatch tool calls to the appropriate module handler."""
        try:
            if name not in tool_module_map:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True,
                )

            module = tool_module_map[name]

            # If caller supplied a Bearer token (HTTP transport), use it
            # instead of the default ApiKey credentials.
            bearer_token = _request_bearer_token.get()
            api = precisely_api.with_bearer_token(bearer_token) if bearer_token else precisely_api

            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                lambda: module.handle_tool_call(name, arguments, api),
            )
            return result

        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}", exc_info=True)
            return CallToolResult(
                content=[TextContent(type="text", text=str(e))],
                isError=True,
            )

    return app
