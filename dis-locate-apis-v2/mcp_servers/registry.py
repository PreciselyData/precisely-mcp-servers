"""Build the TOOLS list and TOOL_MODULE_MAP from all tool modules."""

import logging
import sys

from mcp_servers.tools import (
    geocoding_address,
    geolocation,
    graphql_services,
    map_services,
    spatial_analysis,
    tax_emergency,
    timezone,
    verification,
)
from mcp_servers.tools.output_schemas import TOOL_OUTPUT_SCHEMAS

logger = logging.getLogger(__name__)

_ALL_MODULES = [
    geocoding_address,
    geolocation,
    verification,
    timezone,
    tax_emergency,
    spatial_analysis,
    graphql_services,
    map_services,
]


def build_registry(precisely_api) -> tuple:
    """Collect tools from all modules and validate each maps to a PreciselyAPI method.

    Returns:
        (tools, tool_module_map) where tool_module_map is {tool_name: module}.
    Exits with code 1 if any tool name has no matching method on PreciselyAPI.
    """
    tools = []
    tool_module_map = {}

    for module in _ALL_MODULES:
        module_tools = module.get_tools()
        tools.extend(module_tools)
        for tool in module_tools:
            tool_module_map[tool.name] = module

    # Annotate tools with outputSchema from the central mapping
    annotated = 0
    for tool in tools:
        schema = TOOL_OUTPUT_SCHEMAS.get(tool.name)
        if schema:
            tool.outputSchema = schema
            annotated += 1

    missing = [t.name for t in tools if not hasattr(precisely_api, t.name)]
    if missing:
        logger.critical(
            f"Tool-method mismatch: these tools have no matching PreciselyAPI method: {missing}"
        )
        sys.exit(1)

    logger.info(f"Tool-method cross-validation passed ({len(tools)} tools verified, {annotated} with outputSchema)")
    return tools, tool_module_map
