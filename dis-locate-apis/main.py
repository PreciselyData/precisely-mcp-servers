from precisely_sdk.server import mcp
from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os
print("started")
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')

client = ApiClient(
    base_url=BASE_URL,
    api_key=API_KEY,
    api_secret=API_SECRET
)   

from precisely_sdk.geo_addressing_api import (
    autocomplete,
    autocomplete_postal_city,
    autocomplete_v2,
    geocode,
    lookup,
    reverse_geocode,
    verify_address
)

from precisely_sdk.address_parser_api import (
    parse_address,
    parse_address_batch
)
from precisely_sdk.email_verification_api import (
    verify_email,
    verify_batch_emails
)
from precisely_sdk.emergency_info_api import (
    psap_address,
    psap_location,
    psap_ahj_address,
    psap_ahj_location,
    psap_ahj_fccid
)
from precisely_sdk.geolocation_api import (
    geo_locate_ip_address,
    geo_locate_wifi_access_point
)
from precisely_sdk.geo_tax_api import (
    lookup_by_address,
    lookup_by_addresses,
    lookup_by_location,
    lookup_by_locations
)
from precisely_sdk.name_parsing_api import (
    parse_name
)
from precisely_sdk.phone_verification_api import (
    validate_phone,
    validate_batch_phones
)
from precisely_sdk.timezone_api import (
    timezone_addresses,
    timezone_locations
)

from precisely_sdk.graphql_api import (
    # Core Property Data Functions
    get_addresses_detailed,
    get_buildings_by_address,
    get_parcels_by_address,
    get_places_nearby,
    get_property_attributes_by_address,
    get_replacement_cost_by_address,
    
    # Risk Assessment Functions
    get_coastal_risk,
    get_property_fire_risk,
    get_earth_risk,
    get_wildfire_risk_by_address,
    get_flood_risk_by_address,
    get_historical_weather_risk,
    
    # Demographics & Lifestyle Functions
    get_crime_index_by_address,
    get_psyte_geodemographics_by_address,
    get_ground_view_by_address,
    
    # Neighborhood & Area Functions
    get_neighborhoods_by_address,
    get_schools_by_address,
    get_serviceability,

    
    # Additional Relationship Functions
    get_parcel_by_owner_detailed,
    get_address_family
)    


__all__ = [
    "ApiClient",
    # Geo Addressing API
    "autocomplete",
    "autocomplete_postal_city",
    "autocomplete_v2",
    "geocode",
    "lookup",
    "reverse_geocode",
    "verify_address",
    
    # Address Parser API
    "parse_address",
    "parse_address_batch",
    
    # Email Verification API
    "verify_email",
    "verify_batch_emails",
    
    # Emergency Info API
    "psap_address",
    "psap_location",
    "psap_ahj_address",
    "psap_ahj_location",
    "psap_ahj_fccid",
    
    # Geolocation API
    "geo_locate_ip_address",
    "geo_locate_wifi_access_point",
    
    # Geo Tax API
    "lookup_by_address",
    "lookup_by_addresses",
    "lookup_by_location",
    "lookup_by_locations",
    
    # Name Parsing API
    "parse_name",
    
    # Phone Verification API
    "validate_phone",
    "validate_batch_phones",
    
    # Timezone API
    "timezone_addresses",
    "timezone_locations",
    
    # GraphQL API - Core Property Data Functions
    "get_addresses_detailed",
    "get_buildings_by_address",
    "get_parcels_by_address",
    "get_places_nearby",
    "get_property_attributes_by_address",
    "get_replacement_cost_by_address",
    
    # GraphQL API - Risk Assessment Functions
    "get_coastal_risk",
    "get_property_fire_risk",
    "get_earth_risk",
    "get_wildfire_risk_by_address",
    "get_flood_risk_by_address",
    "get_historical_weather_risk",
    
    # GraphQL API - Demographics & Lifestyle Functions
    "get_crime_index_by_address",
    "get_psyte_geodemographics_by_address",
    "get_ground_view_by_address",
    
    # GraphQL API - Neighborhood & Area Functions
    "get_neighborhoods_by_address",
    "get_schools_by_address",
    "get_serviceability",
    
    # GraphQL API - Additional Relationship Functions
    "get_parcel_by_owner_detailed",
    "get_address_family"
]

print("MCP Server Started")

if __name__ == "__main__":
    mcp.run()