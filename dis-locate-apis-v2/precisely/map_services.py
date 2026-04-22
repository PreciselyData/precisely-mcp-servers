"""OGC Features, WMS, and WMTS API methods (15 tools)."""

import base64
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class MapServicesMixin:
    # ========================================
    # OGC Features APIs
    # ========================================

    def ogc_landing_page(self, **kwargs) -> Dict[str, Any]:
        """The landing page provides links to essential API resources, including:
- **API Definition:** A machine-readable specification of the API.
- **Conformance Declaration:** A list of standards that the API conforms to.
- **Feature Collections:** Information and links to the available feature collections in the dataset.

Use this endpoint to quickly navigate and explore the API's capabilities.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: LandingPageResponse with keys 'title' (str), 'description' (str),
                and 'links' (list of Link objects with href, rel, type, title).

        Example:
            ogc_landing_page()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/"
            logger.debug(f"[ogc_landing_page] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_landing_page] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC landing page error: {e}")
            return self._build_error("OGC landing page", e)

    def ogc_api_definition(self, **kwargs) -> Dict[str, Any]:
        """This endpoint retrieves the complete OpenAPI definition for the API. The response is a machine-readable specification that describes all available endpoints, request/response schemas, and security configurations.

- **Format:** The API definition conforms to the OpenAPI 3.0.1 standard.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Complete OpenAPI 3.0.1 definition as a JSON object with keys 'openapi' (str),
                'info' (dict), 'servers' (list), 'paths' (dict), and 'components' (dict).

        Example:
            ogc_api_definition()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/api"
            headers = {"Accept": "application/vnd.oai.openapi+json;version=3.0"}
            logger.debug(f"[ogc_api_definition] GET {url}")
            response = self.session.get(url, headers=headers)
            logger.debug(f"[ogc_api_definition] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC API definition error: {e}")
            return self._build_error("OGC API definition", e)

    def ogc_functions(self, **kwargs) -> Dict[str, Any]:
        """This endpoint returns a list of available spatial functions within the API.
- **Purpose:** Provides supported spatial functions that can be used for querying features.
- **Function Metadata:** Includes function names, argument types, and return types.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: FunctionResponse with key 'functions' (list of Function objects,
                each with 'name' (str), 'arguments' (list of type arrays), and 'returns' (list of str)).

        Example:
            ogc_functions()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/functions"
            logger.debug(f"[ogc_functions] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_functions] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC functions error: {e}")
            return self._build_error("OGC functions", e)

    def ogc_conformance(self, **kwargs) -> Dict[str, Any]:
        """This endpoint returns the conformance declaration for the API. The conformance declaration is a list of all conformance classes specified in a standard that the server adheres to. It helps clients determine whether the API meets the required standards and their own requirements.

- **Purpose:** Provides a comprehensive list of conformance classes to verify the API's compliance with OGC API standards and additional specifications.
- **Standards:** Includes OGC API conformance classes and any extra specifications the API supports.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: ConformancePageResponse with key 'conformsTo' (list of conformance class URI strings).

        Example:
            ogc_conformance()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/conformance"
            logger.debug(f"[ogc_conformance] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_conformance] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC conformance error: {e}")
            return self._build_error("OGC conformance", e)

    def ogc_collections(self, **kwargs) -> Dict[str, Any]:
        """This endpoint returns the list of feature collections available on the server. Each collection represents a spatial dataset that can be queried and provides essential metadata, including:

- **Collection ID:** A unique identifier for the spatial dataset.
- **Title and Description:** Optional details that describe the collection.
- **Spatial and Temporal Extents:** Indicators of the geographical and time-based coverage of the data.
- **Coordinate Reference Systems (CRS):** A list of supported CRS, with the first being the default (typically WGS 84).
- **Links:** Navigational links to access the collection's items (e.g., `/collections/{collectionId}/items`).

This resource is designed to help clients discover available geospatial datasets and understand the structure of each collection before making queries.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: CollectionsResponse with keys 'links' (list of Link objects) and
                'collections' (list of CollectionsInfo objects with id, title, description, itemType, links).

        Example:
            ogc_collections()
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections"
            logger.debug(f"[ogc_collections] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collections] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collections error: {e}")
            return self._build_error("OGC collections", e)

    def ogc_collection(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """This resource describes the feature collection identified in the path.

Information about the feature collection with id `{collectionId}` is provided. The response contains:

