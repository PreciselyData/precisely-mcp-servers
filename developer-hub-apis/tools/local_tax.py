"""
Local Tax Service functions using Precisely APIs SDK.
Functions for calculating taxes and retrieving tax rates based on addresses and locations.
"""

import json
import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.local_tax_service_api import LocalTaxServiceApi
from com.precisely.apis.model.tax_address_request import TaxAddressRequest
from com.precisely.apis.model.tax_location_request import TaxLocationRequest
from com.precisely.apis.model.tax_rate_address_request import TaxRateAddressRequest
from com.precisely.apis.model.tax_rate_location_request import TaxRateLocationRequest
from com.precisely.apis.model.ipd_tax_by_address_batch_request import IPDTaxByAddressBatchRequest
from com.precisely.apis.model.tax_address import TaxAddress
from com.precisely.apis.model.tax_locations import TaxLocations
from com.precisely.apis.model.local_tax_preferences import LocalTaxPreferences
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Local Tax Service API instance."""
    api = LocalTaxServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def get_specific_tax_by_address(tax_rate_type_id, address, purchase_amount):
    """
    Calculate tax amount for a specific address and purchase amount.
    
    Args:
        tax_rate_type_id (str): The tax rate ID (e.g., 'sales', 'use', etc.)
        address (str): The address to be searched
        purchase_amount (str): The amount on which tax to be calculated
    
    Returns:
        dict: API response with tax calculation or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_specific_tax_by_address(
            tax_rate_type_id=tax_rate_type_id,
            address=address,
            purchase_amount=purchase_amount
        )
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract basic response information
        if hasattr(response, 'object_id') and response.object_id:
            result["data"]["object_id"] = response.object_id
        
        # Extract matched address information
        if hasattr(response, 'matched_address') and response.matched_address:
            matched_address = {}
            if hasattr(response.matched_address, 'formatted_address'):
                matched_address['formatted_address'] = response.matched_address.formatted_address
            if hasattr(response.matched_address, 'main_address_line'):
                matched_address['main_address_line'] = response.matched_address.main_address_line
            if hasattr(response.matched_address, 'address_last_line'):
                matched_address['address_last_line'] = response.matched_address.address_last_line
            if hasattr(response.matched_address, 'place_name'):
                matched_address['place_name'] = response.matched_address.place_name
            if hasattr(response.matched_address, 'area_name1'):
                matched_address['area_name1'] = response.matched_address.area_name1
            if hasattr(response.matched_address, 'area_name2'):
                matched_address['area_name2'] = response.matched_address.area_name2
            if hasattr(response.matched_address, 'area_name3'):
                matched_address['area_name3'] = response.matched_address.area_name3
            if hasattr(response.matched_address, 'postal_code'):
                matched_address['postal_code'] = response.matched_address.postal_code
            if hasattr(response.matched_address, 'country'):
                matched_address['country'] = response.matched_address.country
            result["data"]["matched_address"] = matched_address
        
        # Extract sales tax information
        if hasattr(response, 'sales_tax') and response.sales_tax:
            sales_tax = {}
            if hasattr(response.sales_tax, 'total_sales_tax'):
                sales_tax['total_sales_tax'] = response.sales_tax.total_sales_tax
            if hasattr(response.sales_tax, 'state_sales_tax'):
                sales_tax['state_sales_tax'] = response.sales_tax.state_sales_tax
            if hasattr(response.sales_tax, 'county_sales_tax'):
                sales_tax['county_sales_tax'] = response.sales_tax.county_sales_tax
            if hasattr(response.sales_tax, 'muni_city_sales_tax'):
                sales_tax['muni_city_sales_tax'] = response.sales_tax.muni_city_sales_tax
            if hasattr(response.sales_tax, 'district_sales_tax'):
                sales_tax['district_sales_tax'] = response.sales_tax.district_sales_tax
            result["data"]["sales_tax"] = sales_tax
        
        # Extract use tax information
        if hasattr(response, 'use_tax') and response.use_tax:
            use_tax = {}
            if hasattr(response.use_tax, 'total_use_tax'):
                use_tax['total_use_tax'] = response.use_tax.total_use_tax
            if hasattr(response.use_tax, 'state_use_tax'):
                use_tax['state_use_tax'] = response.use_tax.state_use_tax
            if hasattr(response.use_tax, 'county_use_tax'):
                use_tax['county_use_tax'] = response.use_tax.county_use_tax
            if hasattr(response.use_tax, 'muni_city_use_tax'):
                use_tax['muni_city_use_tax'] = response.use_tax.muni_city_use_tax
            if hasattr(response.use_tax, 'district_use_tax'):
                use_tax['district_use_tax'] = response.use_tax.district_use_tax
            result["data"]["use_tax"] = use_tax
        
        # Extract tax jurisdiction information
        if hasattr(response, 'tax_jurisdiction') and response.tax_jurisdiction:
            jurisdiction = {}
            if hasattr(response.tax_jurisdiction, 'confidence'):
                jurisdiction['confidence'] = response.tax_jurisdiction.confidence
            if hasattr(response.tax_jurisdiction, 'state_sales_tax_rate'):
                jurisdiction['state_sales_tax_rate'] = response.tax_jurisdiction.state_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'county_sales_tax_rate'):
                jurisdiction['county_sales_tax_rate'] = response.tax_jurisdiction.county_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'muni_city_sales_tax_rate'):
                jurisdiction['muni_city_sales_tax_rate'] = response.tax_jurisdiction.muni_city_sales_tax_rate
            result["data"]["tax_jurisdiction"] = jurisdiction
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_specific_tax_by_location(tax_rate_type_id, latitude, longitude, purchase_amount):
    """
    Calculate tax amount for a specific location coordinates and purchase amount.
    
    Args:
        tax_rate_type_id (str): The tax rate ID (e.g., 'sales', 'use', etc.)
        latitude (str): Latitude of the location
        longitude (str): Longitude of the location
        purchase_amount (str): The amount on which tax to be calculated
    
    Returns:
        dict: API response with tax calculation or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_specific_tax_by_location(
            tax_rate_type_id=tax_rate_type_id,
            latitude=latitude,
            longitude=longitude,
            purchase_amount=purchase_amount
        )
        
        # Convert response using same structure as address-based function
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract basic response information
        if hasattr(response, 'object_id') and response.object_id:
            result["data"]["object_id"] = response.object_id
        
        # Extract sales tax information
        if hasattr(response, 'sales_tax') and response.sales_tax:
            sales_tax = {}
            if hasattr(response.sales_tax, 'total_sales_tax'):
                sales_tax['total_sales_tax'] = response.sales_tax.total_sales_tax
            if hasattr(response.sales_tax, 'state_sales_tax'):
                sales_tax['state_sales_tax'] = response.sales_tax.state_sales_tax
            if hasattr(response.sales_tax, 'county_sales_tax'):
                sales_tax['county_sales_tax'] = response.sales_tax.county_sales_tax
            if hasattr(response.sales_tax, 'muni_city_sales_tax'):
                sales_tax['muni_city_sales_tax'] = response.sales_tax.muni_city_sales_tax
            if hasattr(response.sales_tax, 'district_sales_tax'):
                sales_tax['district_sales_tax'] = response.sales_tax.district_sales_tax
            result["data"]["sales_tax"] = sales_tax
        
        # Extract use tax information
        if hasattr(response, 'use_tax') and response.use_tax:
            use_tax = {}
            if hasattr(response.use_tax, 'total_use_tax'):
                use_tax['total_use_tax'] = response.use_tax.total_use_tax
            if hasattr(response.use_tax, 'state_use_tax'):
                use_tax['state_use_tax'] = response.use_tax.state_use_tax
            if hasattr(response.use_tax, 'county_use_tax'):
                use_tax['county_use_tax'] = response.use_tax.county_use_tax
            if hasattr(response.use_tax, 'muni_city_use_tax'):
                use_tax['muni_city_use_tax'] = response.use_tax.muni_city_use_tax
            if hasattr(response.use_tax, 'district_use_tax'):
                use_tax['district_use_tax'] = response.use_tax.district_use_tax
            result["data"]["use_tax"] = use_tax
        
        # Extract tax jurisdiction information
        if hasattr(response, 'tax_jurisdiction') and response.tax_jurisdiction:
            jurisdiction = {}
            if hasattr(response.tax_jurisdiction, 'confidence'):
                jurisdiction['confidence'] = response.tax_jurisdiction.confidence
            if hasattr(response.tax_jurisdiction, 'state_sales_tax_rate'):
                jurisdiction['state_sales_tax_rate'] = response.tax_jurisdiction.state_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'county_sales_tax_rate'):
                jurisdiction['county_sales_tax_rate'] = response.tax_jurisdiction.county_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'muni_city_sales_tax_rate'):
                jurisdiction['muni_city_sales_tax_rate'] = response.tax_jurisdiction.muni_city_sales_tax_rate
            result["data"]["tax_jurisdiction"] = jurisdiction
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_specific_tax_rate_by_address(tax_rate_type_id, address):
    """
    Get tax rates for a specific address without calculating actual tax amount.
    
    Args:
        tax_rate_type_id (str): The tax rate ID (e.g., 'sales', 'use', etc.)
        address (str): The address to be searched
    
    Returns:
        dict: API response with tax rates or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_specific_tax_rate_by_address(
            tax_rate_type_id=tax_rate_type_id,
            address=address
        )
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract basic response information
        if hasattr(response, 'object_id') and response.object_id:
            result["data"]["object_id"] = response.object_id
        
        # Extract matched address information
        if hasattr(response, 'matched_address') and response.matched_address:
            matched_address = {}
            if hasattr(response.matched_address, 'formatted_address'):
                matched_address['formatted_address'] = response.matched_address.formatted_address
            if hasattr(response.matched_address, 'main_address_line'):
                matched_address['main_address_line'] = response.matched_address.main_address_line
            if hasattr(response.matched_address, 'address_last_line'):
                matched_address['address_last_line'] = response.matched_address.address_last_line
            if hasattr(response.matched_address, 'place_name'):
                matched_address['place_name'] = response.matched_address.place_name
            if hasattr(response.matched_address, 'area_name1'):
                matched_address['area_name1'] = response.matched_address.area_name1
            if hasattr(response.matched_address, 'postal_code'):
                matched_address['postal_code'] = response.matched_address.postal_code
            if hasattr(response.matched_address, 'country'):
                matched_address['country'] = response.matched_address.country
            result["data"]["matched_address"] = matched_address
        
        # Extract tax jurisdiction information (rates only)
        if hasattr(response, 'tax_jurisdiction') and response.tax_jurisdiction:
            jurisdiction = {}
            if hasattr(response.tax_jurisdiction, 'confidence'):
                jurisdiction['confidence'] = response.tax_jurisdiction.confidence
            if hasattr(response.tax_jurisdiction, 'state_sales_tax_rate'):
                jurisdiction['state_sales_tax_rate'] = response.tax_jurisdiction.state_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'county_sales_tax_rate'):
                jurisdiction['county_sales_tax_rate'] = response.tax_jurisdiction.county_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'muni_city_sales_tax_rate'):
                jurisdiction['muni_city_sales_tax_rate'] = response.tax_jurisdiction.muni_city_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'district_sales_tax_rate'):
                jurisdiction['district_sales_tax_rate'] = response.tax_jurisdiction.district_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'state_use_tax_rate'):
                jurisdiction['state_use_tax_rate'] = response.tax_jurisdiction.state_use_tax_rate
            if hasattr(response.tax_jurisdiction, 'county_use_tax_rate'):
                jurisdiction['county_use_tax_rate'] = response.tax_jurisdiction.county_use_tax_rate
            if hasattr(response.tax_jurisdiction, 'muni_city_use_tax_rate'):
                jurisdiction['muni_city_use_tax_rate'] = response.tax_jurisdiction.muni_city_use_tax_rate
            if hasattr(response.tax_jurisdiction, 'district_use_tax_rate'):
                jurisdiction['district_use_tax_rate'] = response.tax_jurisdiction.district_use_tax_rate
            result["data"]["tax_jurisdiction"] = jurisdiction
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_specific_tax_rate_by_location(tax_rate_type_id, latitude, longitude):
    """
    Get tax rates for a specific location without calculating actual tax amount.
    
    Args:
        tax_rate_type_id (str): The tax rate ID (e.g., 'sales', 'use', etc.)
        latitude (str): Latitude of the location
        longitude (str): Longitude of the location
    
    Returns:
        dict: API response with tax rates or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_specific_tax_rate_by_location(
            tax_rate_type_id=tax_rate_type_id,
            latitude=latitude,
            longitude=longitude
        )
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract basic response information
        if hasattr(response, 'object_id') and response.object_id:
            result["data"]["object_id"] = response.object_id
        
        # Extract tax jurisdiction information (rates only)
        if hasattr(response, 'tax_jurisdiction') and response.tax_jurisdiction:
            jurisdiction = {}
            if hasattr(response.tax_jurisdiction, 'confidence'):
                jurisdiction['confidence'] = response.tax_jurisdiction.confidence
            if hasattr(response.tax_jurisdiction, 'state_sales_tax_rate'):
                jurisdiction['state_sales_tax_rate'] = response.tax_jurisdiction.state_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'county_sales_tax_rate'):
                jurisdiction['county_sales_tax_rate'] = response.tax_jurisdiction.county_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'muni_city_sales_tax_rate'):
                jurisdiction['muni_city_sales_tax_rate'] = response.tax_jurisdiction.muni_city_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'district_sales_tax_rate'):
                jurisdiction['district_sales_tax_rate'] = response.tax_jurisdiction.district_sales_tax_rate
            if hasattr(response.tax_jurisdiction, 'state_use_tax_rate'):
                jurisdiction['state_use_tax_rate'] = response.tax_jurisdiction.state_use_tax_rate
            if hasattr(response.tax_jurisdiction, 'county_use_tax_rate'):
                jurisdiction['county_use_tax_rate'] = response.tax_jurisdiction.county_use_tax_rate
            if hasattr(response.tax_jurisdiction, 'muni_city_use_tax_rate'):
                jurisdiction['muni_city_use_tax_rate'] = response.tax_jurisdiction.muni_city_use_tax_rate
            if hasattr(response.tax_jurisdiction, 'district_use_tax_rate'):
                jurisdiction['district_use_tax_rate'] = response.tax_jurisdiction.district_use_tax_rate
            result["data"]["tax_jurisdiction"] = jurisdiction
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_ipd_tax_by_address(address, return_lat_long_fields="N", lat_long_format="Decimal"):
    """
    Get IPD (Insurance Premium District) tax rates for a specific address.
    
    Args:
        address (str): The address to be searched
        return_lat_long_fields (str): Y or N (default is N) - Returns Latitude Longitude Fields
        lat_long_format (str): (default is Decimal) - Returns Desired Latitude Longitude Format
    
    Returns:
        dict: API response with IPD tax information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_ipd_tax_by_address(
            address=address,
            return_lat_long_fields=return_lat_long_fields,
            lat_long_format=lat_long_format
        )
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract basic response information
        if hasattr(response, 'object_id') and response.object_id:
            result["data"]["object_id"] = response.object_id
        
        # Extract matched address information
        if hasattr(response, 'matched_address') and response.matched_address:
            matched_address = {}
            if hasattr(response.matched_address, 'formatted_address'):
                matched_address['formatted_address'] = response.matched_address.formatted_address
            if hasattr(response.matched_address, 'main_address_line'):
                matched_address['main_address_line'] = response.matched_address.main_address_line
            if hasattr(response.matched_address, 'address_last_line'):
                matched_address['address_last_line'] = response.matched_address.address_last_line
            if hasattr(response.matched_address, 'place_name'):
                matched_address['place_name'] = response.matched_address.place_name
            if hasattr(response.matched_address, 'area_name1'):
                matched_address['area_name1'] = response.matched_address.area_name1
            if hasattr(response.matched_address, 'postal_code'):
                matched_address['postal_code'] = response.matched_address.postal_code
            if hasattr(response.matched_address, 'country'):
                matched_address['country'] = response.matched_address.country
            result["data"]["matched_address"] = matched_address
        
        # Extract IPD tax district information
        if hasattr(response, 'ipd') and response.ipd:
            ipd_data = {}
            if hasattr(response.ipd, 'ipd_key'):
                ipd_data['ipd_key'] = response.ipd.ipd_key
            if hasattr(response.ipd, 'description'):
                ipd_data['description'] = response.ipd.description
            if hasattr(response.ipd, 'ipd_rate'):
                ipd_data['ipd_rate'] = response.ipd.ipd_rate
            result["data"]["ipd"] = ipd_data
        
        # Extract latitude/longitude if requested
        if hasattr(response, 'lat_long_fields') and response.lat_long_fields:
            lat_long = {}
            if hasattr(response.lat_long_fields, 'latitude'):
                lat_long['latitude'] = response.lat_long_fields.latitude
            if hasattr(response.lat_long_fields, 'longitude'):
                lat_long['longitude'] = response.lat_long_fields.longitude
            result["data"]["lat_long_fields"] = lat_long
        
        return result
        
    except ApiException as e:
        return {
            "success": False,
            "error": f"API Error: {e.status} - {e.reason}",
            "details": e.body if hasattr(e, 'body') else str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


@mcp.tool()
def get_batch_tax_by_address(tax_rate_type_id, addresses_with_purchase_amounts, preferences=None):
    """
    Calculate taxes for multiple addresses with purchase amounts in a single request.
    Note: This is a simplified version that processes addresses individually due to model complexity.
    
    Args:
        tax_rate_type_id (str): The tax rate ID (e.g., 'sales', 'use', etc.)
        addresses_with_purchase_amounts (list): List of dicts with 'address' and 'purchase_amount' keys
        preferences (dict, optional): Tax calculation preferences
    
    Returns:
        dict: API response with batch tax calculations or error information
    """
    try:
        # For now, process each address individually and combine results
        # This avoids complex model instantiation issues
        results = []
        
        for i, item in enumerate(addresses_with_purchase_amounts):
            address = item.get('address', '')
            purchase_amount = item.get('purchase_amount', '0')
            
            # Get individual tax calculation
            individual_result = get_specific_tax_by_address(
                tax_rate_type_id=tax_rate_type_id,
                address=address,
                purchase_amount=purchase_amount
            )
            
            if individual_result.get('success'):
                # Add object_id for batch processing consistency
                individual_result['data']['object_id'] = str(i + 1)
                results.append(individual_result['data'])
            else:
                # Include failed result with error info
                error_result = {
                    'object_id': str(i + 1),
                    'error': individual_result.get('error', 'Unknown error'),
                    'input_address': address,
                    'input_amount': purchase_amount
                }
                results.append(error_result)
        
        return {
            "success": True,
            "data": {
                "responses": results
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Batch processing error: {str(e)}"
        }


@mcp.tool()
def validate_tax_rate_type_id(tax_rate_type_id):
    """
    Validate if a tax rate type ID is in acceptable format.
    
    Args:
        tax_rate_type_id (str): Tax rate type ID to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    # Common tax rate types - NOTE: "general" is known to work with Precisely API
    valid_types = ['general', 'sales', 'use', 'excise', 'luxury', 'sin', 'vat', 'gst']
    
    if not tax_rate_type_id or not isinstance(tax_rate_type_id, str):
        return False
    
    # Check if it's a known type or follows a reasonable pattern
    tax_type_lower = tax_rate_type_id.lower().strip()
    
    # Check against known types
    if tax_type_lower in valid_types:
        return True
    
    # Allow alphanumeric with underscores/hyphens (reasonable pattern)
    import re
    if re.match(r'^[a-zA-Z0-9_-]+$', tax_rate_type_id) and len(tax_rate_type_id) <= 50:
        return True
    
    return False


@mcp.tool()
def validate_purchase_amount(purchase_amount):
    """
    Validate if a purchase amount is in acceptable format.
    
    Args:
        purchase_amount (str): Purchase amount to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    import re
    
    if not purchase_amount or not isinstance(purchase_amount, str):
        return False
    
    # Remove whitespace
    amount = purchase_amount.strip()
    
    # Check for valid decimal number format
    # Allows: 100, 100.00, 100.5, 0.50, etc.
    decimal_pattern = r'^\d+(\.\d{1,2})?$'
    
    if re.match(decimal_pattern, amount):
        try:
            float_amount = float(amount)
            # Check reasonable range (0 to 1 billion)
            return 0 <= float_amount <= 1000000000
        except ValueError:
            return False
    
    return False
