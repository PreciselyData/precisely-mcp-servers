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
        description="""The landing page provides links to essential API resources, including:
- **API Definition:** A machine-readable specification of the API.
- **Conformance Declaration:** A list of standards that the API conforms to.
- **Feature Collections:** Information and links to the available feature collections in the dataset.

Use this endpoint to quickly navigate and explore the API's capabilities.

Returns: Object with links array.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_api_definition",
        description="""This endpoint retrieves the complete OpenAPI definition for the API. The response is a machine-readable specification that describes all available endpoints, request/response schemas, and security configurations.

- **Format:** The API definition conforms to the OpenAPI 3.0.1 standard.

Returns: OpenAPI 3.0.1 specification document describing all available endpoints.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/api""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_functions",
        description="""This endpoint returns a list of available spatial functions within the API.
- **Purpose:** Provides supported spatial functions that can be used for querying features.
- **Function Metadata:** Includes function names, argument types, and return types.

Returns: List of available spatial functions with function names, argument types, and return types.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/functions""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_conformance",
        description="""This endpoint returns the conformance declaration for the API. The conformance declaration is a list of all conformance classes specified in a standard that the server adheres to. It helps clients determine whether the API meets the required standards and their own requirements.

- **Purpose:** Provides a comprehensive list of conformance classes to verify the API's compliance with OGC API standards and additional specifications.
- **Standards:** Includes OGC API conformance classes and any extra specifications the API supports.

Returns: Conformance declaration listing all conformance classes the server adheres to.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/conformance""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_collections",
        description="""This endpoint returns the list of feature collections available on the server. Each collection represents a spatial dataset that can be queried and provides essential metadata, including:

- **Collection ID:** spatial dataset's unique identifier.
- **Title and Description**
- **Collection Item Type**
- **Links:** Navigational links to access the collection’s items (e.g., `/collections/{collectionId}/items`).

This resource is designed to help clients discover available geospatial datasets and understand the structure of each collection before making queries.

Returns: List of feature collections with metadata including collection IDs, titles, descriptions, and links.

Example Request: https://api.cloud.precisely.com/v1/ogcapi/enrich/collections""",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="ogc_collection",
        description="""Gives information about the feature collection with id `{collectionId}`. The response contains:

- A link to the items in the collection (path `/collections/{collectionId}/items`, relation: items).
- A unique local identifier for the collection.
- Title and description for the collection.
- An optional indicator of the item type (default is 'feature').

Returns: Collection metadata including id, title, description, and links to items/schema.

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
        description="""Provides the schema for collection with id `{collectionId}`. The schema defines the structure of the collection. The response includes:

- **Field Names:** Names of each field/attribute/property/column in the collection.
- **Data Types/Formats:** The expected data type (e.g., string, integer, double) for each field.
- **Descriptions:** Explanatory details for each attribute to clarify its purpose.

This information is essential for validating client queries and constructing dynamic interfaces.

Returns: JSON describing the collection structure with properties/field names, data types/formats, and descriptions.

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
        description="""This resource returns the queryable properties for a specific collection identified by its unique id. It provides detailed metadata for each attribute in the collection that can be used to filter queries. The response includes:

- **Field Names:** The names of queryable fields/attributes/properties/columns in the collection.
- **Descriptions:** A description of each attribute to clarify its purpose and usage.
- **Formats:** The data types i.e. formats (e.g., string, number, geospatial) of each attribute.

This metadata is essential for clients to build dynamic query interfaces and validate their requests against the collection's schema.

Returns: Queryable properties with metadata for each filterable attribute in the collection.

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

Every feature in a dataset belongs to a collection. A dataset may consist of multiple feature collections, each representing a group of features that share a common schema and type.

The **collection id** is a unique identifier for the spatial dataset and is used to reference a specific collection within the API.

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
        description="""Processes WMS requests using GET: GetCapabilities, GetMap, or GetFeatureInfo. Use GetCapabilities to retrieve all available layers, their styles, CRS, and geographic bounding box. Use get_spatial_products tool to discover recommended styles, summary attributes, label columns, and data vintage, layer extents, and other metadata.

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
                "REQUEST": {"type": "string", "description": "The WMS request type: GetCapabilities, GetMap, or GetFeatureInfo"},
                "SERVICE": {"type": "string", "description": "Service type. Always 'WMS'."},
                "VERSION": {"type": "string", "description": "WMS version. Supported: '1.1.1', '1.3.0'."},
                "crs": {"type": "string", "description": "Coordinate reference system (WMS 1.3.0). 'EPSG:3857', 'EPSG:4326' or 'CRS:84'"},
                "srs": {"type": "string", "description": "Spatial reference system (WMS 1.1.1) 'EPSG:3857', 'EPSG:4326' or 'CRS:84'"},
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
                "BGCOLOR": {"type": "string", "description": "Background color for the map image."},
                "RESOLUTION": {"type": "string", "description": "Resolution of the map image."},
                "EXCEPTIONS": {"type": "string", "description": "Format for exception reporting."}
            },
            "required": ["REQUEST", "SERVICE", "VERSION"]
        }
    ),
    Tool(
        name="wms_post_get_map",
        description="""Processes WMS GetMap requests using POST. Supports both WMS 1.3.0 (use 'crs' param) and WMS 1.1.1 (use 'srs' param). Accepts SLD_BODY as a form parameter (URL-encoded JSON). Use wms_get_request GetCapabilities to retrieve all available layers, their styles, CRS, and geographic bounding box. Use get_spatial_products tool to discover recommended styles, and data vintage, layer extents, and other metadata.

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
        description="""Handles WMTS operations via the KVP (Key-Value Pair) query parameter interface. Use Request=GetCapabilities to retrieve all available layers, their styles, tile matrix sets, and supported formats. Use Request=GetTile to retrieve a map tile image by specifying Layer, Style, TileMatrixSet, TileMatrix, TileRow, TileCol, and Format. Use get_spatial_products tool to discover recommended styles, zoom levels, and data vintage, layer extents, and other metadata.

Returns: For GetCapabilities: Dict with 'xml' (str) containing the capabilities XML document and 'content_type' (str). For GetTile: Dict with 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

Example 1 GetCapabilities Request:
https://api.cloud.precisely.com/v1/spatial/wmts?SERVICE=WMTS&REQUEST=GetCapabilities&ACCEPTVERSIONS={version}""",
        inputSchema={
            "type": "object",
            "properties": {
                "Service": {"type": "string", "description": "Service type. Always 'WMTS'."},
                "Request": {"type": "string", "description": "The WMTS request type: GetCapabilities or GetTile."},
                "Version": {"type": "string", "description": "WMTS version (e.g., '1.0.0')."},
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
        description="""Returns a map tile, using standard parameters/approach. RESTful encoding of WMTS service. Use wmts_request with Request=GetCapabilities to retrieve all available layers, their styles, tile matrix sets, and supported formats. Use get_spatial_products tool to discover recommended styles, zoom levels, and data vintage, layer extents, and other metadata.

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
        description="""Returns a map tile, using less parameters/simple approach. Use this tool when you do NOT need to specify Style or TileMatrixSet. RESTful encoding of WMTS service. Use wmts_request with Request=GetCapabilities to retrieve all available layers, their styles, tile matrix sets, and supported formats. Use get_spatial_products tool to discover recommended styles, zoom levels, and data vintage, layer extents, and other metadata.

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
