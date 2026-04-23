"""
Output schemas for all 68 MCP tools.
Each schema describes the JSON structure returned by the tool on success.
Used as `outputSchema` on Tool definitions per MCP spec 2025-11-25.
"""

# ============================================================
# Geocoding & Address (9 tools)
# ============================================================

# geocode, reverse_geocode, verify_address
GEOCODE_RESPONSE = {
    "type": "object",
    "properties": {
        "responses": {
            "type": "array",
            "description": "Array of geocode result objects, one per input address.",
            "items": {
                "type": "object",
                "properties": {
                    "addressId": {"type": "string", "description": "Client-supplied address identifier for correlation."},
                    "status": {"type": "string", "description": "Result status (e.g., 'OK', 'ZERO_RESULTS')."},
                    "results": {
                        "type": "array",
                        "description": "Ranked list of candidate matches.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "score": {"type": "number", "description": "Match confidence score."},
                                "address": {"type": "object", "description": "Parsed address components."},
                                "addressLines": {"type": "array", "items": {"type": "string"}, "description": "Formatted address lines."},
                                "location": {"type": "object", "description": "Geographic coordinates and metadata."},
                                "explanation": {"type": "object", "description": "Match explanation with source and match details."},
                                "customFields": {"type": "object", "description": "Additional precision and metadata fields."}
                            }
                        }
                    }
                },
                "required": ["status"]
            }
        }
    },
    "required": ["responses"]
}

# autocomplete, autocomplete_postal_city
AUTOCOMPLETE_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Result status (e.g., 'OK')."},
                "predictions": {
                    "type": "array",
                    "description": "List of autocomplete prediction results.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "prediction": {"type": "string", "description": "Full predicted address string."},
                            "address": {"type": "object", "description": "Parsed address components."},
                            "addressLines": {"type": "array", "items": {"type": "string"}, "description": "Formatted address lines."},
                            "location": {"type": "object", "description": "Geographic coordinates."}
                        }
                    }
                }
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# autocomplete_v2
AUTOCOMPLETE_V2_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Result status."},
                "predictions": {
                    "type": "array",
                    "description": "List of autocomplete prediction results with explanation.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "prediction": {"type": "string", "description": "Full predicted address string."},
                            "address": {"type": "object", "description": "Parsed address components."},
                            "addressLines": {"type": "array", "items": {"type": "string"}},
                            "location": {"type": "object", "description": "Geographic coordinates."},
                            "explanation": {"type": "object", "description": "Match explanation including source."}
                        }
                    }
                }
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# lookup
LOOKUP_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Result status."},
                "prediction": {"type": "string", "description": "Full predicted address."},
                "address": {"type": "object", "description": "Parsed address components."},
                "addressLines": {"type": "array", "items": {"type": "string"}},
                "location": {"type": "object", "description": "Geographic coordinates."}
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# parse_address, parse_address_batch
PARSE_ADDRESS_RESPONSE = {
    "type": "object",
    "properties": {
        "responses": {
            "type": "array",
            "description": "Array of parsed address results.",
            "items": {
                "type": "object",
                "properties": {
                    "addressId": {"type": "string"},
                    "status": {"type": "string"},
                    "addressLine1": {"type": "string"},
                    "addressLine2": {"type": "string"},
                    "city": {"type": "string"},
                    "stateProvince": {"type": "string"},
                    "postalCode": {"type": "string"},
                    "country": {"type": "string"},
                    "firmName": {"type": "string"}
                },
                "required": ["status"]
            }
        }
    },
    "required": ["responses"]
}

# ============================================================
# Geolocation (2 tools)
# ============================================================

# geo_locate_ip_address
GEO_LOCATE_IP_RESPONSE = {
    "type": "object",
    "properties": {
        "ipAddress": {"type": "string", "description": "The resolved IP address."},
        "location": {
            "type": "object",
            "description": "Geographic location of the IP address.",
            "properties": {
                "country": {"type": "string"},
                "state": {"type": "string"},
                "city": {"type": "string"},
                "postalCode": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "areaCode": {"type": "string"},
                "timeZone": {"type": "string"}
            }
        },
        "network": {"type": "object", "description": "Network information for the IP."},
        "confidence": {"type": "object", "description": "Location confidence scores."}
    }
}

