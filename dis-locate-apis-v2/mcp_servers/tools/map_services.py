"""
Map Services Tools Module
Contains 15 tools for WMS, WMTS, and OGC Features APIs
"""
from typing import List, Dict, Any
from mcp.types import Tool, TextContent, ImageContent, CallToolResult
from mcp_servers.tools.base_tool import get_logger
import json

logger = get_logger(__name__)


def get_tools() -> list[Tool]:
    """Returns list of map services tool definitions"""
    return [
        Tool(
        name="ogc_landing_page",
        description="""Discovery tool: retrieve the OGC API landing page with links to essential API resources.
Provides links to the API definition, conformance declaration, and feature collections.
Use this as the entry point to navigate and explore OGC API capabilities.
Call this first if you have no other OGC resource URLs and need to discover what is available.

Returns: Object with links array (API definition, conformance, feature collections).

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_api_definition",
        description="""Discovery tool: retrieve the full OpenAPI 3.0.1 specification for the OGC Enrich API.
The specification describes all available endpoints, request/response schemas, and security configurations.
Use this when you need to inspect full API capabilities programmatically.
Do NOT use for listing feature collections — use ogc_collections instead.

Returns: OpenAPI 3.0.1 specification document.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/api""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_functions",
        description="""Discovery tool: retrieve a list of available spatial functions within the OGC Enrich API.
Use this to discover what spatial functions (e.g., s_contains, s_within, s_intersects) can be used
in filter expressions for ogc_collection_items queries.

Returns: List of spatial functions with their names, argument types, and return types.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/functions""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_conformance",
        description="""Discovery tool: retrieve the conformance declaration listing all OGC API standards this server conforms to.
Use this to verify whether the API supports specific OGC standards required by your client.
Do NOT use to discover feature collections — use ogc_collections instead.

Returns: Conformance declaration with a list of conformance class URIs.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/conformance""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_collections",
        description="""Discovery tool: retrieve the list of all available OGC feature collections (spatial datasets) with metadata.
Use this tool when you need to discover available datasets (collectionIds) before calling
ogc_collection, ogc_collection_schema, ogc_collection_queryables, ogc_collection_items, or ogc_feature_by_id.
Do NOT use this to fetch actual features — use ogc_collection_items or ogc_feature_by_id once you have the collectionId.

Returns: List of feature collection metadata objects with id, title, description, item type, and navigation links.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_collection",
        description="""Retrieve metadata for a specific OGC feature collection identified by collectionId.
Returns title, description, item type, and links to items and schema for the collection.
Use ogc_collections first if you do not yet know the collectionId.
Do NOT use this to fetch actual features — use ogc_collection_items or ogc_feature_by_id instead.
Do NOT use this for column/field schema — use ogc_collection_schema or ogc_collection_queryables instead.

Returns: Collection metadata object with id, title, description, and navigation links.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "Unique identifier of the collection (e.g., 'properties/buildings')"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_collection_schema",
        description="""Retrieve the full schema (all field names, data types, and descriptions) for a specific OGC feature collection.
Use this tool when you need to know all fields and their types for a collection, including non-queryable fields.
Call ogc_collections first if you do not yet know the collectionId.
Do NOT use this for filtering — for filterable/queryable fields only, use ogc_collection_queryables instead
(ogc_collection_queryables is a subset of ogc_collection_schema focused on fields usable in CQL filter expressions).

Returns: JSON schema with all field names, data types (string, integer, double, etc.), and descriptions.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/schema""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "Unique identifier of the collection (e.g., 'properties/buildings')"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_collection_queryables",
        description="""Retrieve the filterable (queryable) fields for a specific OGC feature collection.
Queryable fields are the subset of collection properties that can be used in CQL filter expressions
when calling ogc_collection_items (e.g., filter=fieldName='value' or spatial filters).
Use this tool before constructing filter queries for ogc_collection_items to verify which fields can be filtered.
Call ogc_collections first if you do not yet know the collectionId.
Do NOT use this if you need all fields including non-queryable ones — use ogc_collection_schema instead.

Returns: List of queryable property definitions with field name, data type/format, and description.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/queryables""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "Unique identifier of the collection (e.g., 'properties/buildings')"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_collection_items",
        description="""Fetch features of the feature collection with id `{collectionId}` subject to parameters. Use ogc_collections tool to list all available collections and their ids, ogc_collection_queryables tool to get properties that can be used for filtering, and get_spatial_products tool to discover layer extents for bbox, data vintage, recommended label columns, and other metadata.

Additional capabilities include:
- **Filtering:** Supports attribute-based filtering using CQL (Common Query Language).
- **Pagination:** Use `limit` and `offset` parameters to paginate results.
- **Spatial Queries:**
  - **Bounding Box (bbox):** Retrieve features within a rectangular spatial extent (`minX, minY, maxX, maxY`).
  - **Spatial Filters:** Support for `contains`, `intersects`, and `within` (OGC Filter Encoding).

Returns: GeoJSON FeatureCollection with features matching the query, and pagination links.

Example 1 Request (Items without additional parameters): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items

Example 2 Request (Items with limit): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?limit=5

Example 3 Request (Items with offset): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?limit=5&offset=10

Example 4 Request (Items with bbox): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?bbox=-74.013219,40.702976,-74.01162,40.70357&limit=100

Example 5 Request (Items with filter and s_contains): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=s_contains(GEOM,POINT (-74.011728 40.701114))&limit=100

Example 6 Request (Items with filter and s_within): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=s_within(GEOM,POLYGON ((-74.009523 40.703347, -74.010445 40.704257, -74.011078 40.704062, -74.011127 40.703363, -74.010526 40.702822, -74.009523 40.703347)))&limit=100

Example 7 Request (Items with filter and s_intersects): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=s_intersects(GEOM,POLYGON ((-74.009523 40.703347, -74.010445 40.704257, -74.011078 40.704062, -74.011127 40.703363, -74.010526 40.702822, -74.009523 40.703347)))&limit=100

Example 8 Request (Items with filter and = operator): https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items?filter=bldgid%3D'B000CTPA4MY1'""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "The unique identifier for the feature collection (e.g., 'properties/buildings')"},
                "limit": {"type": "string", "description": "Number of features to return. Default: 10."},
                "offset": {"type": "string", "description": "Number of features to skip. Default: 0."},
                "bbox": {"type": "string", "description": "Bounding box for spatial filtering (minX, minY, maxX, maxY) (e.g., '-74.2,40.8,-73.9,40.9')"},
                "filter": {"type": "string", "description": "Filter query in CQL format. (e.g., type = 'residential'"}
            },
            "required": ["collectionId"]
        }
    ),
    Tool(
        name="ogc_feature_by_id",
        description="""Retrieves a single feature having unique id `{featureId}` from collection with id `{collectionId}`.

Returns: GeoJSON FeatureCollection with geometry and properties of the feature(s).

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections/properties/buildings/items/1""",
        inputSchema={
            "type": "object",
            "properties": {
                "collectionId": {"type": "string", "description": "The unique identifier for the feature collection (e.g., 'properties/buildings')"},
                "featureId": {"type": "string", "description": "The unique identifier for the feature within the collection (e.g., '1')"}
            },
            "required": ["collectionId", "featureId"]
        }
    ),
    # ========================================
    # WMS (Web Map Service) APIs (2 tools)
    # ========================================
    Tool(
        name="wms_get_request",
        description="""Processes following WMS requests using HTTP GET: GetCapabilities, GetMap, or GetFeatureInfo. Use GetCapabilities to retrieve all available layers, their styles, CRS, and geographic bounding box. Use get_spatial_products tool to discover recommended styles, summary attributes, label columns, and data vintage, layer extents, and other metadata.

Returns: For GetMap success: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int). For GetCapabilities success: Dict with 'xml' (str), 'content_type' (str). For GetFeatureInfo success: JSON dict. On any error (auth, invalid params, or WMS ServiceException): Dict with 'error' (str) containing the error or ServiceExceptionReport XML.

Example 1 GetCapabilities Request:
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetCapabilities

Example 2 GetMap Request (WMS version 1.1.1, SRS parameter for EPSG:4326, Axis order lon-lat for BBOX):
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&SRS=EPSG:4326&BBOX=-125,24,-66,50&WIDTH=400&HEIGHT=300&Layers=census_state&STYLES=census_state&FORMAT=image/png

Example 3 GetMap Request (WMS version 1.3.0, CRS parameter for CRS:84, Axis order lon-lat for BBOX):
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetMap&CRS=CRS:84&BBOX=-125,24,-66,50&WIDTH=400&HEIGHT=300&Layers=census_state&STYLES=census_state&FORMAT=image/png

Example 4 GetMap Request (WMS version 1.3.0, CRS parameter for EPSG:4326, Axis order lat-lon for BBOX):
https://api.cloud.precisely.com/v1/Spatial/WMS?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetMap&CRS=EPSG:4326&BBOX=24,-125,50,-66&WIDTH=400&HEIGHT=300&Layers=census_state&STYLES=census_state&FORMAT=image/png

Example 5 GetFeatureInfo Request:
https://api.cloud.precisely.com/v1/spatial/wms?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetFeatureInfo&CRS=EPSG:4326&BBOX=29.19367847889249035,-98.56156199862394374,29.35037762857998089,-98.33146912069426548&WIDTH=400&HEIGHT=300&LAYERS=wildfire_risk&INFO_FORMAT=application/json&QUERY_LAYERS=wildfire_risk&I=1&J=1&PIXELSEARCHRADIUS=10""",
        inputSchema={
            "type": "object",
            "properties": {
                "REQUEST": {
                    "type": "string",
                    "description": "The WMS request type.",
                    "enum": ["GetCapabilities", "GetMap", "GetFeatureInfo"]
                },
                "SERVICE": {"type": "string", "description": "Service type. Always 'WMS'.", "enum": ["WMS"]},
                "VERSION": {"type": "string", "description": "WMS version. Use '1.1.1' (SRS+lon-lat BBOX) or '1.3.0' (CRS; axis order depends on CRS).", "enum": ["1.1.1", "1.3.0"]},
                "crs": {"type": "string", "description": "Coordinate reference system (WMS 1.3.0). 'EPSG:3857', 'EPSG:4326' or 'CRS:84'"},
                "srs": {"type": "string", "description": "Spatial reference system (WMS 1.1.1) 'EPSG:3857' or 'EPSG:4326'"},
                "BBOX": {"type": "string", "description": "The area to be mapped, specified as four comma-separated numbers: 'min_x,min_y,max_x,max_y'. Order's dependent on SRS or CRS (e.g., '-30,20,50,80')."},
                "width": {"type": "string", "description": "Width of the map image in pixels."},
                "height": {"type": "string", "description": "Height of the map image in pixels."},
                "layers": {"type": "string", "description": "Comma-separated list of layer names to display."},
                "STYLES": {"type": "string", "description": "Comma-separated list of one rendering style per requested layer. A style is required for each layer requested. STYLES=Style1,,Style3"},
                "FORMAT": {"type": "string", "description": "Output format of map image (e.g., 'image/png')."},
                "TRANSPARENT": {"type": "string", "description": "Whether the map background is transparent, 'TRUE' or 'FALSE'."},
                "Info_Format": {"type": "string", "description": "Format for GetFeatureInfo response (e.g., 'application/json')."},
                "QUERY_LAYERS": {"type": "string", "description": "Comma-separated list of layers to query for GetFeatureInfo."},
                "I": {"type": "string", "description": "X pixel coordinate for GetFeatureInfo (WMS 1.3.0)."},
                "J": {"type": "string", "description": "Y pixel coordinate for GetFeatureInfo (WMS 1.3.0)."},
                "X": {"type": "string", "description": "X pixel coordinate for GetFeatureInfo (WMS 1.1.1)."},
                "Y": {"type": "string", "description": "Y pixel coordinate for GetFeatureInfo (WMS 1.1.1)."},
                "Feature_Count": {"type": "string", "description": "Maximum number of features returned for GetFeatureInfo."},
                "PIXELSEARCHRADIUS": {"type": "string", "description": "Pixel search radius for GetFeatureInfo."},
                "BGCOLOR": {"type": "string", "description": "Hex RGB background color for the map image."},
                "RESOLUTION": {"type": "string", "description": "Resolution of the map image. Minimum 72 dpi."},
                "EXCEPTIONS": {"type": "string", "description": "Format for exception reporting."}
            },
            "required": ["REQUEST", "SERVICE", "VERSION"]
        }
    ),
    Tool(
        name="wms_post_get_map",
        description="""Processes WMS GetMap requests using HTTP POST. Supports both WMS 1.3.0 (use 'crs' param) and WMS 1.1.1 (use 'srs' param). Accepts SLD_BODY as a form parameter (URL-encoded JSON). Use wms_get_request GetCapabilities to retrieve all available layers, their styles, CRS/SRS, and geographic bounding box. Use get_spatial_products tool to discover recommended styles, and data vintage, layer extents, and other metadata.

When the STYLES parameter is left empty, the styling defined in SLD_BODY (if provided) is applied. If the STYLES parameter specifies a server-side style, the SLD_BODY is ignored, even if it is included in the request.

Returns: On success: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int). On any error (auth, invalid params, or WMS ServiceException): Dict with 'error' (str) containing the error or ServiceExceptionReport XML.

Example 1 Post Request for one layer (solid brown fill with darker brown outline for buildings):
POST https://api.cloud.precisely.com/v1/spatial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=37.78662956646336823%2C-122.2745967175037549%2C37.81410536165775227%2C-122.2403683391127061&CRS=EPSG%3A4326&WIDTH=1062&HEIGHT=853&LAYERS=buildings&STYLES=&FORMAT=image%2Fpng&TRANSPARENT=TRUE
Content-Type: application/x-www-form-urlencoded
BODY: SLD_BODY={"styleDetails": [{"themeList": {"theme": [{"type": "OverrideTheme","style": {"type": "MapBasicCompositeStyle","AreaStyle": {"type": "MapBasicAreaStyle","MapBasicPen": {"width": 1,"pattern": 2,"color": "#964B00","unit": "PIXEL"},"MapBasicBrush": {"pattern": 2,"foregroundColor": "#E0AB8B","backgroundColor": "#C0C0C0"}}}}]}}]}
(SLD_BODY must be URL-encoded when sent as form data)

Example 2 Post Request for two layers (solid brown fill for buildings, blue star icon for address_fabric points). Note: styleDetails is an array with one entry per layer, each entry containing the layer name and its themeList:
POST https://api.cloud.precisely.com/v1/spatial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=37.78662956646336823%2C-122.2745967175037549%2C37.81410536165775227%2C-122.2403683391127061&CRS=EPSG%3A4326&WIDTH=1062&HEIGHT=853&LAYERS=buildings,address_fabric&STYLES=&FORMAT=image%2Fpng&TRANSPARENT=TRUE
Content-Type: application/x-www-form-urlencoded
BODY: SLD_BODY={"styleDetails": [{"layer": {"name": "address_fabric","type": "NamedLayer"},"themeList": {"theme": [{"type": "OverrideTheme","style": {"type": "MapBasicCompositeStyle","PointStyle": {"type": "MapBasicPointStyle","MapBasicSymbol": {"type": "MapBasicFontSymbol","shape": 36,"size": 12,"color": "255","fontName": "MapInfo Symbols","rotation": 0,"bold": false,"dropShadow": false,"border": "NONE"}}}}]}},{"layer": {"name": "buildings","type": "NamedLayer"},"themeList": {"theme": [{"type": "OverrideTheme","style": {"type": "MapBasicCompositeStyle","AreaStyle": {"type": "MapBasicAreaStyle","MapBasicPen": {"width": 1,"pattern": 2,"color": "#964B00","unit": "PIXEL"},"MapBasicBrush": {"pattern": 2,"foregroundColor": "#E0AB8B","backgroundColor": "#C0C0C0"}}}}]}}]}
(SLD_BODY must be URL-encoded when sent as form data)""",
        inputSchema={
            "type": "object",
            "properties": {
                "REQUEST": {"type": "string", "description": "The WMS request type. Always 'GetMap' for this endpoint."},
                "SERVICE": {"type": "string", "description": "Service type. Always 'WMS'."},
                "VERSION": {"type": "string", "description": "WMS version ('1.3.0' uses crs param; '1.1.1' uses srs param)."},
                "crs": {"type": "string", "description": "Coordinate reference system for WMS 1.3.0 (e.g., 'EPSG:4326', 'CRS:84', 'EPSG:3857')."},
                "srs": {"type": "string", "description": "Spatial reference system for WMS 1.1.1 (e.g., 'EPSG:4326', 'EPSG:3857')."},
                "BBOX": {"type": "string", "description": "Bounding box coordinates."},
                "width": {"type": "string", "description": "Width of the map image in pixels."},
                "height": {"type": "string", "description": "Height of the map image in pixels."},
                "layers": {"type": "string", "description": "Comma-separated list of layer names."},
                "STYLES": {"type": "string", "description": "Comma-separated list of style names, one per requested layer."},
                "FORMAT": {"type": "string", "description": "Output format (e.g., 'image/png')."},
                "TRANSPARENT": {"type": "string", "description": "Whether the map background is transparent ('TRUE' or 'FALSE')."},
                "SLD_BODY": {"type": "string", "description": "Proprietary Precisely JSON style definition for customizing layer appearance."},
            },
            "required": ["REQUEST", "SERVICE", "VERSION", "BBOX", "width", "height", "layers", "STYLES", "FORMAT"]
        }
    ),
    # ========================================
    # WMTS (Web Map Tile Service) APIs (3 tools)
    # ========================================
    Tool(
        name="wmts_request",
        description="""Handles WMTS operations via the KVP (Key-Value Pair) query parameter interface. Use Request=GetCapabilities to retrieve all available layers, their styles, tile matrix sets, and supported formats. Use Request=GetTile to retrieve a map tile image by specifying Layer, Style, TileMatrixSet, TileMatrix, TileRow, TileCol, and Format. Use get_spatial_products tool to discover recommended zoom levels, and data vintage, layer extents, and other metadata.

Returns: For GetCapabilities: Dict with 'xml' (str) containing the capabilities XML document and 'content_type' (str). For GetTile: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

Example 1 GetCapabilities Request:
https://api.cloud.precisely.com/v1/spatial/wmts?SERVICE=WMTS&REQUEST=GetCapabilities&ACCEPTVERSIONS={version}""",
        inputSchema={
            "type": "object",
            "properties": {
                "Service": {"type": "string", "description": "Service type. Always 'WMTS'."},
                "Request": {
                    "type": "string",
                    "description": "The WMTS request type.",
                    "enum": ["GetCapabilities", "GetTile"]
                },
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0').", "enum": ["1.0.0"]},
                "Layer": {"type": "string", "description": "Layer name for GetTile request."},
                "Style": {"type": "string", "description": "Style name for GetTile request."},
                "TileMatrixSet": {"type": "string", "description": "Tile matrix set identifier for GetTile request."},
                "TileMatrix": {"type": "string", "description": "Tile matrix (zoom level) for GetTile request."},
                "TileRow": {"type": "integer", "description": "Tile row for GetTile request."},
                "TileCol": {"type": "integer", "description": "Tile column for GetTile request."},
                "Format": {"type": "string", "description": "Output format for GetTile. 'image/png' or 'application/vnd.mapbox-vector-tile'"}
            },
            "required": ["Service", "Request"]
        }
    ),
    Tool(
        name="wmts_get_standard_tile",
        description="""Returns a map tile, using standard parameters/approach. RESTful encoding of WMTS service. Use wmts_request with Request=GetCapabilities to retrieve all available layers, their styles, tile matrix sets, and supported formats. Use get_spatial_products tool to discover recommended zoom levels, and data vintage, layer extents, and other metadata.

Returns: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int) containing the requested map tile.

Example Request: https://api.cloud.precisely.com/v1/spatial/wmts/1.0.0/default/tiles/wildfire_risk/default/WorldWebMercatorQuad_0_to_19/12/1190/1550.png""",
        inputSchema={
            "type": "object",
            "properties": {
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0')."},
                "Layer": {"type": "string", "description": "Layer name (e.g., 'parcels', 'wildfire_risk')."},
                "Style": {"type": "string", "description": "Style name. Comma-separated list of one rendering style per requested layer (e.g., 'default')."},
                "TileMatrixSet": {"type": "string", "description": "Tile matrix set identifier (e.g., 'WorldWebMercatorQuad_0_to_19')."},
                "TileMatrix": {"type": "string", "description": "Tile matrix (zoom level)."},
                "TileCol": {"type": "integer", "description": "Tile column number."},
                "TileRow": {"type": "integer", "description": "Tile row number."},
                "Format": {"type": "string", "description": "Output format. 'png' or 'mvt'"}
            },
            "required": ["Version", "Layer", "Style", "TileMatrixSet", "TileMatrix", "TileCol", "TileRow", "Format"]
        }
    ),
    Tool(
        name="wmts_get_simple_tile",
        description="""Returns a map tile, using less parameters/simple approach. Use this tool when you do NOT need to specify Style or TileMatrixSet. RESTful encoding of WMTS service. Use wmts_request with Request=GetCapabilities to retrieve all available layers, their styles, tile matrix sets, and supported formats. Use get_spatial_products tool to discover recommended zoom levels, and data vintage, layer extents, and other metadata.

Returns: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int) containing the requested map tile.

Example Request: https://api.cloud.precisely.com/v1/spatial/wmts/1.0.0/simpleProfileTile/tiles/wildfire_risk/12/1190/1550.png""",
        inputSchema={
            "type": "object",
            "properties": {
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0')."},
                "Layer": {"type": "string", "description": "Layer name (e.g., 'parcels', 'wildfire_risk')."},
                "TileMatrix": {"type": "string", "description": "Tile matrix (zoom level)."},
                "TileCol": {"type": "integer", "description": "Tile column number."},
                "TileRow": {"type": "integer", "description": "Tile row number."},
                "Format": {"type": "string", "description": "Output format. 'png' or 'mvt'"}
            },
            "required": ["Version", "Layer", "TileMatrix", "TileCol", "TileRow", "Format"]
        }
    ),
    ]


def handle_tool_call(name: str, arguments: Dict[str, Any], precisely_api: Any) -> List[TextContent | ImageContent] | CallToolResult:
    """Handle tool execution for map services tools"""
    try:
        if not hasattr(precisely_api, name):
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                isError=True,
            )
        method = getattr(precisely_api, name)
        result = method(**arguments)

        # Check for error responses first
        if isinstance(result, dict) and "error" in result:
            error_val = result["error"]
            error_text = json.dumps(error_val, indent=2) if isinstance(error_val, dict) else str(error_val)
            return CallToolResult(
                content=[TextContent(type="text", text=error_text)],
                isError=True,
            )

        # Handle image responses for map services
        if isinstance(result, dict) and result.get("image_base64"):
            return [ImageContent(type="image", data=result["image_base64"],
                                mimeType=result.get("content_type", "image/png"))]

        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return CallToolResult(
            content=[TextContent(type="text", text=str(e))],
            isError=True,
        )
