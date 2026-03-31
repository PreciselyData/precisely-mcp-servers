"""
Base Tool Module
Provides common imports, logging setup, and the shared handle_tool_call function
used by all tool modules.
"""
from typing import List, Dict, Any
from mcp.types import Tool, TextContent, ImageContent
import json
import logging


def get_logger(name: str) -> logging.Logger:
    """Returns a logger for the given module name"""
    return logging.getLogger(name)


def handle_tool_call(name: str, arguments: Dict[str, Any], precisely_api: Any) -> List[TextContent | ImageContent]:
    """
    Handle tool execution by dispatching to the matching PreciselyAPI method.

    Args:
        name: Tool name
        arguments: Tool arguments
        precisely_api: PreciselyAPI instance

    Returns:
        List of TextContent or ImageContent
    """
    logger = logging.getLogger(__name__)
    try:
        if not hasattr(precisely_api, name):
            return [TextContent(type="text", text=f'{{"error": "Unknown tool: {name}"}}')]

        method = getattr(precisely_api, name)
        result = method(**arguments)

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f'{{"error": "{str(e)}"}}')]
