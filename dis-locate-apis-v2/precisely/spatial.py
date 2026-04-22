"""Spatial analysis API methods (7 tools)."""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class SpatialMixin:
    def find_nearest_candidates(self, tableName: str, attributes: list, location: dict, withinDistance: str, **kwargs) -> Dict[str, Any]:
        """Identifies the nearest locations or points of interest to a specified geometry or address based on distance or defined criteria, returning the spatial features in distance order with the distance value.

        Args:
            tableName (str): Name of the table containing the spatial data.
            attributes (list): Comma separated list of column names of enrich table to be included in the response. "*" can be used to specify all columns.
            location (dict): input for which spatial analysis is to be done. Can be a geometry or address
            withinDistance (str): The distance to search around the geometry.
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                distanceAttributeName (str): The name of the distance attribute between input geometry and target geometry. Default value is "distance".
                maxFeatures (int): Maximum number of features returned against each geometry. Default value is 10 and minimum value is 1.
                uomAttributeName (str): Custom name of parameter showing unit of measurement for distance between input and target geometry. Default value is "uom".
                inputPointAttributeName (str): Custom name of parameter indicating point on input geometry which was used to calculate the distance. Default value is "inputPoint".
                targetPointAttributeName (str): Custom name of parameter indicating point on target geometry which was used to calculate the distance. Default value is "targetPoint".
                bearingAttributeName (str): Custom name of parameter for bearing value. Default value is "bearing".
                sortBy (str): Defines the attribute by which the results should be sorted.
                sortOrder (str): Specifies the order of sorting.
                limit (int): Specifies the maximum number of results to return.
                offset (int): Specifies the number of records to skip.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with properties and geometry), 'responseParameters' (dict with recordsMatched, recordsReturned),
                and 'Metadata' (list of attribute definitions with name and type).

        Example:
            find_nearest_candidates(
                tableName="/risks/flood_risk",
                attributes=["statecode", "type", "mapname"],
                location={"format": "WKT", "value": "MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211)))"},
                withinDistance="10 mi",
                attributeFilter="id > 100",
                distanceAttributeName="dist",
                maxFeatures=2,
                uomAttributeName="unit",
                inputPointAttributeName="ip",
                targetPointAttributeName="tp",
                bearingAttributeName="bearingAngle"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/findNearest"
            params = {p: kwargs[p] for p in ["sortBy", "sortOrder", "limit", "offset"] if p in kwargs}
            json_data = {"tableName": tableName, "attributes": attributes, "location": location, "withinDistance": withinDistance}
            for k in ["attributeFilter", "distanceAttributeName", "maxFeatures", "uomAttributeName", "inputPointAttributeName", "targetPointAttributeName", "bearingAttributeName"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[find_nearest_candidates] POST {url}")
            logger.debug(f"[find_nearest_candidates] Request params: {params}")
            logger.debug(f"[find_nearest_candidates] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, params=params, headers=headers)
            logger.debug(f"[find_nearest_candidates] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Find nearest candidates error: {e}")
            return self._build_error("Find nearest candidates", e)

    def search_at_location(self, tableName: str, attributes: list, location: dict, **kwargs) -> Dict[str, Any]:
        """Searches for locations or points of interest within or intersecting a defined geographic area(geometry or address) or a buffer around a specified location.

        Args:
            tableName (str): Name of the table containing the spatial data.
            attributes (list): Comma separated list of column names of enrich table to be included in the response. "*" can be used to specify all columns.
            location (dict): input for which spatial analysis is to be done. Can be a geometry or address
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                spatialOperation (str): The type of spatial query. Possible values are: intersects, within, contains. Default value is "intersects".
                bufferDistance (str): Distance by which the input geometry will be extrapolated.
                sortBy (str): Defines the attribute by which the results should be sorted.
                sortOrder (str): Specifies the order of sorting.
                limit (int): Specifies the maximum number of results to return.
                offset (int): Specifies the number of records to skip.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with properties and geometry), 'responseParameters' (dict with recordsMatched, recordsReturned),
                and 'Metadata' (list of attribute definitions with name and type).

        Example:
            search_at_location(
                tableName="/risks/flood_risk",
                attributes=["statecode", "type", "mapname"],
                location={"format": "WKT", "value": "MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211)))"},
                spatialOperation="INTERSECTS",
                attributeFilter="id > 100",
                bufferDistance="10 mi"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/searchAtLocation"
            params = {p: kwargs[p] for p in ["sortBy", "sortOrder", "limit", "offset"] if p in kwargs}
            json_data = {"tableName": tableName, "attributes": attributes, "location": location}
            for k in ["attributeFilter", "spatialOperation", "bufferDistance"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[search_at_location] POST {url}")
            logger.debug(f"[search_at_location] Request params: {params}")
            logger.debug(f"[search_at_location] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, params=params, headers=headers)
            logger.debug(f"[search_at_location] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Search at location error: {e}")
            return self._build_error("Search at location", e)

    def overlap(self, tableName: str, attributes: list, location: dict, uom: str, **kwargs) -> Dict[str, Any]:
        """Identifies spatial intersections between a specified geometry or address in a chosen Enrich spatial table returning the overlap geometry with the percentage and area of overlap.

        Args:
            tableName (str): Name of the table containing the spatial data.
            attributes (list): Comma separated list of column names of enrich table to be included in the response. "*" can be used to specify all columns, will only include scalar columns
            location (dict): input for which spatial analysis is to be done. Can be a geometry or address
            uom (str): Unit of measurement used to return intersection length/area
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                areaAttributeName (str): Custom name of intersection area parameter when intersection area is polygon. Default value is "intersectionArea".
                lengthAttributeName (str): Custom name of intersection length parameter when intersection area is linestring. Default value is "intersectionLength".
                percentTargetAttributeName (str): Custom name of parameter indicating percentage of overlap with target geometry. Default value is "percentageOfTarget".
                percentInputAttributeName (str): Custom name of parameter indicating percentage of overlap with input geometry. Default value is "percentageOfInput".
                uomAttributeName (str): Custom name of unit of measurement parameter. Default value is "uom".
                bufferDistance (str): Distance by which the input geometry will be extrapolated.
                limit (int): Specifies the maximum number of results to return.
                offset (int): Specifies the number of records to skip.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with properties including overlap area/length/percentage and geometry), 'responseParameters'
                (dict with recordsMatched, recordsReturned), and 'Metadata' (list of attribute definitions).

        Example:
            overlap(
                tableName="/properties/buildings",
                location={"format": "WKT", "value": "POLYGON ((-74.01316 40.700479, -74.012028 40.700479, -74.012028 40.701403, -74.01316 40.701403, -74.01316 40.700479))"},
                attributes=["fips"],
                uom="m",
                attributeFilter="elevation > 0",
                areaAttributeName="overlappedArea",
                lengthAttributeName="overlappedLength",
                percentTargetAttributeName="targetOverlapPercentage",
                percentInputAttributeName="inputOverlapPercentage",
                uomAttributeName="measurementUnit",
                bufferDistance="2 km"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/overlap"
            params = {p: kwargs[p] for p in ["limit", "offset"] if p in kwargs}
            json_data = {"tableName": tableName, "attributes": attributes, "location": location, "uom": uom}
            for k in ["attributeFilter", "areaAttributeName", "lengthAttributeName", "percentTargetAttributeName", "percentInputAttributeName", "uomAttributeName", "bufferDistance"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[overlap] POST {url}")
            logger.debug(f"[overlap] Request params: {params}")
            logger.debug(f"[overlap] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, params=params, headers=headers)
            logger.debug(f"[overlap] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Overlap error: {e}")
            return self._build_error("Overlap", e)

    def get_spatial_products(self, **kwargs) -> Dict[str, Any]:
        """Get a list of available Enrich Data products along with their metadata such as product family, applicable geographic area, vintage, available layers, appropriate zoom levels for display and styles to use.

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: List of product metadata objects, each with keys 'productId' (str), 'productName' (str),
                'productFamily' (str), 'vintage' (str), 'geography' (str), and 'layers' (list of layer objects
                with layerId, displayName, featureTable, recommendedStyle, etc.).

        Example:
            get_spatial_products()
        """
        try:
            url = f"{self.base_url}/v1/spatial/products"
            logger.debug(f"[get_spatial_products] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[get_spatial_products] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Get spatial products error: {e}")
            return self._build_error("Get spatial products", e)

    def list_spatial_tables(self, **kwargs) -> Dict[str, Any]:
        """This endpoint retrieves a list of spatial tables from database

        Args:
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: List of table name strings (e.g., ["/properties/buildings", "/risks/flood_risk", ...]).

        Example:
            list_spatial_tables()
        """
        try:
            url = f"{self.base_url}/v1/spatial/tables"
            logger.debug(f"[list_spatial_tables] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[list_spatial_tables] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"List spatial tables error: {e}")
            return self._build_error("List spatial tables", e)

    def get_table_metadata(self, tableName: str, **kwargs) -> Dict[str, Any]:
        """This endpoint retrieves a metadata information of a specific/given table from database

        Args:
            tableName (str): Name of table for which metadata request will be executed
            **kwargs: Additional keyword arguments passed to the API.

        Returns:
            Dict[str, Any]: Table metadata object with keys 'tableName' (str), 'geometryType' (str),
                'numberOfRows' (int), 'columns' (list of ColumnDetail objects with columnName, description,
                dataType), 'xMin' (float), 'xMax' (float), 'yMin' (float), 'yMax' (float).

        Example:
            get_table_metadata(tableName="risks/flood_risk")
        """
        try:
            table_path = tableName.lstrip("/")
            url = f"{self.base_url}/v1/spatial/tables/{table_path}/metadata"
            logger.debug(f"[get_table_metadata] GET {url}")
            response = self.session.get(url)
            logger.debug(f"[get_table_metadata] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Get table metadata error: {e}")
            return self._build_error("Get table metadata", e)

    def summarize(self, tableName: str, location: Dict, aggregateColumns: Dict, **kwargs) -> Dict[str, Any]:
        """Generates detailed data summaries within a user defined region(geometry or address), including total, average, minimum and maximum values for data such as population.

        Args:
            tableName (str): Name of the table containing the spatial data.
            location (dict): Input for which spatial analysis is to be done. Can be a geometry or address.
            aggregateColumns (dict): Columns to be aggregated and corresponding aggregation operations to be performed. Possible values are: min, max, avg, sum, median.
            **kwargs: Additional keyword arguments passed to the API.
                attributeFilter (str): specifies filter on scalar attributes
                spatialOperation (str): The type of spatial operation. Possible values are: intersects, within. Default value is "intersects".
                proportionalCalculation (bool): Determines if proportional calculations should be applied. Only applicable where the spatialOperation parameter is "intersects".
                bufferDistance (str): Distance by which the input geometry will be extrapolated.

        Returns:
            Dict[str, Any]: GeoJSON FeatureCollection with keys 'type' (str), 'features' (list of Feature objects
                with aggregated summary properties such as column_MIN, column_MAX, column_AVG, column_SUM,
                column_MEDIAN, and count).

        Example:
            summarize(
                tableName="/risks/historical_weather_windgrid",
                aggregateColumns={"w11": ["min", "max", "avg", "sum"], "w10": ["min", "max", "sum", "avg", "median"]},
                location={"format": "WKT", "value": "GEOMETRYCOLLECTION (MULTIPOLYGON (((-122.399306 37.712211, -122.398975 37.712132, -122.399007 37.712049, -122.399338 37.712127, -122.399316 37.712185, -122.399306 37.712211))), LINESTRING (-121.756899 37.653383, -121.158302 37.304645, -121.690998 37.120906))"},
                spatialOperation="intersects",
                attributeFilter="grid_id > 0",
                proportionalCalculation=True,
                bufferDistance="10 mi"
            )
        """
        try:
            url = f"{self.base_url}/v1/spatial/summarize"
            json_data = {"tableName": tableName, "location": location, "aggregateColumns": aggregateColumns}
            for k in ["attributeFilter", "spatialOperation", "proportionalCalculation", "bufferDistance"]:
                if k in kwargs:
                    json_data[k] = kwargs[k]
            headers = {"Accept": "application/geo+json"}
            logger.debug(f"[summarize] POST {url}")
            logger.debug(f"[summarize] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data, headers=headers)
            logger.debug(f"[summarize] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Summarize error: {e}")
            return self._build_error("Summarize", e)
