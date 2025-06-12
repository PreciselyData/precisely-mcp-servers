"""
Email Verification functions using Precisely APIs SDK.
Functions for validating email addresses for deliverability and correctness.
"""

import json
import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.email_verification_service_api import EmailVerificationServiceApi
from com.precisely.apis.exceptions import ApiException

# Model imports
from com.precisely.apis.model.validate_email_address_api_request import ValidateEmailAddressAPIRequest
from com.precisely.apis.model.validate_email_address_input import ValidateEmailAddressInput
from com.precisely.apis.model.validate_email_address_input_row import ValidateEmailAddressInputRow

from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely

from server import mcp
def _get_api_client():
    """Create and configure the Email Verification API instance."""
    api = EmailVerificationServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api

@mcp.tool()
def validate_email_address(
    email_address,
    rtc="N",
    bogus="N", 
    role="N",
    emps="N",
    fccwireless="N",
    language="E",
    complain="N",
    disposable="N",
    atc="N",
    rtc_timeout="5"
):
    """
    Validate an email address for deliverability and correctness.
    
    Args:
        email_address (str): The email address to validate (required)
        rtc (str, optional): Real-time contact verification. Default "N"
        bogus (str, optional): Check for bogus email addresses. Default "N"  
        role (str, optional): Check for role-based emails. Default "N"
        emps (str, optional): Employee email verification. Default "N"
        fccwireless (str, optional): FCC wireless check. Default "N"
        language (str, optional): Language preference. Default "E" (English)
        complain (str, optional): Complainer list check. Default "N"
        disposable (str, optional): Disposable email check. Default "N"
        atc (str, optional): Address type code. Default "N"
        rtc_timeout (str, optional): Timeout for real-time checks. Default "5"
    
    Returns:
        dict: API response with email validation results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create the input row with email address and validation options
        input_row = ValidateEmailAddressInputRow(
            email_address=email_address,
            rtc=rtc,
            bogus=bogus,
            role=role,
            emps=emps,
            fccwireless=fccwireless,
            language=language,
            complain=complain,
            disposable=disposable,
            atc=atc,
            rtc_timeout=rtc_timeout
        )
        
        # Create the input object
        input_obj = ValidateEmailAddressInput(row=[input_row])
        
        # Create the request object
        request = ValidateEmailAddressAPIRequest(input=input_obj)
        
        # Call the API
        response = api_instance.validate_email_address(request)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": []
        }
        
        if hasattr(response, 'output') and response.output:
            for output in response.output:
                output_dict = {}
                
                # Map response fields to dictionary
                if hasattr(output, 'email') and output.email is not None:
                    output_dict['email'] = output.email
                if hasattr(output, 'finding') and output.finding is not None:
                    output_dict['finding'] = output.finding
                if hasattr(output, 'comment') and output.comment is not None:
                    output_dict['comment'] = output.comment
                if hasattr(output, 'comment_code') and output.comment_code is not None:
                    output_dict['comment_code'] = output.comment_code
                if hasattr(output, 'sugg_email') and output.sugg_email is not None:
                    output_dict['suggested_email'] = output.sugg_email
                if hasattr(output, 'sugg_comment') and output.sugg_comment is not None:
                    output_dict['suggested_comment'] = output.sugg_comment
                if hasattr(output, 'error_response') and output.error_response is not None:
                    output_dict['error_response'] = output.error_response
                if hasattr(output, 'error') and output.error is not None:
                    output_dict['error'] = output.error
                if hasattr(output, 'status') and output.status is not None:
                    output_dict['status'] = output.status
                if hasattr(output, 'status_code') and output.status_code is not None:
                    output_dict['status_code'] = output.status_code
                if hasattr(output, 'status_description') and output.status_description is not None:
                    output_dict['status_description'] = output.status_description
                
                result["data"].append(output_dict)
        
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
def validate_email_batch(email_addresses):
    """
    Validate multiple email addresses in a single request.
    
    Args:
        email_addresses (list): List of email addresses to validate
    
    Returns:
        dict: API response with validation results for all emails or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Create input rows for each email address
        input_rows = []
        for email in email_addresses:
            input_row = ValidateEmailAddressInputRow(
                email_address=email,
                rtc="N",
                bogus="N",
                role="N",
                emps="N",
                fccwireless="N",
                language="E",
                complain="N",
                disposable="N",
                atc="N",
                rtc_timeout="5"
            )
            input_rows.append(input_row)
        
        # Create the input object
        input_obj = ValidateEmailAddressInput(row=input_rows)
        
        # Create the request object
        request = ValidateEmailAddressAPIRequest(input=input_obj)
        
        # Call the API
        response = api_instance.validate_email_address(request)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": []
        }
        
        if hasattr(response, 'output') and response.output:
            for output in response.output:
                output_dict = {}
                
                # Map response fields to dictionary
                if hasattr(output, 'email') and output.email is not None:
                    output_dict['email'] = output.email
                if hasattr(output, 'finding') and output.finding is not None:
                    output_dict['finding'] = output.finding
                if hasattr(output, 'comment') and output.comment is not None:
                    output_dict['comment'] = output.comment
                if hasattr(output, 'comment_code') and output.comment_code is not None:
                    output_dict['comment_code'] = output.comment_code
                if hasattr(output, 'sugg_email') and output.sugg_email is not None:
                    output_dict['suggested_email'] = output.sugg_email
                if hasattr(output, 'sugg_comment') and output.sugg_comment is not None:
                    output_dict['suggested_comment'] = output.sugg_comment
                if hasattr(output, 'error_response') and output.error_response is not None:
                    output_dict['error_response'] = output.error_response
                if hasattr(output, 'error') and output.error is not None:
                    output_dict['error'] = output.error
                if hasattr(output, 'status') and output.status is not None:
                    output_dict['status'] = output.status
                if hasattr(output, 'status_code') and output.status_code is not None:
                    output_dict['status_code'] = output.status_code
                if hasattr(output, 'status_description') and output.status_description is not None:
                    output_dict['status_description'] = output.status_description
                
                result["data"].append(output_dict)
        
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
def validate_email_with_options(
    email_address,
    options=None
):
    """
    Validate an email address with custom options.
    
    Args:
        email_address (str): The email address to validate (required)
        options (dict, optional): Custom validation options
    
    Returns:
        dict: API response with email validation results or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Default options
        default_options = {
            "rtc": "N",
            "bogus": "N", 
            "role": "N",
            "emps": "N",
            "fccwireless": "N",
            "language": "E",
            "complain": "N",
            "disposable": "N",
            "atc": "N",
            "rtc_timeout": "5"
        }
        
        # Merge with provided options
        if options:
            default_options.update(options)
        
        # Create the input row with email address and validation options
        input_row = ValidateEmailAddressInputRow(
            email_address=email_address,
            rtc=default_options.get("rtc"),
            bogus=default_options.get("bogus"),
            role=default_options.get("role"),
            emps=default_options.get("emps"),
            fccwireless=default_options.get("fccwireless"),
            language=default_options.get("language"),
            complain=default_options.get("complain"),
            disposable=default_options.get("disposable"),
            atc=default_options.get("atc"),
            rtc_timeout=default_options.get("rtc_timeout")
        )
        
        # Create the input object
        input_obj = ValidateEmailAddressInput(row=[input_row])
        
        # Create the request object  
        request_options = options.get("request_options", {}) if options else {}
        request = ValidateEmailAddressAPIRequest(
            input=input_obj,
            options=request_options if request_options else None
        )
        
        # Call the API
        response = api_instance.validate_email_address(request)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": []
        }
        
        if hasattr(response, 'output') and response.output:
            for output in response.output:
                output_dict = {}
                
                # Map response fields to dictionary
                if hasattr(output, 'email') and output.email is not None:
                    output_dict['email'] = output.email
                if hasattr(output, 'finding') and output.finding is not None:
                    output_dict['finding'] = output.finding
                if hasattr(output, 'comment') and output.comment is not None:
                    output_dict['comment'] = output.comment
                if hasattr(output, 'comment_code') and output.comment_code is not None:
                    output_dict['comment_code'] = output.comment_code
                if hasattr(output, 'sugg_email') and output.sugg_email is not None:
                    output_dict['suggested_email'] = output.sugg_email
                if hasattr(output, 'sugg_comment') and output.sugg_comment is not None:
                    output_dict['suggested_comment'] = output.sugg_comment
                if hasattr(output, 'error_response') and output.error_response is not None:
                    output_dict['error_response'] = output.error_response
                if hasattr(output, 'error') and output.error is not None:
                    output_dict['error'] = output.error
                if hasattr(output, 'status') and output.status is not None:
                    output_dict['status'] = output.status
                if hasattr(output, 'status_code') and output.status_code is not None:
                    output_dict['status_code'] = output.status_code
                if hasattr(output, 'status_description') and output.status_description is not None:
                    output_dict['status_description'] = output.status_description
                
                result["data"].append(output_dict)
        
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
        
