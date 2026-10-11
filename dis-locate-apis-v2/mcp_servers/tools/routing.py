"""Routing Tools Module
Contains 3 routing tools for matrix, directions, and reachable area.
"""

from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of routing tool definitions."""
    return [
        Tool(
            name="calculate_travel_time_and_distance",
            description="""Compute ETA and distance matrix for multiple origins and destinations using the Routing API POST endpoint.
Uses POST /v1/matrix/location with option=flexible.

Use this tool when you need travel times/distances for origin-destination pairs at scale.
Output: JSON matrix response including status, rows, durations, and distances.

Sample request:
{
    "option": "flexible",
    "request_body": {
        "origins": [{"lat": 41.349302, "lon": 2.136480}],
        "destinations": [{"lat": 41.389925, "lon": 2.136258}],
        "mode": "car",
        "route_type": "fastest"
    }
}""",
            inputSchema={
                "type": "object",
                "properties": {
                    "option": {
                        "type": "string",
                        "description": "Routing behavior option. Use 'flexible'.",
                        "default": "flexible",
                        "enum": ["flexible"],
                    },
                    "x_request_id": {
                        "type": "string",
                        "description": "Optional request correlation ID passed as X-Request-Id header.",
                    },
                    "request_body": {
                        "type": "object",
                        "description": "POST body for /v1/matrix/location. Supports coordinate-based or address-based origin/destination sets and advanced routing constraints.",
                        "properties": {
                            "origins": {
                                "type": "array",
                                "description": "Origin points. Common format: [{\"lat\": 41.34, \"lon\": 2.13}] or provider-supported alternatives.",
                                "items": {"type": "object"},
                            },
                            "destinations": {
                                "type": "array",
                                "description": "Destination points. Common format: [{\"lat\": 41.38, \"lon\": 2.13}] or provider-supported alternatives.",
                                "items": {"type": "object"},
                            },
                            "mode": {
                                "type": "string",
                                "description": "Travel mode.",
                                "enum": ["car", "truck"],
                            },
                            "route_type": {
                                "type": "string",
                                "description": "Route optimization preference.",
                                "enum": ["fastest", "shortest"],
                            },
                            "departure_time": {
                                "type": "integer",
                                "description": "Departure time as UNIX epoch seconds.",
                            },
                            "local_departure_time": {
                                "type": "string",
                                "description": "Local departure time format like 'Monday 08:00'.",
                            },
                            "avoid": {
                                "type": "string",
                                "description": "Flexible avoid filters, comma-separated (for example: ferry,toll).",
                            },
                            "exclude": {
                                "type": "string",
                                "description": "Strict exclusion filters, comma-separated.",
                            },
                            "truck_size": {
                                "type": "string",
                                "description": "Truck dimensions in cm: height,width,length.",
                            },
                            "truck_weight": {
                                "type": "integer",
                                "description": "Truck weight in kilograms.",
                            },
                            "cross_border": {
                                "type": "boolean",
                                "description": "Allow crossing international borders when needed.",
                            },
                            "hazmat_type": {
                                "type": "string",
                                "description": "Hazmat type(s), comma-separated when multiple are provided.",
                            },
                            "coordOrder": {
                                "type": "string",
                                "description": "Coordinate order in requests when relevant.",
                                "enum": ["LatLon", "LonLat"],
                            },
                        },
                    },
                },
                "required": ["request_body"],
            },
        ),
        Tool(
            name="calculate_route_directions",
            description="""Compute route directions between origin and destination (with optional waypoints) using the Routing API POST endpoint.
Uses POST /v1/direction/location with option=flexible.

Use this tool when you need detailed route geometry, legs, steps, ETA, and distance.
Input supports either coordinates (origin/destination) or address fields (originAddress/destinationAddress with country).
Output: JSON route response including routes, distance, duration, geometry, and legs.

Sample request (coordinates):
{
    "option": "flexible",
    "request_body": {
        "origin": {"lat": 48.87862672840649, "lon": 2.2724349629292195},
        "destination": {"lat": 48.73000636636801, "lon": 2.3044168556664175},
        "mode": "car",
        "geometry": "geojson",
        "route_type": "fastest"
    }
}

