import json
from typing import Optional, Dict, Any
from com.precisely.apis.api.address_autocomplete_service_api import AddressAutocompleteServiceApi
from com.precisely.apis.exceptions import ApiException

from server import mcp
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely



@mcp.tool()
def create_autocomplete_api() -> AddressAutocompleteServiceApi:
    """Create and configure the Address Autocomplete API instance."""
    api = AddressAutocompleteServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api

@mcp.tool()
def address_autocomplete_search(
    search_text: str,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    search_radius: Optional[str] = None,
    search_radius_unit: Optional[str] = None,
    max_candidates: Optional[str] = None,
    country: Optional[str] = None,
    match_on_address_number: Optional[str] = None,
    auto_detect_location: Optional[str] = None,
    ip_address: Optional[str] = None,
    area_name1: Optional[str] = None,
    area_name3: Optional[str] = None,
    post_code: Optional[str] = None,
    return_admin_areas_only: Optional[str] = None,
    include_ranges_details: Optional[str] = None,
    search_type: Optional[str] = None,
    search_on_address_number: Optional[str] = None,
    search_on_unit_info: Optional[str] = None,
    search_on_po_box: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform address autocomplete search with configurable parameters.
    
    Args:
        search_text: The input text to be searched (required)
        latitude: Latitude of the location
        longitude: Longitude of the location
        search_radius: Radius range within which search is performed
        search_radius_unit: Radius unit (Feet, Kilometers, Miles, Meters)
        max_candidates: Maximum number of POIs that can be retrieved
        country: Country ISO code
        match_on_address_number: Force API to match on address number
        auto_detect_location: Allow API to detect origin automatically
        ip_address: IP address for location detection
        area_name1: State/province of the input to be searched
        area_name3: City of the input to be searched
        post_code: Postal code of the input to be searched
        return_admin_areas_only: Return only admin areas ('Y'/'N')
        include_ranges_details: Include unit info of ranges ('Y'/'N')
        search_type: Preference to control search type
        search_on_address_number: Preference to search on address number
        search_on_unit_info: Preference to search on unit info
        search_on_po_box: Enable search for PO Box matching
    
    Returns:
        Dict containing the API response or error information
    """
    api = create_autocomplete_api()
    
    # Build kwargs dictionary with only non-None values
    kwargs = {}
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'search_radius': search_radius,
        'search_radius_unit': search_radius_unit,
        'max_candidates': max_candidates,
        'country': country,
        'match_on_address_number': match_on_address_number,
        'auto_detect_location': auto_detect_location,
        'ip_address': ip_address,
        'area_name1': area_name1,
        'area_name3': area_name3,
        'post_code': post_code,
        'return_admin_areas_only': return_admin_areas_only,
        'include_ranges_details': include_ranges_details,
        'search_type': search_type,
        'search_on_address_number': search_on_address_number,
        'search_on_unit_info': search_on_unit_info,
        'search_on_po_box': search_on_po_box
    }
    
    # Add only non-None parameters
    for key, value in params.items():
        if value is not None:
            kwargs[key] = value
    
    try:
        response = api.search_v2(search_text, **kwargs)
        return {
            'success': True,
            'data': response.to_dict() if hasattr(response, 'to_dict') else str(response),
            'search_text': search_text,
            'parameters': kwargs
        }
    except ApiException as e:
        return {
            'success': False,
            'error': e.body if hasattr(e, 'body') else str(e),
            'search_text': search_text,
            'parameters': kwargs
        }
