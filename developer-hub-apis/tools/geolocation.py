"""
Geolocation functions using Precisely APIs SDK.
Functions for determining location based on IP addresses and WiFi access points.
"""

import json
import os
from typing import Optional, Dict, Any, List
from com.precisely.apis.api.geolocation_service_api import GeolocationServiceApi
from com.precisely.apis.exceptions import ApiException
from credentials import PRECISELY_API_KEY, PRECISELY_API_SECRET  # Import your credentials securely


from server import mcp
def _get_api_client():
    """Create and configure the Geolocation API instance."""
    api = GeolocationServiceApi()
    # Set OAuth credentials (suppressing type warnings - these are dynamic attributes)
    setattr(api.api_client, 'oAuthApiKey', PRECISELY_API_KEY)  # type: ignore
    setattr(api.api_client, 'oAuthSecret', PRECISELY_API_SECRET)  # type: ignore
    api.api_client.generateAndSetToken()
    return api


@mcp.tool()
def get_location_by_ip_address(ip_address):
    """
    Get geographic location based on an IP address.
    
    Args:
        ip_address (str): The IP address to locate (required)
                         Must be a standard IPv4 octet and a valid external address
    
    Returns:
        dict: API response with location information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Call the API
        response = api_instance.get_location_by_ip_address(ip_address=ip_address)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract geometry information
        if hasattr(response, 'geometry') and response.geometry:
            geometry_dict = {}
            if hasattr(response.geometry, 'coordinates') and response.geometry.coordinates:
                geometry_dict['coordinates'] = response.geometry.coordinates
            if hasattr(response.geometry, 'type') and response.geometry.type:
                geometry_dict['type'] = response.geometry.type
            if hasattr(response.geometry, 'crs') and response.geometry.crs:
                crs_dict = {}
                if hasattr(response.geometry.crs, 'properties') and response.geometry.crs.properties:
                    crs_dict['properties'] = response.geometry.crs.properties
                if hasattr(response.geometry.crs, 'type') and response.geometry.crs.type:
                    crs_dict['type'] = response.geometry.crs.type
                geometry_dict['crs'] = crs_dict
            result["data"]["geometry"] = geometry_dict
        
        # Extract accuracy information
        if hasattr(response, 'accuracy') and response.accuracy:
            accuracy_dict = {}
            if hasattr(response.accuracy, 'unit') and response.accuracy.unit:
                accuracy_dict['unit'] = response.accuracy.unit
            if hasattr(response.accuracy, 'value') and response.accuracy.value:
                accuracy_dict['value'] = response.accuracy.value
            result["data"]["accuracy"] = accuracy_dict
        
        # Extract IP information
        if hasattr(response, 'ip_info') and response.ip_info:
            ip_info_dict = {}
            if hasattr(response.ip_info, 'ip_address') and response.ip_info.ip_address:
                ip_info_dict['ip_address'] = response.ip_info.ip_address
            if hasattr(response.ip_info, 'isp') and response.ip_info.isp:
                ip_info_dict['isp'] = response.ip_info.isp
            if hasattr(response.ip_info, 'connection_type') and response.ip_info.connection_type:
                ip_info_dict['connection_type'] = response.ip_info.connection_type
            if hasattr(response.ip_info, 'carrier') and response.ip_info.carrier:
                ip_info_dict['carrier'] = response.ip_info.carrier
            if hasattr(response.ip_info, 'routing_type') and response.ip_info.routing_type:
                ip_info_dict['routing_type'] = response.ip_info.routing_type
            if hasattr(response.ip_info, 'organization') and response.ip_info.organization:
                ip_info_dict['organization'] = response.ip_info.organization
            result["data"]["ip_info"] = ip_info_dict
        
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
def get_location_by_wifi_access_point(
    mac=None,
    ssid=None,
    rsid=None,
    speed=None,
    access_point=None
):
    """
    Get geographic location based on WiFi access point information.
    
    Args:
        mac (str, optional): 48-bit MAC address (BSSID) of wireless access point.
                           Format: Six groups of two hexadecimal digits separated by hyphens or colons
        ssid (str, optional): Service set identifier for WiFi access point.
                             Alphanumeric with maximum 32 characters
        rsid (str, optional): Received signal strength indicator from WiFi access point.
                             Number from -113 to 0 (dBm)
        speed (str, optional): Connection speed for WiFi.
                              Number from 0 to 6930 (Mbps)
        access_point (str, optional): JSON list of WiFi access points in device vicinity.
                                     Helpful for better location calculation with multiple access points
    
    Returns:
        dict: API response with location information or error information
        
    Note:
        Either mac or access_point parameter must be provided
    """
    try:
        api_instance = _get_api_client()
        
        # Prepare parameters - only include non-None values
        params = {}
        if mac is not None:
            params['mac'] = mac
        if ssid is not None:
            params['ssid'] = ssid
        if rsid is not None:
            params['rsid'] = rsid
        if speed is not None:
            params['speed'] = speed
        if access_point is not None:
            params['access_point'] = access_point
        
        # Call the API
        response = api_instance.get_location_by_wi_fi_access_point(**params)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract geometry information
        if hasattr(response, 'geometry') and response.geometry:
            geometry_dict = {}
            if hasattr(response.geometry, 'coordinates') and response.geometry.coordinates:
                geometry_dict['coordinates'] = response.geometry.coordinates
            if hasattr(response.geometry, 'type') and response.geometry.type:
                geometry_dict['type'] = response.geometry.type
            if hasattr(response.geometry, 'crs') and response.geometry.crs:
                crs_dict = {}
                if hasattr(response.geometry.crs, 'properties') and response.geometry.crs.properties:
                    crs_dict['properties'] = response.geometry.crs.properties
                if hasattr(response.geometry.crs, 'type') and response.geometry.crs.type:
                    crs_dict['type'] = response.geometry.crs.type
                geometry_dict['crs'] = crs_dict
            result["data"]["geometry"] = geometry_dict
        
        # Extract accuracy information
        if hasattr(response, 'accuracy') and response.accuracy:
            accuracy_dict = {}
            if hasattr(response.accuracy, 'unit') and response.accuracy.unit:
                accuracy_dict['unit'] = response.accuracy.unit
            if hasattr(response.accuracy, 'value') and response.accuracy.value:
                accuracy_dict['value'] = response.accuracy.value
            result["data"]["accuracy"] = accuracy_dict
        
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
def get_location_by_multiple_wifi_points(access_points_list):
    """
    Get geographic location based on multiple WiFi access points for better accuracy.
    
    Args:
        access_points_list (list): List of dictionaries containing WiFi access point information.
                                  Each dictionary can contain keys: mac, ssid, rsid, speed
    
    Returns:
        dict: API response with location information or error information
    """
    try:
        api_instance = _get_api_client()
        
        # Convert access points list to JSON string
        access_point_json = json.dumps(access_points_list)
        
        # Call the API with the JSON access points
        response = api_instance.get_location_by_wi_fi_access_point(access_point=access_point_json)
        
        # Convert response to dictionary format
        result = {
            "success": True,
            "data": {}
        }
        
        # Extract geometry information
        if hasattr(response, 'geometry') and response.geometry:
            geometry_dict = {}
            if hasattr(response.geometry, 'coordinates') and response.geometry.coordinates:
                geometry_dict['coordinates'] = response.geometry.coordinates
            if hasattr(response.geometry, 'type') and response.geometry.type:
                geometry_dict['type'] = response.geometry.type
            if hasattr(response.geometry, 'crs') and response.geometry.crs:
                crs_dict = {}
                if hasattr(response.geometry.crs, 'properties') and response.geometry.crs.properties:
                    crs_dict['properties'] = response.geometry.crs.properties
                if hasattr(response.geometry.crs, 'type') and response.geometry.crs.type:
                    crs_dict['type'] = response.geometry.crs.type
                geometry_dict['crs'] = crs_dict
            result["data"]["geometry"] = geometry_dict
        
        # Extract accuracy information
        if hasattr(response, 'accuracy') and response.accuracy:
            accuracy_dict = {}
            if hasattr(response.accuracy, 'unit') and response.accuracy.unit:
                accuracy_dict['unit'] = response.accuracy.unit
            if hasattr(response.accuracy, 'value') and response.accuracy.value:
                accuracy_dict['value'] = response.accuracy.value
            result["data"]["accuracy"] = accuracy_dict
        
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
def validate_ip_address(ip_address):
    """
    Validate if an IP address is in the correct format.
    
    Args:
        ip_address (str): IP address to validate
        
    Returns:
        bool: True if valid IPv4 format, False otherwise
    """
    import re
    
    # Basic IPv4 validation pattern
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    
    if not re.match(ipv4_pattern, ip_address):
        return False
    
    # Check if each octet is in valid range (0-255)
    octets = ip_address.split('.')
    for octet in octets:
        if not 0 <= int(octet) <= 255:
            return False
    
    return True


@mcp.tool()
def validate_mac_address(mac_address):
    """
    Validate if a MAC address is in the correct format.
    
    Args:
        mac_address (str): MAC address to validate
        
    Returns:
        bool: True if valid MAC format, False otherwise
    """
    import re
    
    # MAC address patterns with consistent separators
    mac_patterns = [
        r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$',  # With colons only
        r'^([0-9A-Fa-f]{2}-){5}([0-9A-Fa-f]{2})$',  # With hyphens only
        r'^([0-9A-Fa-f]{2}){6}$'  # Without separators
    ]
    
    for pattern in mac_patterns:
        if re.match(pattern, mac_address):
            return True
    
    return False