# geo_locate_wifi_access_point
GEO_LOCATE_WIFI_RESPONSE = {
    "type": "object",
    "properties": {
        "accessPoints": {"type": "array", "description": "Input access point data."},
        "location": {
            "type": "object",
            "description": "Estimated location from WiFi signals.",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "accuracy": {"type": "number"}
            }
        }
    }
}

# ============================================================
# Verification (5 tools)
# ============================================================

# verify_email
VERIFY_EMAIL_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "email": {
                    "type": "object",
                    "description": "Email verification result.",
                    "properties": {
                        "address": {"type": "string", "description": "The email address verified."},
                        "result": {"type": "string", "description": "Verification result (e.g., 'valid', 'invalid')."},
                        "subResult": {"type": "string", "description": "Detailed sub-result (e.g., 'failed_syntax_check')."},
                        "freeEmail": {"type": "string"},
                        "mxFound": {"type": "string"},
                        "processedAt": {"type": "string"}
                    }
                }
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# verify_batch_emails
VERIFY_BATCH_EMAILS_RESPONSE = {
    "type": "object",
    "properties": {
        "responses": {
            "type": "array",
            "description": "Array of email verification results.",
            "items": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "id": {"type": "string"},
                    "email": {"type": "object", "description": "Email verification result."}
                },
                "required": ["status"]
            }
        }
    },
    "required": ["responses"]
}

# parse_name
PARSE_NAME_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "middleName": {"type": "string"},
                "prefix": {"type": "string"},
                "suffix": {"type": "string"},
                "fullName": {"type": "string"}
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# validate_phone
VALIDATE_PHONE_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "phoneNumber": {
                    "type": "object",
                    "description": "Phone validation result.",
                    "properties": {
                        "formattedPhoneNumber": {"type": "string"},
                        "validStatus": {"type": "boolean"},
                        "validationDescription": {"type": "string"},
                        "numberType": {"type": "string"},
                        "countryCode": {"type": "string"},
                        "carrier": {"type": "string"}
                    }
                }
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# validate_batch_phones
VALIDATE_BATCH_PHONES_RESPONSE = {
    "type": "object",
    "properties": {
        "responses": {
            "type": "array",
            "description": "Array of phone validation results.",
            "items": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "id": {"type": "string"},
                    "phoneNumber": {"type": "object", "description": "Phone validation result."}
                },
                "required": ["status"]
            }
        }
    },
    "required": ["responses"]
}

# ============================================================
# Timezone (2 tools)
# ============================================================

TIMEZONE_RESPONSE = {
    "type": "object",
    "properties": {
        "responses": {
            "type": "array",
            "description": "Array of timezone results, one per input.",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Client-supplied identifier for correlation."},
                    "status": {"type": "string"},
                    "timezone": {
                        "type": "object",
                        "properties": {
                            "timezoneName": {"type": "string", "description": "IANA timezone name (e.g., 'America/Chicago')."},
                            "zoneType": {"type": "string"},
                            "dstOffset": {"type": "object", "description": "DST offset hours/minutes."},
                            "timestamp": {"type": "object"},
                            "utcOffset": {"type": "object", "description": "UTC offset hours/minutes."}
                        }
                    }
                },
                "required": ["status"]
            }
        }
    },
    "required": ["responses"]
}

# ============================================================
# Tax & Emergency (6 tools)
# ============================================================

