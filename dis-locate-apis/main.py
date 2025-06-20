from precisely_sdk.server import mcp
from precisely_sdk.api_client import ApiClient
from dotenv import load_dotenv
import os
print("started")
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')
print(API_KEY, API_SECRET, BASE_URL)
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

__all__ = [
    "ApiClient",
    "autocomplete",
    "autocomplete_postal_city",
    "autocomplete_v2",
    "geocode",
    "lookup",
    "reverse_geocode",
    "verify_address",
    "generate_upload_url",
    "list_uploaded_files",
    "delete_uploaded_file",
    "bulk_geocode",
    "bulk_verify",
    "get_job_status",
    "parse_address",
    "parse_address_batch",
    "verify_email",
    "verify_batch_emails",
    "psap_address",
    "psap_location",
    "psap_ahj_address",
    "psap_ahj_location",
    "psap_ahj_fccid",
    "geo_locate_ip_address",
    "geo_locate_wifi_access_point",
    "lookup_by_address",
    "lookup_by_addresses",
    "lookup_by_location",
    "lookup_by_locations",
    "parse_name",
    "validate_phone",
    "validate_batch_phones",
    "timezone_addresses",
    "timezone_locations"
]

if __name__ == "__main__":
    mcp.run()