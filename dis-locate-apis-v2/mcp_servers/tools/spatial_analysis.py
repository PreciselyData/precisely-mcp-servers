"""
Spatial Analysis Tools Module
Contains 7 tools for spatial queries, analysis, and metadata discovery
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of spatial analysis tool definitions"""
    return [
        Tool(
        name="find_nearest_candidates",
        description="""Returns nearest locations or points of interest within specified distance from input geometry/address, by default ordered closest first. Input can also be an address, no need to geocode it. Use list_spatial_tables tool to find available spatial tables/data, get_table_metadata tool for available columns and their metadata, and get_spatial_products tool to discover recommended summary attributes, label columns, and data vintage, layer extents, and other metadata.

Returns: GeoJSON FeatureCollection with features. Includes distance values, recordsMatched, recordsReturned, and metadata.

Example 1 Request (Geometry):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'attributes': ['incremental_s_no', 'state', 'wr_id'], 'location': {'format': 'wkt', 'value': 'LINESTRING (-122.769499 38.005947, -122.773625 37.999047)'}, 'withinDistance': '10 mi', 'distanceAttributeName': 'dist', 'maxFeatures': '5', 'inputPointAttributeName': 'inputPoint', 'targetPointAttributeName': 'targetPoint', 'bearingAttributeName': 'bearing'}

Example 2 Request (Address):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'attributes': ['incremental_s_no', 'state', 'wr_id'], 'location': {'format': 'address', 'value': 'POINT REYES STATION CA', 'country': 'United States'}, 'withinDistance': '10 mi', 'distanceAttributeName': 'dist', 'maxFeatures': '5', 'inputPointAttributeName': 'inputPoint', 'targetPointAttributeName': 'targetPoint', 'bearingAttributeName': 'bearing'}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the spatial table (e.g., '/risks/flood_risk')"},
                "attributes": {"type": "array", "items": {"type": "string"}, "description": "Comma separated list of column names of enrich table to be included in the response. '*' can be used to specify all columns, will only include scalar columns."},
                "location": {"type": "object", "description": "Input geometry or address. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "withinDistance": {"type": "string", "description": "Distance within which nearest features will be searched. Must be positive, zero or negative values are not allowed (e.g., '10 mi', '5 km')"},
                "distanceAttributeName": {"type": "string", "description": "Custom name of distance parameter."},
                "maxFeatures": {"type": "integer", "description": "Maximum number of features returned. Default value is 10 and minimum value is 1.", "default": 10, "minimum": 1},
                "uomAttributeName": {"type": "string", "description": "Custom name of unit of measurement parameter."},
                "inputPointAttributeName": {"type": "string", "description": "Custom name of point on input from which distance is calculated."},
                "targetPointAttributeName": {"type": "string", "description": "Custom name of point on target from which distance is calculated."},
                "bearingAttributeName": {"type": "string", "description": "Custom name of bearing angle between input and target point."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"},
                "sortBy": {"type": "string", "description": "Column name to sort by."},
                "sortOrder": {"type": "string", "description": "Sort order: 'ASC' or 'DESC'."},
                "limit": {"type": "integer", "description": "Specifies the maximum number of results to return."},
                "offset": {"type": "integer", "description": "Specifies the number of records to skip."}
            },
            "required": ["tableName", "location", "withinDistance", "attributes"]
        }
    ),
    Tool(
        name="search_at_location",
        description="""Searches for and returns detailed info about locations or points of interest when they're within the input geometry, or when they contain the input geometry, or when they intersect with the input geometry. Input can also be an address, no need to geocode it. Use list_spatial_tables tool to find available spatial tables/data, get_table_metadata tool for available columns and their metadata, and get_spatial_products tool to discover recommended summary attributes, label columns, and data vintage, layer extents, and other metadata.

Spatial operation semantics — choose carefully based on the query intent:
- Use 'contains' when the query asks for table features that ENCLOSE or SURROUND the input point/geometry. Natural language cues: "containing", "enclosing", "surrounding", "which X contains this address", "find the building/parcel/zone that contains this location". Example: "find the building containing this address" → the building (table feature) contains the address point → use 'contains'.
- Use 'within' when the query asks for table features that are INSIDE the input geometry. Natural language cues: "within", "inside", "that fall within this area". Example: "find all parcels within this polygon" → parcels are within the polygon → use 'within'.
- Use 'intersects' when the query asks for table features that INTERSECT, CROSS, TOUCH, OVERLAP or share any portion of the input geometry. Natural language cues: "intersecting", "crossing", "overlapping".

Returns: GeoJSON FeatureCollection with matching features, recordsMatched, recordsReturned, and metadata.

Example 1 Request (Geometry, WITHIN):
{'spatialOperation': 'WITHIN', 'tableName': '/risks/flood_risk', 'attributes': ['statecode', 'type', 'mapname', 'incremental_s_no'], 'location': {'format': 'wkt', 'value': 'MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211)))'}, 'bufferDistance': '10 mi'}

Example 2 Request (Address, WITHIN):
{'spatialOperation': 'WITHIN', 'tableName': '/properties/parcels', 'attributes': ['prclid'], 'location': {'format': 'address', 'value': '1 GLOBAL VW, TROY NY 12180-8371, UNITED STATES OF AMERICA', 'country': 'USA'}, 'bufferDistance': '1 km'}

Example 3 Request (Address, CONTAINS — find the building enclosing an address):
{'spatialOperation': 'contains', 'tableName': '/properties/buildings', 'attributes': ['*'], 'location': {'format': 'address', 'value': '2286 JACKSON ST, SAN FRANCISCO CA 94115-1321, UNITED STATES OF AMERICA', 'country': 'USA'}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the spatial table (e.g., '/risks/flood_risk')"},
                "attributes": {"type": "array", "items": {"type": "string"}, "description": "Comma separated list of column names of enrich table to be included in the response. '*' can be used to specify all columns, will only include scalar columns."},
                "location": {"type": "object", "description": "Input geometry or address. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "spatialOperation": {"type": "string", "description": "Spatial operation to perform. Supported values: intersects, within, contains. Choose based on query intent: use 'contains' when a table feature should enclose/surround the input (e.g., 'find the building containing this address'); use 'within' when table features should be inside the input area; use 'intersects' when any intersection/overlap is acceptable."},
                "bufferDistance": {"type": "string", "description": "Distance by which the input geometry will be extrapolated (e.g., '100 m', '2 km')."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"},
                "sortBy": {"type": "string", "description": "Column name to sort by."},
                "sortOrder": {"type": "string", "description": "Sort order: 'ASC' or 'DESC'."},
                "limit": {"type": "integer", "description": "Specifies the maximum number of results to return."},
                "offset": {"type": "integer", "description": "Specifies the number of records to skip."}
            },
            "required": ["tableName", "attributes", "location"]
        }
    ),
    Tool(
        name="overlap",
        description="""Returns geometries that represent the overlap of the input geometry/address with the geometries in the target table, along with the percentage and area/length of overlap/intersection. Input can also be an address, no need to geocode it. If input is an address, bufferDistance is required. Use list_spatial_tables tool to find available spatial tables/data, get_table_metadata tool for available columns and their metadata, and get_spatial_products tool to discover recommended summary attributes, label columns, and data vintage, layer extents, and other metadata.

Returns: GeoJSON FeatureCollection with overlapping geometries, intersection area/length, and percentage of overlap with both target and input geometries.

Example 1 Request (Geometry):
{'tableName': '/risks/historical_weather_hurricanelines_world', 'uom': 'mi', 'attributes': ['stormname', 'windspeed'], 'location': {'format': 'wkt', 'value': 'POLYGON ((-74.286804 40.515887, -74.292297 40.478292, -73.66333 40.560765, -73.737488 40.839788, -74.002533 40.909361, -74.286804 40.515887))'}, 'totalAttributeName': 'tc'}

Example 2 Request (Address):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'uom': 'mi', 'attributes': ['state', 'riskdesc'], 'location': {'format': 'address', 'value': '1 Global View Troy NY', 'country': 'USA'}, 'bufferDistance': '5 km'}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the spatial table (e.g., '/properties/buildings', '/risks/flood_risk')"},
                "attributes": {"type": "array", "items": {"type": "string"}, "description": "Comma separated list of column names of enrich table to be included in the response. '*' can be used to specify all columns; will only include scalar columns."},
                "location": {"type": "object", "description": "Input geometry or address. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "uom": {"type": "string", "description": "Unit of measurement used to return intersection length/area (e.g., 'm')"},
                "areaAttributeName": {"type": "string", "default": "intersectionArea", "description": "Custom name of intersection area parameter when intersection area is polygon. Default: 'intersectionArea'."},
                "lengthAttributeName": {"type": "string", "default": "intersectionLength", "description": "Custom name of intersection length parameter when intersection area is linestring. Default: 'intersectionLength'."},
                "percentTargetAttributeName": {"type": "string", "default": "percentageOfTarget", "description": "Custom name of parameter indicating percentage of overlap with target geometry. Default: 'percentageOfTarget'."},
                "percentInputAttributeName": {"type": "string", "default": "percentageOfInput", "description": "Custom name of parameter indicating percentage of overlap with input geometry. Default: 'percentageOfInput'."},
                "uomAttributeName": {"type": "string", "default": "uom", "description": "Custom name of unit of measurement parameter. Default: 'uom'."},
                "bufferDistance": {"type": "string", "description": "Distance by which the input geometry will be extrapolated (e.g., '100 m', '2 km')."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"},
                "limit": {"type": "integer", "description": "Specifies the maximum number of results to return."},
                "offset": {"type": "integer", "description": "Specifies the number of records to skip."}
            },
            "required": ["tableName", "attributes", "location", "uom"]
        }
    ),
    Tool(
        name="get_spatial_products",
        description="""Get a list of available Enrich Data products along with their metadata such as product family, geography, data vintage, availablity, recommended zoom levels, styles, summary attributes, label columns, layer extents, and other metadata.

Returns: List of product metadata objects with productId, productName, productFamily, vintage, geography, and layers (including layerId, displayName, featureTable, recommendedStyle).

Example Request: https://api.cloud.precisely.com/v1/spatial/products""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="list_spatial_tables",
        description="""Retrieves list of available spatial tables.

Returns: List of spatial table names available in the database.

Example Request: https://api.cloud.precisely.com/v1/spatial/tables""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="get_table_metadata",
        description="""Retrieves metadata for a specific spatial table.

Returns: Object with table name, columns and their description and type, bounding box in case of spatial table, and row count.

Example Request: https://api.cloud.precisely.com/v1/spatial/tables/properties/buildings/metadata""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the spatial table for which the metadata needs to be described (e.g., 'properties/buildings', 'risks/flood_risk')"}
            },
            "required": ["tableName"]
        }
    ),
    Tool(
        name="summarize",
        description="""Generates min, max, avg, sum, or median statistics for given columns of geometries fully within the input geometry, or intersecting the input geometry. Input can also be an address, no need to geocode it. Use list_spatial_tables tool to find available spatial tables/data, get_table_metadata tool for available columns and their metadata, and get_spatial_products tool to discover recommended summary attributes, label columns, and data vintage, layer extents, and other metadata.

Returns: Aggregate statistics for specified columns.

Example 1 Request (Geometry, Intersects):
{'spatialOperation': 'INTERSECTS', 'tableName': '/risks/historical_weather_windgrid', 'aggregateColumns': {'w9': ['min', 'max', 'avg', 'sum']}, 'location': {'format': 'wkt', 'value': 'GEOMETRYCOLLECTION (MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211))), LINESTRING (-121.756899 37.653383, -121.158302 37.304645, -121.690998 37.120906))'}, 'proportionalCalculation': true}

Example 2 Request (Address, Intersects):
{'spatialOperation': 'INTERSECTS', 'tableName': '/risks/flood_risk', 'location': {'format': 'address', 'value': '1 Global View Troy NY', 'country': 'USA'}, 'aggregateColumns': {'id': ['min', 'max', 'avg', 'sum']}, 'proportionalCalculation': true, 'bufferDistance': '10 km'}

Example 3 Request (Geometry, Within):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'location': {'format': 'WKT', 'value': 'POLYGON ((-122.766919 38.031512, -122.766919 38.051864, -122.741314 38.051864, -122.741314 38.031512, -122.766919 38.031512))'}, 'spatialOperation': 'within', 'proportionalCalculation': false, 'aggregateColumns': {'acres': ['min', 'MAX', 'avg', 'sum', 'MEDIAN']}}

Example 4 Request (Address, Within):
{'tableName': '/risks/wildfire_risk_fire_perimeter', 'location': {'format': 'address', 'value': '1 Global View Troy NY', 'country': 'USA'}, 'spatialOperation': 'within', 'proportionalCalculation': false, 'bufferDistance': '10 km', 'aggregateColumns': {'acres': ['min', 'MAX', 'avg', 'sum', 'MEDIAN']}}""",
        inputSchema={
            "type": "object",
            "properties": {
                "tableName": {"type": "string", "description": "Name of the spatial table (e.g., '/risks/historical_weather_windgrid')"},
                "aggregateColumns": {"type": "object", "description": "Dictionary of column names mapped to lists of aggregate functions. Supported functions: min, max, avg, sum, median."},
                "location": {"type": "object", "description": "Input geometry or address. Supported formats: wkt, geojson, lonlat, address. If format is 'address', country field is mandatory."},
                "spatialOperation": {"type": "string", "description": "Spatial operation to perform. Supported values: intersects, within."},
                "proportionalCalculation": {"type": "boolean", "description": "Whether to use proportional calculation. Only applicable when the spatialOperation parameter is 'intersects'"},
                "bufferDistance": {"type": "string", "description": "Distance by which the input geometry will be extrapolated (e.g., '100 m', '2 km')."},
                "attributeFilter": {"type": "string", "description": "specifies filter on scalar attributes"}
            },
            "required": ["tableName", "location", "aggregateColumns"]
        }
    ),
    ]

