"""
GraphQL Services Tools Module
Contains 22 tools for property, demographics, risk, and advanced GraphQL queries
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of GraphQL services tool definitions"""
    tools = []
    # Property & Risk tools (9 tools)
    for name in ["get_property_data", "get_property_attributes_by_address", "get_replacement_cost_by_address",
                 "get_flood_risk_by_address", "get_wildfire_risk_by_address", "get_property_fire_risk",
                 "get_earth_risk", "get_coastal_risk", "get_historical_weather_risk"]:
        tools.append(Tool(name=name, description=f"{name.replace('_', ' ').title()}", 
                         inputSchema={"type": "object", "properties": {"address": {"type": "string"}, "country": {"type": "string", "default": "US"}}, "required": ["address"]}))
    
    # Demographics & Neighborhoods tools (8 tools)
    for name in ["get_demographics", "get_crime_index", "get_psyte_geodemographics_by_address",
                 "get_ground_view_by_address", "get_neighborhoods_by_address", "get_schools_by_address",
                 "get_buildings_by_address", "get_parcels_by_address"]:
        tools.append(Tool(name=name, description=f"{name.replace('_', ' ').title()}",
                         inputSchema={"type": "object", "properties": {"address": {"type": "string"}, "country": {"type": "string", "default": "US"}}, "required": ["address"]}))
    
    # Advanced GraphQL tools  (5 tools)
    for name in ["get_addresses_detailed", "get_parcel_by_owner_detailed", "get_address_family",
                 "get_serviceability", "get_places_by_address"]:
        tools.append(Tool(name=name, description=f"{name.replace('_', ' ').title()} using GraphQL",
                         inputSchema={"type": "object", "properties": {"data": {"type": "object"}}, "required": ["data"]}))
    
    return tools