# lookup_tax_jurisdiction (single returns response, batch returns responses)
TAX_JURISDICTION_RESPONSE = {
    "type": "object",
    "description": "Single record returns 'response', multiple records return 'responses' array.",
    "properties": {
        "response": {
            "type": "object",
            "description": "Single tax jurisdiction result.",
            "properties": {
                "status": {"type": "string"},
                "result": {
                    "type": "object",
                    "properties": {
                        "jurisdiction": {"type": "array", "description": "List of jurisdiction codes and names."},
                        "matchedAddress": {"type": "object"},
                        "census": {"type": "object"},
                        "latLongFields": {"type": "object"}
                    }
                }
            }
        },
        "responses": {
            "type": "array",
            "description": "Batch tax jurisdiction results.",
            "items": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "result": {"type": "object"}
                }
            }
        }
    }
}

# psap_address, psap_location
PSAP_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "psap": {
                    "type": "object",
                    "description": "PSAP (Public Safety Answering Point) information.",
                    "properties": {
                        "psapId": {"type": "string"},
                        "fccId": {"type": "string"},
                        "type": {"type": "string"},
                        "agency": {"type": "string"},
                        "phone": {"type": "string"},
                        "county": {"type": "string"},
                        "contactPerson": {"type": "string"},
                        "siteDetails": {"type": "object"},
                        "mailingAddress": {"type": "object"}
                    }
                }
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# psap_ahj_address, psap_ahj_location, psap_ahj_fccid
PSAP_AHJ_RESPONSE = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "psap": {"type": "object", "description": "PSAP information."},
                "ahjs": {
                    "type": "array",
                    "description": "Authorities Having Jurisdiction associated with this PSAP.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "ahjType": {"type": "string"},
                            "ahjId": {"type": "string"},
                            "name": {"type": "string"},
                            "fipsCode": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["status"]
        }
    },
    "required": ["response"]
}

# ============================================================
# GraphQL (22 tools)
# ============================================================

# Generic GraphQL response wrapper — all GraphQL tools return this top-level structure.
# The nested contents vary per tool but all share the data.getByAddress pattern.
def _graphql_schema(inner_description: str, inner_fields: dict) -> dict:
    """Build a GraphQL outputSchema with the standard wrapper."""
    return {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "getByAddress": {
                        "type": "object",
                        "description": inner_description,
                        "properties": inner_fields
                    }
                }
            }
        },
        "required": ["data"]
    }

_DATA_BLOCK = {
    "type": "object",
    "description": "Data block with metadata and data array.",
    "properties": {
        "metadata": {"type": "object", "description": "Source, vintage, and field metadata."},
        "data": {"type": "array", "description": "Array of data records."}
    }
}

# Property & Risk tools
GET_PROPERTY_DATA = _graphql_schema("Property data bundle.", {
    "addresses": _DATA_BLOCK,
    "propertyAttributes": _DATA_BLOCK,
    "buildings": _DATA_BLOCK
})

GET_PROPERTY_ATTRIBUTES = _graphql_schema("Property attributes.", {
    "propertyAttributes": _DATA_BLOCK
})

GET_REPLACEMENT_COST = _graphql_schema("Replacement cost estimate.", {
    "replacementCost": _DATA_BLOCK
})

GET_FLOOD_RISK = _graphql_schema("Flood risk assessment.", {
    "floodRisk": _DATA_BLOCK
})

GET_WILDFIRE_RISK = _graphql_schema("Wildfire risk assessment.", {
    "wildfireRisk": _DATA_BLOCK
})

GET_PROPERTY_FIRE_RISK = _graphql_schema("Property fire risk.", {
    "propertyFireRisk": _DATA_BLOCK
})

GET_EARTH_RISK = _graphql_schema("Earthquake risk.", {
    "earthRisk": _DATA_BLOCK
})

GET_COASTAL_RISK = _graphql_schema("Coastal risk.", {
    "coastalRisk": _DATA_BLOCK
})

GET_HISTORICAL_WEATHER_RISK = _graphql_schema("Historical weather risk.", {
    "historicalWeatherRisk": _DATA_BLOCK
})

# Demographics tools
GET_DEMOGRAPHICS = _graphql_schema("Demographic data.", {
    "addresses": _DATA_BLOCK,
    "psyteGeodemographics": _DATA_BLOCK,
    "groundView": _DATA_BLOCK
})