- A link to the items in the collection (path `/collections/{collectionId}/items`, relation: items).
- A unique local identifier for the collection.
- A list of coordinate reference systems (CRS) in which geometries may be returned; the first CRS is the default (typically WGS 84 with axis order longitude/latitude).
- An optional title and description for the collection.
- An optional spatial and temporal extent derived from the data.
- An optional indicator of the item type (default is 'feature').

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: CollectionIdResponse with keys 'id' (str), 'title' (str), 'description' (str),
                'itemType' (str), and 'links' (list of Link objects with href, rel, type, title).

        Example:
            ogc_collection(collectionId="properties/buildings")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}"
            logger.debug(f"[ogc_collection] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collection] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection error: {e}")
            return self._build_error("OGC collection", e)

    def ogc_collection_schema(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """This resource provides the schema for a specified feature collection. The schema defines the structure of the collection and includes details such as field names, data types, formats, and descriptions.

The **collection id** is a unique identifier used to reference a specific dataset. When you provide a collection id, the response includes:

- **Field Names:** Names of each attribute in the collection.
- **Data Types & Formats:** The expected data type (e.g., string, integer, double) and format for each field.
- **Descriptions:** Explanatory details for each attribute to clarify its purpose.
- **Geospatial Data Types:** Specific spatial types for any geospatial attributes, along with the default coordinate reference system.

This information is essential for validating client queries and constructing dynamic interfaces.

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: DescribeCollectionResponse with keys '$schema' (str), '$id' (str),
                'type' (str), 'title' (str), 'description' (str), and 'properties' (dict of field name
                to SchemaProperties with title, description, format).

        Example:
            ogc_collection_schema(collectionId="properties/buildings")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/schema"
            logger.debug(f"[ogc_collection_schema] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collection_schema] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection schema error: {e}")
            return self._build_error("OGC collection schema", e)

    def ogc_collection_queryables(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """This resource returns the queryable properties for a specific collection identified by its unique id. Queryable properties provide detailed metadata for each attribute available in the collection that can be used to filter queries. The response includes information such as:

- **Field Names:** The names of the attributes in the collection.
- **Descriptions:** A description of each attribute to clarify its purpose and usage.
- **Formats:** The data types or formats (e.g., string, number, geospatial) of each attribute.
- **Geospatial Data Types:** Specific spatial types for attributes that support geospatial queries.

This metadata is essential for clients to build dynamic query interfaces and validate their requests against the collection's schema.

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: QueryableResponse (JSON Schema) with keys '$schema' (str), '$id' (str),
                'type' (str), 'title' (str), 'description' (str), 'properties' (dict of queryable
                field name to PropertyInfo with title, description, format), and 'additionalProperties' (bool).

        Example:
            ogc_collection_queryables(collectionId="properties/buildings")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/queryables"
            logger.debug(f"[ogc_collection_queryables] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[ogc_collection_queryables] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection queryables error: {e}")
            return self._build_error("OGC collection queryables", e)

    def ogc_collection_items(self, collectionId: str, **kwargs) -> Dict[str, Any]:
        """Fetch features of the feature collection with id `{collectionId}`.

Every feature in a dataset belongs to a collection. A dataset may consist of multiple feature collections, each representing a group of features that share a common schema and type.

The **collection id** is a unique identifier for the spatial dataset and is used to reference a specific collection within the API.

Additional capabilities include:
- **Filtering:** Supports attribute-based filtering using CQL (Common Query Language).
- **Pagination:** Use `limit` and `offset` parameters to paginate results.
- **Spatial Queries:**
  - **Bounding Box (bbox):** Retrieve features within a rectangular spatial extent (`minX, minY, maxX, maxY`).
  - **Spatial Filters:** Support for `contains`, `intersects`, and `within` (OGC Filter Encoding).

        Args:
            collectionId (str): Unique identifier of the collection.
            **kwargs: Additional keyword arguments passed to the API.
                limit (str): Number of items to return (max: 10,000).
                offset (str): Offset for pagination.
                bbox (str): Bounding box for spatial filtering (minX, minY, maxX, maxY).
                filter (str): Filter query in CQL format.

        Returns:
            Dict[str, Any]: FeatureCollectionResponse (GeoJSON) with keys 'type' (str), 'features'
                (list of Feature objects with properties, geometry, and optional id), 'timeStamp' (str),
                and 'links' (list of Link objects for pagination).

        Example:
            ogc_collection_items(collectionId="properties/buildings", limit=100, offset=0)
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/items"
            params = {k: kwargs[k] for k in ["limit", "offset", "bbox", "filter"] if k in kwargs}
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[ogc_collection_items] GET {url}")
            logger.debug(f"[ogc_collection_items] Request params: {params}")
            response = self.session.get(url, params=params, headers=headers)
            logger.debug(f"[ogc_collection_items] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC collection items error: {e}")
            return self._build_error("OGC collection items", e)

    def ogc_feature_by_id(self, collectionId: str, featureId: str, **kwargs) -> Dict[str, Any]:
        """Retrieves a single feature in GeoJSON format,

        Args:
            collectionId (str): Unique collection identifier
            featureId (str): Unique feature identifier
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: FeatureCollectionResponse (GeoJSON) with keys 'type' (str), 'features'
                (list containing the single Feature with properties, geometry, and id), 'timeStamp' (str),
                and 'links' (list of Link objects).

        Example:
            ogc_feature_by_id(collectionId="properties/buildings", featureId="1")
        """
        try:
            url = f"{self.base_url}/v1/ogcapi/enrich/collections/{collectionId}/items/{featureId}"
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[ogc_feature_by_id] GET {url}")
            response = self.session.get(url, headers=headers)
            logger.debug(f"[ogc_feature_by_id] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"OGC feature by ID error: {e}")
            return self._build_error("OGC feature by ID", e)

    # ========================================
    # WMS (Web Map Service) APIs
    # ========================================

    def wms_get_request(self, **kwargs) -> Dict[str, Any]:
        """Processes WMS requests: GetCapabilities, GetMap, GetFeatureInfo. WMS service errors (ServiceExceptionReport) with HTTP 2xx are raised as exceptions and returned as {"error": <xml>}.

        Args:
            **kwargs: Additional keyword arguments passed to the API.
                REQUEST (str): WMS request type
                SERVICE (str): Service type
                VERSION (str): WMS version
                crs (str): crs
                srs (str): srs
                BBOX (str): BBOX
                width (str): width
                height (str): height
                layers (str): layers
                Info_Format (str): Info_Format
                QUERY_LAYERS (str): QUERY_LAYERS
                I (str): I
                J (str): J
                X (str): X
                Y (str): Y
                Feature_Count (str): Feature_Count
                PIXELSEARCHRADIUS (str): PIXELSEARCHRADIUS
                STYLES (str): STYLES
                FORMAT (str): FORMAT
                TRANSPARENT (str): TRANSPARENT
                BGCOLOR (str): BGCOLOR
                RESOLUTION (str): RESOLUTION
                EXCEPTIONS (str): EXCEPTIONS

        Returns:
            Dict[str, Any]: For GetMap success: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
                For GetCapabilities success: Dict with keys 'xml' (str), 'content_type' (str).
                For GetFeatureInfo success: JSON response dict, or Dict with keys 'xml' (str), 'content_type' (str) for XML info_format.
                On any error (HTTP 4xx/5xx or WMS ServiceException): Dict with key 'error' (str) containing the error detail or ServiceExceptionReport XML.

        Example:
            wms_get_request(REQUEST="GetCapabilities", SERVICE="WMS", VERSION="1.3.0")
        """
        try:
            url = f"{self.base_url}/v1/spatial/wms"
            params = {k: kwargs[k] for k in ["REQUEST", "SERVICE", "VERSION", "crs", "srs", "BBOX", "width", "height", "layers", "Info_Format", "QUERY_LAYERS", "I", "J", "X", "Y", "Feature_Count", "PIXELSEARCHRADIUS", "STYLES", "FORMAT", "TRANSPARENT", "BGCOLOR", "RESOLUTION", "EXCEPTIONS"] if k in kwargs}
            request_type = kwargs.get("REQUEST", "").upper()
            logger.debug(f"[wms_get_request] GET {url}")
            logger.debug(f"[wms_get_request] Request params: {params}")
            response = self.session.get(url, params=params, headers={"Accept": "*/*"})
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                logger.debug(f"[wms_get_request] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wms_get_request] Raw response: {response.text}")
            response.raise_for_status()
            if "image" not in content_type and "<ServiceException" in response.text:
                raise ValueError(response.text)
            if request_type == "GETMAP":
                if "image" in content_type:
                    return {"image_base64": base64.b64encode(response.content).decode(), "content_type": content_type, "size_bytes": len(response.content)}
                return {"xml": response.text, "content_type": content_type}
            if request_type == "GETCAPABILITIES":
                return {"xml": response.text, "content_type": content_type}
            if request_type == "GETFEATUREINFO":
                if "json" in content_type:
                    return response.json()
                return {"xml": response.text, "content_type": content_type}
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMS get request error: {e}")
            return self._build_error("WMS get request", e)

    def wms_post_get_map(self, **kwargs) -> Dict[str, Any]:
        """Processes WMS GetMap requests using a POST method. Accepts SLD_BODY as a form parameter (URL-encoded JSON). WMS service errors (ServiceExceptionReport) with HTTP 2xx are raised as exceptions and returned as {"error": <xml>}.

        Args:
            **kwargs: Additional keyword arguments passed to the API.
                REQUEST (str): WMS request type
                SERVICE (str): Service type
                VERSION (str): WMS version ('1.3.0' uses crs; '1.1.1' uses srs)
                crs (str): Coordinate reference system for WMS 1.3.0 (e.g. 'CRS:84', 'EPSG:4326', 'EPSG:3857')
                srs (str): Spatial reference system for WMS 1.1.1 (e.g. 'EPSG:4326', 'EPSG:3857')
                BBOX (str): BBOX
                width (str): width
                height (str): height
                layers (str): layers
                STYLES (str): Comma-separated list of style names, one per requested layer. MUST always be supplied. Omitting STYLES entirely causes a server-side StyleNotDefined error.
                FORMAT (str): FORMAT
                TRANSPARENT (str): TRANSPARENT
                DPI (str): DPI hint (accepted by server but silently ignored — has no effect on output).
                MAP_RESOLUTION (str): Map resolution hint (accepted by server but silently ignored — has no effect on output).
                FORMAT_OPTIONS (str): Additional format options e.g. 'dpi:96' (accepted by server but silently ignored — has no effect on output).
                SLD_BODY (str): URL-encoded JSON style definition. Use empty string ('') or omit entirely to use default server styles. NOTE: passing SLD_BODY='{}' (JSON empty object string) causes a server-side InvalidStyleDetails error — always use SLD_BODY='' or omit.

        Returns:
            Dict[str, Any]: On success: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
                On any error (HTTP 4xx/5xx or WMS ServiceException): Dict with key 'error' (str) containing the error detail or ServiceExceptionReport XML.

        Example:
            wms_post_get_map(
                REQUEST="GetMap",
                SERVICE="WMS",
                VERSION="1.3.0",
                crs="CRS:84",
                BBOX="-122.712622,38.035008,-122.692382,38.045271",
                width="640",
                height="480",
                layers="wildfire_risk",
                FORMAT="image/png",
                STYLES=""
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/wms"
            params = {k: kwargs[k] for k in ["REQUEST", "SERVICE", "VERSION", "crs", "srs", "BBOX", "width", "height", "layers", "STYLES", "FORMAT", "TRANSPARENT"] if k in kwargs}
            form_data = {}
            if "SLD_BODY" in kwargs:
                form_data["SLD_BODY"] = kwargs["SLD_BODY"]
            headers = dict(self.session.headers)
            headers.pop("Content-Type", None)
            headers["Accept"] = "image/png"
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            logger.debug(f"[wms_post_get_map] POST {url}")
            logger.debug(f"[wms_post_get_map] Request params: {params}")
            response = self.session.post(url, params=params, data=form_data, headers=headers)
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                logger.debug(f"[wms_post_get_map] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wms_post_get_map] Raw response: {response.text}")
            response.raise_for_status()
            if "image" not in content_type and "<ServiceException" in response.text:
                raise ValueError(response.text)
            if "image" in content_type:
                return {"image_base64": base64.b64encode(response.content).decode(), "content_type": content_type, "size_bytes": len(response.content)}
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMS POST GetMap error: {e}")
            return self._build_error("WMS POST GetMap", e)

    # ========================================
    # WMTS (Web Map Tile Service) APIs
    # ========================================

    def wmts_request(self, **kwargs) -> Dict[str, Any]:
        """Use the appropriate parameters based on the request type.

        Args:
            **kwargs: Additional keyword arguments passed to the API.
                Service (str): Specifies the service type (must be `WMTS`).
                Request (str): Defines the request type. Available values : GetCapabilities, GetTile
                Version (str): WMTS version.
                Layer (str): Available layer name via Data or Repository (required for `GetTile`).
                Style (str): Comma-separated list of one rendering style per requested layer(required for `GetTile`).
                TileMatrixSet (str): Tile matrix set to generate tiles for(required for `GetTile`).
                TileMatrix (str): An integer value which will be number of levels or zoom level(required for `GetTile`).
                TileRow (int): An integer value that specifies the row number of the tile you want (required for `GetTile`).
                TileCol (int): An integer value that specifies the column number of the tile you want (required for `GetTile`).
                Format (str): The format in which the map image is to be returned(required for `GetTile`).

        Returns:
            Dict[str, Any]: For GetTile: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
                For GetCapabilities: Dict with keys 'xml' (str), 'content_type' (str).

        Example:
            wmts_request(Service="WMTS", Request="GetCapabilities")
        """
        try:
            url = f"{self.base_url}/v1/spatial/wmts"
            params = {k: kwargs[k] for k in ["Service", "Request", "Version", "Layer", "Style", "TileMatrixSet", "TileMatrix", "TileRow", "TileCol", "Format"] if k in kwargs}
            logger.debug(f"[wmts_request] GET {url}")
            logger.debug(f"[wmts_request] Request params: {params}")
            response = self.session.get(url, params=params)
            content_type = response.headers.get("Content-Type", "")
            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                logger.debug(f"[wmts_request] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wmts_request] Raw response: {response.text}")
            response.raise_for_status()
            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                return {"image_base64": base64.b64encode(response.content).decode(), "content_type": content_type, "size_bytes": len(response.content)}
            if "xml" in content_type.lower() or kwargs.get("Request", "").upper() == "GETCAPABILITIES":
                return {"xml": response.text, "content_type": content_type or "application/xml"}
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMTS request error: {e}")
            return self._build_error("WMTS request", e)

    def wmts_get_standard_tile(self, Version: str, Layer: str, Style: str, TileMatrixSet: str, TileMatrix: str, TileCol: int, TileRow: int, Format: str, **kwargs) -> Dict[str, Any]:
        """Returns a map tile based on the RESTful encoding for the WMTS service.


        Args:
            Version (str): WMTS version (default is `1.0.0`).
            Layer (str): Available layer name via Data or Repository.
            Style (str): Comma-separated list of one rendering style per requested layer.
            TileMatrixSet (str): Tile matrix set to generate tiles for.
            TileMatrix (str): Level of detail (zoom level).
            TileCol (int): An integer value that specifies the column number of the tile you want.
            TileRow (int): An integer value that specifies the row number of the tile you want.
            Format (str): Image format extension.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

        Example:
            wmts_get_standard_tile(
                Version="1.0.0",
                Layer="parcels",
                Style="default",
                TileMatrixSet="WorldWebMercatorQuad_0_to_19",
                TileMatrix="17",
                TileCol=31118,
                TileRow=50069,
                Format="png"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/wmts/{Version}/default/tiles/{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.{Format}"
            logger.debug(f"[wmts_get_standard_tile] GET {url}")
            response = self.session.get(url)
            content_type = response.headers.get("Content-Type", "")
            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                logger.debug(f"[wmts_get_standard_tile] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wmts_get_standard_tile] Raw response: {response.text}")
            response.raise_for_status()
            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                return {"image_base64": base64.b64encode(response.content).decode(), "content_type": content_type, "size_bytes": len(response.content)}
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMTS get standard tile error: {e}")
            return self._build_error("WMTS get standard tile", e)

    def wmts_get_simple_tile(self, Version: str, Layer: str, TileMatrix: str, TileCol: int, TileRow: int, Format: str, **kwargs) -> Dict[str, Any]:
        """Returns a map tile based on the RESTful encoding for the WMTS service.

        Args:
            Version (str): WMTS version (default is `1.0.0`).
            Layer (str): Available layer name via Data or Repository.
            TileMatrix (str): Level of detail (zoom level).
            TileCol (int): An integer value that specifies the column number of the tile you want.
            TileRow (int): An integer value that specifies the row number of the tile you want.
            Format (str): Image format extension.
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).

        Example:
            wmts_get_simple_tile(
                Version="1.0.0",
                Layer="parcels",
                TileMatrix="17",
                TileCol=31118,
                TileRow=50069,
                Format="png"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/wmts/{Version}/simpleProfileTile/tiles/{Layer}/{TileMatrix}/{TileCol}/{TileRow}.{Format}"
            logger.debug(f"[wmts_get_simple_tile] GET {url}")
            response = self.session.get(url)
            content_type = response.headers.get("Content-Type", "")
            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                logger.debug(f"[wmts_get_simple_tile] Raw response: binary {len(response.content)} bytes, {content_type}")
            else:
                logger.debug(f"[wmts_get_simple_tile] Raw response: {response.text}")
            response.raise_for_status()
            if "image/" in content_type.lower() or "application/vnd.mapbox-vector-tile" in content_type.lower():
                return {"image_base64": base64.b64encode(response.content).decode(), "content_type": content_type, "size_bytes": len(response.content)}
            return {"error": f"Unexpected response, content_type: {content_type} Check logs in DEBUG mode for more details"}
        except Exception as e:
            logger.error(f"WMTS get simple tile error: {e}")
            return self._build_error("WMTS get simple tile", e)