Sample request (address):
{
    "option": "flexible",
    "request_body": {
        "originAddress": "POINT REYES STATION CA",
        "originCountry": "USA",
        "destinationAddress": "Lagunitas CA",
        "destinationCountry": "USA",
        "mode": "car",
        "geometry": "geojson",
        "route_type": "fastest"
    }
}""",
            inputSchema={
                "type": "object",
                "properties": {
                    "option": {
                        "type": "string",
                        "description": "Routing behavior option. Use 'flexible'.",
                        "default": "flexible",
                        "enum": ["flexible"],
                    },
                    "x_request_id": {
                        "type": "string",
                        "description": "Optional request correlation ID passed as X-Request-Id header.",
                    },
                    "request_body": {
                        "type": "object",
                        "description": "POST body for /v1/direction/location. Supports either coordinates (origin, destination, waypoints) or address fields (originAddress, originCountry, destinationAddress, destinationCountry), plus mode/constraints.",
                        "properties": {
                            "origin": {
                                "type": "object",
                                "description": "Origin coordinate object, commonly {\"lat\": <number>, \"lon\": <number>}.",
                            },
                            "destination": {
                                "type": "object",
                                "description": "Destination coordinate object, commonly {\"lat\": <number>, \"lon\": <number>}.",
                            },
                            "waypoints": {
                                "type": "array",
                                "description": "Optional ordered waypoint coordinate objects.",
                                "items": {"type": "object"},
                            },
                            "originAddress": {
                                "type": "string",
                                "description": "Origin address when using address-based routing.",
                            },
                            "originCountry": {
                                "type": "string",
                                "description": "Origin country for address-based input.",
                            },
                            "destinationAddress": {
                                "type": "string",
                                "description": "Destination address when using address-based routing.",
                            },
                            "destinationCountry": {
                                "type": "string",
                                "description": "Destination country for address-based input.",
                            },
                            "mode": {
                                "type": "string",
                                "description": "Travel mode.",
                                "enum": ["car", "truck"],
                            },
                            "geometry": {
                                "type": "string",
                                "description": "Geometry format in response.",
                                "enum": ["polyline", "polyline6", "geojson"],
                            },
                            "route_type": {
                                "type": "string",
                                "description": "Route optimization preference.",
                                "enum": ["fastest", "shortest"],
                            },
                            "alternatives": {
                                "type": "boolean",
                                "description": "Return alternate routes when available.",
                            },
                            "altcount": {
                                "type": "integer",
                                "description": "Number of alternate routes to attempt returning.",
                            },
                            "departure_time": {
                                "type": "integer",
                                "description": "Departure time as UNIX epoch seconds.",
                            },
                            "local_departure_time": {
                                "type": "string",
                                "description": "Local departure time format like 'Monday 08:00'.",
                            },
                            "avoid": {
                                "type": "string",
                                "description": "Flexible avoid filters, comma-separated.",
                            },
                            "exclude": {
                                "type": "string",
                                "description": "Strict exclusion filters, comma-separated.",
                            },
                            "road_info": {
                                "type": "string",
                                "description": "Additional road info output options (for example: max_speed, toll_distance, toll_cost).",
                            },
                            "cross_border": {
                                "type": "boolean",
                                "description": "Allow crossing international borders when needed.",
                            },
                            "truck_size": {
                                "type": "string",
                                "description": "Truck dimensions in cm: height,width,length.",
                            },
                            "truck_weight": {
                                "type": "integer",
                                "description": "Truck weight in kilograms.",
                            },
                            "hazmat_type": {
                                "type": "string",
                                "description": "Hazmat type(s), comma-separated when multiple are provided.",
                            },
                            "coordOrder": {
                                "type": "string",
                                "description": "Coordinate order in requests when relevant.",
                                "enum": ["LatLon", "LonLat"],
                            },
                        },
                    },
                },
                "required": ["request_body"],
            },
        ),
        Tool(
            name="calculate_reachable_area",
            description="""Calculate reachable travel area boundaries using the Routing API location endpoint.
Uses GET /v1/isochrone/location.

Use this tool when you need to find area boundaries reachable within time or distance from one starting point.
Input supports either coordinates or an address with country.
Output: JSON reachable-area response with features and status.

Sample request (coordinates):
{
    "coordinates": "38.62283557773102,-90.22415391657728",
    "contours_minutes": "5,10",
    "mode": "car",
    "polygons": true
}

Sample request (address):
{
    "address": "POINT REYES STATION CA",
    "country": "USA",
    "contours_minutes": "5,10",
    "mode": "car",
    "polygons": true
}""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x_request_id": {
                        "type": "string",
                        "description": "Optional request correlation ID passed as X-Request-Id header.",
                    },
                    "coordinates": {
                        "type": "string",
                        "description": "Start coordinate pair as 'lat,lon'. Use this or address.",
                    },
                    "address": {
                        "type": "string",
                        "description": "Start address. Use this or coordinates.",
                    },
                    "country": {
                        "type": "string",
                        "description": "Country used with address-based input.",
                    },
                    "contours_minutes": {
                        "type": "string",
                        "description": "Comma-separated minute contours in increasing order (for example: '5,10').",
                    },
                    "contours_meters": {
                        "type": "string",
                        "description": "Comma-separated distance contours in increasing order.",
                    },
                    "mode": {
                        "type": "string",
                        "description": "Travel mode.",
                        "enum": ["car", "truck"],
                    },
                    "polygons": {
                        "type": "boolean",
                        "description": "When true, returns polygon boundaries; otherwise line strings.",
                    },
                    "contours_colors": {
                        "type": "string",
                        "description": "Optional comma-separated color values for multiple contours.",
                    },
                    "denoise": {
                        "type": "number",
                        "description": "Remove smaller contours, from 0.0 to 1.0.",
                    },
                    "generalize": {
                        "type": "number",
                        "description": "Douglas-Peucker generalization tolerance in meters.",
                    },
                    "departure_time": {
                        "type": "integer",
                        "description": "Departure time as UNIX epoch seconds.",
                    },
                    "local_departure_time": {
                        "type": "string",
                        "description": "Local departure time format like 'Monday 08:00'.",
                    },
                    "coordOrder": {
                        "type": "string",
                        "description": "Coordinate order in requests when relevant.",
                        "enum": ["LatLon", "LonLat"],
                    },
                },
                "required": [],
            },
        ),
    ]