GET_CRIME_INDEX = _graphql_schema("Crime index data.", {
    "crimeIndex": _DATA_BLOCK
})

GET_PSYTE = _graphql_schema("PSYTE geodemographic segmentation.", {
    "psyteGeodemographics": _DATA_BLOCK
})

GET_GROUND_VIEW = _graphql_schema("Ground-level neighborhood view.", {
    "groundView": _DATA_BLOCK
})

GET_NEIGHBORHOODS = _graphql_schema("Neighborhood boundaries and data.", {
    "neighborhoods": _DATA_BLOCK
})

GET_SCHOOLS = _graphql_schema("School data.", {
    "schools": _DATA_BLOCK
})

GET_BUILDINGS = _graphql_schema("Building footprint data.", {
    "buildings": _DATA_BLOCK
})

GET_PARCELS = _graphql_schema("Parcel boundary data.", {
    "parcels": _DATA_BLOCK
})

# Advanced GraphQL tools
GET_ADDRESSES_DETAILED = _graphql_schema("Detailed address data.", {
    "addresses": _DATA_BLOCK
})

GET_PARCEL_BY_OWNER = _graphql_schema("Parcel data by owner name.", {
    "parcels": _DATA_BLOCK
})

GET_ADDRESS_FAMILY = _graphql_schema("Related addresses at the same location.", {
    "addressFamily": _DATA_BLOCK
})

GET_SERVICEABILITY = _graphql_schema("Serviceability data.", {
    "serviceability": _DATA_BLOCK
})

GET_PLACES = _graphql_schema("Points of interest near the address.", {
    "places": _DATA_BLOCK
})

# ============================================================
# Spatial Analysis (7 tools)
# ============================================================

# GeoJSON FeatureCollection for find_nearest_candidates, search_at_location, overlap, summarize
GEOJSON_FEATURE_COLLECTION = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "const": "FeatureCollection"},
        "features": {
            "type": "array",
            "description": "Array of GeoJSON Feature objects.",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "const": "Feature"},
                    "properties": {"type": "object", "description": "Feature attributes."},
                    "geometry": {"type": "object", "description": "GeoJSON geometry (Point, Polygon, MultiPolygon, etc.)."},
                    "id": {}
                }
            }
        },
        "responseParameters": {
            "type": "object",
            "description": "Query metadata (recordsReturned, recordsMatched, etc.)."
        },
        "Metadata": {
            "type": "array",
            "description": "Field metadata with name, type, and description."
        }
    },
    "required": ["type", "features"]
}

