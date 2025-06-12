"""
Phone Verification functions using Precisely APIs SDK.
Functions for validating phone numbers and determining landline vs wireless type.
"""

import json
import os
import re
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.phone_verification_service_api import PhoneVerificationServiceApi
from com.precisely.apis.exceptions import ApiException

# Model imports
from com.precisely.apis.model.validate_phone_number_api_request import ValidatePhoneNumberAPIRequest
from com.precisely.apis.model.validate_phone_number_api_request_input import ValidatePhoneNumberAPIRequestInput
from com.precisely.apis.model.validate_phone_number_api_request_input_row import ValidatePhoneNumberAPIRequestInputRow
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Phone Verification API instance."""
    api = PhoneVerificationServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def validate_phone_number(phone_number, country="US"):
    """
    Validate a phone number and determine if it's landline or wireless.
    
    Args:
        phone_number (str): The phone number to validate (required)
        country (str, optional): Country code for the phone number. Default "US"
        
    Returns:
        dict: Phone verification results including:
            - phone_number: Original phone number
            - phone_number_formatted: Formatted phone number
            - phone_type: Type of phone (landline, wireless, etc.)
            - carrier_name: Name of the carrier
            - country_code: Country code
            - mcc: Mobile Country Code
            - mnc: Mobile Network Code
            - result_code: Result status code
            - user_fields: Additional user fields
            
    Raises:
        ValueError: If phone_number is empty or invalid
        ApiException: If API call fails
    """
    try:
        if not phone_number or not phone_number.strip():
            raise ValueError("Phone number cannot be empty")
            
        # Create request objects
        input_row = ValidatePhoneNumberAPIRequestInputRow(
            phone_number=phone_number.strip(),
            country=country
        )
        
        input_data = ValidatePhoneNumberAPIRequestInput(
            row=[input_row]
        )
        
        request = ValidatePhoneNumberAPIRequest(
            input=input_data
        )
        
        # Make API call
        api = _get_api_client()
        response = api.validatephonenumber(request)
        
        # Parse response
        result = {}
        if hasattr(response, 'output') and response.output:
            output = response.output[0]
            result = {
                'phone_number': getattr(output, 'phone_number', ''),
                'phone_number_formatted': getattr(output, 'phone_number_formatted', ''),
                'phone_type': getattr(output, 'phone_type', ''),
                'carrier_name': getattr(output, 'carrier_name', ''),
                'country_code': getattr(output, 'country_code', ''),
                'mcc': getattr(output, 'mcc', ''),
                'mnc': getattr(output, 'mnc', ''),
                'result_code': getattr(output, 'result_code', ''),
                'user_fields': getattr(output, 'user_fields', [])
            }
        
        return result
        
    except ApiException as e:
        print(f"API error validating phone number {phone_number}: {e}")
        raise
    except Exception as e:
        print(f"Error validating phone number {phone_number}: {e}")
        raise


@mcp.tool()
def validate_phone_batch(phone_numbers, country="US"):
    """
    Validate multiple phone numbers in a single request.
    
    Args:
        phone_numbers (list): List of phone numbers to validate
        country (str, optional): Country code for all phone numbers. Default "US"
        
    Returns:
        list: List of phone verification results for each number
        
    Raises:
        ValueError: If phone_numbers is empty or not a list
        ApiException: If API call fails
    """
    try:
        if not phone_numbers or not isinstance(phone_numbers, list):
            raise ValueError("phone_numbers must be a non-empty list")
            
        # Create input rows for all phone numbers
        input_rows = []
        for phone_number in phone_numbers:
            if phone_number and phone_number.strip():
                input_rows.append(ValidatePhoneNumberAPIRequestInputRow(
                    phone_number=phone_number.strip(),
                    country=country
                ))
        
        if not input_rows:
            raise ValueError("No valid phone numbers provided")
            
        input_data = ValidatePhoneNumberAPIRequestInput(
            row=input_rows
        )
        
        request = ValidatePhoneNumberAPIRequest(
            input=input_data
        )
        
        # Make API call
        api = _get_api_client()
        response = api.validatephonenumber(request)
        
        # Parse response
        results = []
        if hasattr(response, 'output') and response.output:
            for output in response.output:
                result = {
                    'phone_number': getattr(output, 'phone_number', ''),
                    'phone_number_formatted': getattr(output, 'phone_number_formatted', ''),
                    'phone_type': getattr(output, 'phone_type', ''),
                    'carrier_name': getattr(output, 'carrier_name', ''),
                    'country_code': getattr(output, 'country_code', ''),
                    'mcc': getattr(output, 'mcc', ''),
                    'mnc': getattr(output, 'mnc', ''),
                    'result_code': getattr(output, 'result_code', ''),
                    'user_fields': getattr(output, 'user_fields', [])
                }
                results.append(result)
        
        return results
        
    except ApiException as e:
        print(f"API error validating phone numbers: {e}")
        raise
    except Exception as e:
        print(f"Error validating phone numbers: {e}")
        raise


@mcp.tool()
def validate_international_phone(phone_number, country):
    """
    Validate an international phone number with specific country code.
    
    Args:
        phone_number (str): The phone number to validate (required)
        country (str): Country code for the phone number (required)
        
    Returns:
        dict: Phone verification results
        
    Raises:
        ValueError: If phone_number or country is empty
        ApiException: If API call fails
    """
    try:
        if not phone_number or not phone_number.strip():
            raise ValueError("Phone number cannot be empty")
        if not country or not country.strip():
            raise ValueError("Country code cannot be empty")
            
        return validate_phone_number(phone_number.strip(), country.strip().upper())
        
    except Exception as e:
        print(f"Error validating international phone number: {e}")
        raise


@mcp.tool()
def is_valid_phone_format(phone_number):
    """
    Basic validation of phone number format using regex patterns.
    
    Args:
        phone_number (str): Phone number to validate format
        
    Returns:
        bool: True if format appears valid, False otherwise
    """
    try:
        if not phone_number or not isinstance(phone_number, str):
            return False
            
        # Remove common separators and spaces
        cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone_number.strip())
        
        # Check if it contains only digits
        if not cleaned.isdigit():
            return False
            
        # Check length (most phone numbers are 7-15 digits)
        if len(cleaned) < 7 or len(cleaned) > 15:
            return False
            
        return True
        
    except Exception:
        return False


@mcp.tool()
def is_wireless_phone_type(phone_type):
    """
    Check if a phone type indicates a wireless/mobile phone.
    
    Args:
        phone_type (str): Phone type returned from verification
        
    Returns:
        bool: True if phone type indicates wireless/mobile
    """
    try:
        if not phone_type:
            return False
            
        wireless_types = ['wireless', 'mobile', 'cell', 'cellular']
        return phone_type.lower() in wireless_types
        
    except Exception:
        return False


@mcp.tool()
def is_landline_phone_type(phone_type):
    """
    Check if a phone type indicates a landline phone.
    
    Args:
        phone_type (str): Phone type returned from verification
        
    Returns:
        bool: True if phone type indicates landline
    """
    try:
        if not phone_type:
            return False
            
        landline_types = ['landline', 'fixed', 'wireline']
        return phone_type.lower() in landline_types
        
    except Exception:
        return False


@mcp.tool()
def get_carrier_info(phone_number, country="US"):
    """
    Get carrier information for a phone number.
    
    Args:
        phone_number (str): The phone number to lookup
        country (str, optional): Country code. Default "US"
        
    Returns:
        dict: Carrier information including:
            - carrier_name: Name of the carrier
            - mcc: Mobile Country Code
            - mnc: Mobile Network Code
            - phone_type: Type of phone service
            
    Raises:
        ValueError: If phone_number is empty
        ApiException: If API call fails
    """
    try:
        result = validate_phone_number(phone_number, country)
        
        return {
            'carrier_name': result.get('carrier_name', ''),
            'mcc': result.get('mcc', ''),
            'mnc': result.get('mnc', ''),
            'phone_type': result.get('phone_type', '')
        }
        
    except Exception as e:
        print(f"Error getting carrier info for {phone_number}: {e}")
        raise


@mcp.tool()
def format_phone_number_display(phone_number, country="US"):
    """
    Get a properly formatted display version of a phone number.
    
    Args:
        phone_number (str): The phone number to format
        country (str, optional): Country code. Default "US"
        
    Returns:
        str: Formatted phone number for display
        
    Raises:
        ValueError: If phone_number is empty
        ApiException: If API call fails
    """
    try:
        result = validate_phone_number(phone_number, country)
        return result.get('phone_number_formatted', phone_number)
        
    except Exception as e:
        print(f"Error formatting phone number {phone_number}: {e}")
        raise


@mcp.tool()
def validate_phone_with_details(phone_number, country="US"):
    """
    Comprehensive phone validation returning all available details.
    
    Args:
        phone_number (str): The phone number to validate
        country (str, optional): Country code. Default "US"
        
    Returns:
        dict: Complete validation results with additional analysis:
            - validation_result: Full API response
            - is_valid: Boolean indicating if phone is valid
            - is_wireless: Boolean indicating if phone is wireless
            - is_landline: Boolean indicating if phone is landline
            - formatted_number: Display-formatted number
            - carrier_info: Carrier details
            
    Raises:
        ValueError: If phone_number is empty
        ApiException: If API call fails
    """
    try:
        result = validate_phone_number(phone_number, country)
        
        phone_type = result.get('phone_type', '')
        result_code = result.get('result_code', '')
        
        return {
            'validation_result': result,
            'is_valid': bool(result_code and result_code != 'ERROR'),
            'is_wireless': is_wireless_phone_type(phone_type),
            'is_landline': is_landline_phone_type(phone_type),
            'formatted_number': result.get('phone_number_formatted', ''),
            'carrier_info': {
                'name': result.get('carrier_name', ''),
                'mcc': result.get('mcc', ''),
                'mnc': result.get('mnc', ''),
                'type': phone_type
            }
        }
        
    except Exception as e:
        print(f"Error validating phone with details {phone_number}: {e}")
        raise


# Export all functions
__all__ = [
    'validate_phone_number',
    'validate_phone_batch', 
    'validate_international_phone',
    'is_valid_phone_format',
    'is_wireless_phone_type',
    'is_landline_phone_type',
    'get_carrier_info',
    'format_phone_number_display',
    'validate_phone_with_details'
]