# get_spatial_products
SPATIAL_PRODUCTS_RESPONSE = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "description": "List of spatial data products/layers with metadata.",
            "items": {
                "type": "object",
                "properties": {
                    "productId": {"type": "string", "description": "Unique product identifier."},
                    "productName": {"type": "string", "description": "Display name of the product."},
                    "productFamily": {"type": "string", "description": "Product family (e.g., 'Risks', 'Properties')."},
                    "vintage": {"type": "string", "description": "Data vintage (e.g., '2025.12')."},
                    "geography": {"type": "string", "description": "Geographic coverage (e.g., 'PGC_USA')."},
                    "layers": {
                        "type": "array",
                        "description": "Available layers within this product.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "layerId": {"type": "string"},
                                "displayName": {"type": "string"},
                                "featureTable": {"type": "string"},
                                "numberOfRows": {"type": "integer"},
                                "recommendedDisplayMinZoom": {"type": "integer"},
                                "recommendedDisplayMaxZoom": {"type": "integer"},
                                "recommendedStyle": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    },
    "required": ["products"]
}

# list_spatial_tables
SPATIAL_TABLES_RESPONSE = {
    "type": "object",
    "properties": {
        "tables": {
            "type": "array",
            "description": "List of available spatial table names.",
            "items": {"type": "string"}
        }
    },
    "required": ["tables"]
}

# get_table_metadata
TABLE_METADATA_RESPONSE = {
    "type": "object",
    "properties": {
        "tableName": {"type": "string", "description": "Fully-qualified table name."},
        "geometryType": {"type": "string", "description": "Geometry type (e.g., 'polygon', 'point')."},
        "numberOfRows": {"type": "integer", "description": "Total row count in the table."},
        "columns": {
            "type": "array",
            "description": "Column definitions for the table.",
            "items": {
                "type": "object",
                "properties": {
                    "columnName": {"type": "string"},
                    "description": {"type": "string"},
                    "dataType": {"type": "string", "description": "Data type (e.g., 'STRING', 'INTEGER', 'LONG_INTEGER', 'FEATURE_GEOMETRY')."},
                    "queryable": {"type": "boolean", "description": "Whether filters can be applied on this column."}
                }
            }
        },
        "xMin": {"type": "number", "description": "Bounding box minimum X (longitude)."},
        "xMax": {"type": "number", "description": "Bounding box maximum X (longitude)."},
        "yMin": {"type": "number", "description": "Bounding box minimum Y (latitude)."},
        "yMax": {"type": "number", "description": "Bounding box maximum Y (latitude)."}
    },
    "required": ["tableName", "columns"]
}

# ============================================================
# OGC Features (10 tools)
# ============================================================

OGC_LANDING_PAGE = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "links": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "href": {"type": "string"},
                    "rel": {"type": "string"},
                    "type": {"type": "string"},
                    "title": {"type": "string"}
                }
            }
        }
    }
}

OGC_API_DEFINITION = {
    "type": "object",
    "description": "Full OpenAPI 3.0.1 specification.",
    "properties": {
        "openapi": {"type": "string"},
        "info": {"type": "object"},
        "servers": {"type": "array"},
        "paths": {"type": "object"},
        "components": {"type": "object"}
    }
}

OGC_FUNCTIONS = {
    "type": "object",
    "properties": {
        "functions": {
            "type": "array",
            "description": "Available spatial functions.",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Function name (e.g., 's_within', 's_contains', 's_intersects')."},
                    "arguments": {"type": "array"},
                    "returns": {"type": "array"}
                }
            }
        }
    }
}

OGC_CONFORMANCE = {
    "type": "object",
    "properties": {
        "conformsTo": {
            "type": "array",
            "description": "List of OGC conformance class URIs.",
            "items": {"type": "string"}
        }
    },
    "required": ["conformsTo"]
}

OGC_COLLECTIONS = {
    "type": "object",
    "properties": {
        "collections": {
            "type": "array",
            "description": "List of available feature collections.",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "itemType": {"type": "string"},
                    "links": {"type": "array"}
                }
            }
        },
        "links": {"type": "array"}
    }
}

OGC_COLLECTION = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "Collection identifier."},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "itemType": {"type": "string"},
        "links": {"type": "array"}
    }
}

OGC_COLLECTION_SCHEMA = {
    "type": "object",
    "description": "JSON Schema for the collection's feature properties.",
    "properties": {
        "$schema": {"type": "string", "description": "JSON Schema version URI."},
        "$id": {"type": "string", "description": "Schema endpoint URI."},
        "type": {"type": "string"},
        "title": {"type": "string", "description": "Collection name."},
        "description": {"type": "string", "description": "Collection description."},
        "properties": {"type": "object", "description": "Field definitions with name, type, description."}
    }
}

OGC_COLLECTION_QUERYABLES = {
    "type": "object",
    "description": "Queryable properties for CQL filtering.",
    "properties": {
        "$schema": {"type": "string", "description": "JSON Schema version URI."},
        "$id": {"type": "string", "description": "Queryables endpoint URI."},
        "type": {"type": "string"},
        "title": {"type": "string", "description": "Collection name."},
        "description": {"type": "string", "description": "Collection description."},
        "properties": {"type": "object", "description": "Queryable field definitions."},
        "additionalProperties": {"type": "boolean", "description": "Whether unlisted properties are allowed."}
    }
}

# ogc_collection_items, ogc_feature_by_id
OGC_FEATURE_COLLECTION = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "const": "FeatureCollection"},
        "features": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "const": "Feature"},
                    "id": {},
                    "properties": {"type": "object"},
                    "geometry": {"type": "object"}
                }
            }
        },
        "timeStamp": {"type": "string", "description": "ISO 8601 timestamp of the response."},
        "links": {"type": "array", "description": "Pagination and navigation links."}
    },
    "required": ["type", "features"]
}

# ============================================================
# WMS (2 tools)
# ============================================================

_IMAGE_RESULT = {
    "type": "object",
    "description": "Map image result.",
    "properties": {
        "image_base64": {"type": "string", "description": "Base64-encoded image data."},
        "content_type": {"type": "string", "description": "MIME type (e.g., 'image/png')."},
        "size_bytes": {"type": "integer", "description": "Image size in bytes."}
    },
    "required": ["image_base64", "content_type", "size_bytes"]
}

# wms_get_request — multi-response: GetMap→image, GetCapabilities→xml, GetFeatureInfo→json/xml
WMS_GET_REQUEST = {
    "type": "object",
    "description": "Response varies by REQUEST type: GetMap returns image, GetCapabilities returns XML, GetFeatureInfo returns JSON or XML.",
    "properties": {
        "image_base64": {"type": "string", "description": "Base64-encoded map image (GetMap)."},
        "content_type": {"type": "string", "description": "MIME type of the response."},
        "size_bytes": {"type": "integer", "description": "Image size in bytes (GetMap)."},
        "xml": {"type": "string", "description": "XML document content (GetCapabilities/GetFeatureInfo XML)."},
        "type": {"type": "string", "description": "GeoJSON type (GetFeatureInfo JSON)."},
        "features": {"type": "array", "description": "GeoJSON features (GetFeatureInfo JSON)."}
    }
}

# wms_post_get_map — always returns image
WMS_POST_GET_MAP = _IMAGE_RESULT

# ============================================================
# WMTS (3 tools)
# ============================================================

# wmts_request — multi-response: GetTile→image, GetCapabilities→xml
WMTS_REQUEST = {
    "type": "object",
    "description": "Response varies by Request type: GetTile returns image, GetCapabilities returns XML.",
    "properties": {
        "image_base64": {"type": "string", "description": "Base64-encoded tile image (GetTile)."},
        "content_type": {"type": "string", "description": "MIME type of the response."},
        "size_bytes": {"type": "integer", "description": "Tile size in bytes (GetTile)."},
        "xml": {"type": "string", "description": "XML capabilities document (GetCapabilities)."}
    }
}

# wmts_get_standard_tile, wmts_get_simple_tile — always return image
WMTS_TILE = _IMAGE_RESULT


# ============================================================
# Tool name → outputSchema mapping (all 68 tools)
# ============================================================
TOOL_OUTPUT_SCHEMAS = {
    # Geocoding & Address (9)
    "geocode": GEOCODE_RESPONSE,
    "reverse_geocode": GEOCODE_RESPONSE,
    "verify_address": GEOCODE_RESPONSE,
    "autocomplete": AUTOCOMPLETE_RESPONSE,
    "autocomplete_postal_city": AUTOCOMPLETE_RESPONSE,
    "autocomplete_v2": AUTOCOMPLETE_V2_RESPONSE,
    "lookup": LOOKUP_RESPONSE,
    "parse_address": PARSE_ADDRESS_RESPONSE,
    "parse_address_batch": PARSE_ADDRESS_RESPONSE,
    # Geolocation (2)
    "geo_locate_ip_address": GEO_LOCATE_IP_RESPONSE,
    "geo_locate_wifi_access_point": GEO_LOCATE_WIFI_RESPONSE,
    # Verification (5)
    "verify_email": VERIFY_EMAIL_RESPONSE,
    "verify_batch_emails": VERIFY_BATCH_EMAILS_RESPONSE,
    "parse_name": PARSE_NAME_RESPONSE,
    "validate_phone": VALIDATE_PHONE_RESPONSE,
    "validate_batch_phones": VALIDATE_BATCH_PHONES_RESPONSE,
    # Timezone (2)
    "timezone_addresses": TIMEZONE_RESPONSE,
    "timezone_locations": TIMEZONE_RESPONSE,
    # Tax & Emergency (6)
    "lookup_tax_jurisdiction": TAX_JURISDICTION_RESPONSE,
    "psap_address": PSAP_RESPONSE,
    "psap_location": PSAP_RESPONSE,
    "psap_ahj_address": PSAP_AHJ_RESPONSE,
    "psap_ahj_location": PSAP_AHJ_RESPONSE,
    "psap_ahj_fccid": PSAP_AHJ_RESPONSE,
    # GraphQL Property & Risk (9)
    "get_property_data": GET_PROPERTY_DATA,
    "get_property_attributes_by_address": GET_PROPERTY_ATTRIBUTES,
    "get_replacement_cost_by_address": GET_REPLACEMENT_COST,
    "get_flood_risk_by_address": GET_FLOOD_RISK,
    "get_wildfire_risk_by_address": GET_WILDFIRE_RISK,
    "get_property_fire_risk": GET_PROPERTY_FIRE_RISK,
    "get_earth_risk": GET_EARTH_RISK,
    "get_coastal_risk": GET_COASTAL_RISK,
    "get_historical_weather_risk": GET_HISTORICAL_WEATHER_RISK,
    # GraphQL Demographics (8)
    "get_demographics": GET_DEMOGRAPHICS,
    "get_crime_index": GET_CRIME_INDEX,
    "get_psyte_geodemographics_by_address": GET_PSYTE,
    "get_ground_view_by_address": GET_GROUND_VIEW,
    "get_neighborhoods_by_address": GET_NEIGHBORHOODS,
    "get_schools_by_address": GET_SCHOOLS,
    "get_buildings_by_address": GET_BUILDINGS,
    "get_parcels_by_address": GET_PARCELS,
    # GraphQL Advanced (5)
    "get_addresses_detailed": GET_ADDRESSES_DETAILED,
    "get_parcel_by_owner_detailed": GET_PARCEL_BY_OWNER,
    "get_address_family": GET_ADDRESS_FAMILY,
    "get_serviceability": GET_SERVICEABILITY,
    "get_places_by_address": GET_PLACES,
    # Spatial Analysis (7)
    "find_nearest_candidates": GEOJSON_FEATURE_COLLECTION,
    "search_at_location": GEOJSON_FEATURE_COLLECTION,
    "overlap": GEOJSON_FEATURE_COLLECTION,
    "summarize": GEOJSON_FEATURE_COLLECTION,
    "get_spatial_products": SPATIAL_PRODUCTS_RESPONSE,
    "list_spatial_tables": SPATIAL_TABLES_RESPONSE,
    "get_table_metadata": TABLE_METADATA_RESPONSE,
    # OGC Features (10)
    "ogc_landing_page": OGC_LANDING_PAGE,
    "ogc_api_definition": OGC_API_DEFINITION,
    "ogc_functions": OGC_FUNCTIONS,
    "ogc_conformance": OGC_CONFORMANCE,
    "ogc_collections": OGC_COLLECTIONS,
    "ogc_collection": OGC_COLLECTION,
    "ogc_collection_schema": OGC_COLLECTION_SCHEMA,
    "ogc_collection_queryables": OGC_COLLECTION_QUERYABLES,
    "ogc_collection_items": OGC_FEATURE_COLLECTION,
    "ogc_feature_by_id": OGC_FEATURE_COLLECTION,
    # WMS (2)
    "wms_get_request": WMS_GET_REQUEST,
    "wms_post_get_map": WMS_POST_GET_MAP,
    # WMTS (3)
    "wmts_request": WMTS_REQUEST,
    "wmts_get_standard_tile": WMTS_TILE,
    "wmts_get_simple_tile": WMTS_TILE,
}
