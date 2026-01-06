"""
Unified Test Suite for Precisely MCP Server
Combines 3-tier testing: Layer 1 (API Core) → Layer 2 (MCP Server) → Layer 3 (Functional)

Tests all 49 Precisely API tools with comprehensive validation and detailed logging
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import time

# Add parent directory and MCP server directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp_servers'))

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

from precisely_api_core import PreciselyAPI

# Configure logging
test_log_dir = "test_logs"
os.makedirs(test_log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(test_log_dir, f"unified_test_{timestamp}.log")

logger = logging.getLogger("precisely_mcp_test")
logger.setLevel(logging.DEBUG)

# File handler (DEBUG level - logs everything)
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Console handler (INFO level - key information only)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


@dataclass
class TestResult:
    """Represents a test result"""
    test_name: str
    method_name: str
    description: str
    status: str  # PASSED, FAILED, SKIPPED
    duration_ms: float
    query: Optional[str] = None
    payload: Optional[Dict] = None
    response: Optional[Any] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PreciselyMCPTestSuite:
    """Unified test suite for Precisely MCP Server"""
    
    def __init__(self):
        self.api: Optional[PreciselyAPI] = None
        self.results: List[TestResult] = []
        self.layer1_passed = False
        self.layer2_passed = False
        
    def log_separator(self, char="=", length=80):
        """Log a separator line"""
        logger.info(char * length)
    
    def log_header(self, title: str):
        """Log a section header"""
        self.log_separator()
        logger.info(title.center(80))
        self.log_separator()
    
    # ========================================
    # LAYER 1: API Core Testing
    # ========================================
    
    def test_layer1_api_core(self) -> bool:
        """
        Layer 1: Test the foundation - can we call Precisely APIs?
        - Initialize API
        - Verify all 49 methods exist
        - Run sample tests to validate API responses
        """
        self.log_header("LAYER 1: API CORE TESTING")
        
        # Test 1: API Initialization
        logger.info("\n[1/3] Testing API Initialization...")
        api_key = os.getenv("PRECISELY_API_KEY") or os.getenv("API_KEY")
        api_secret = os.getenv("PRECISELY_API_SECRET") or os.getenv("PRECISELY_SECRET") or os.getenv("API_SECRET")
        
        if not api_key or not api_secret:
            logger.error("  [FAIL] API credentials not found in .env file")
            return False
        
        try:
            self.api = PreciselyAPI(api_key, api_secret)
            logger.info("  [PASS] API initialized successfully")
        except Exception as e:
            logger.error(f"  [FAIL] API initialization failed: {e}")
            return False
        
        # Test 2: Verify all methods exist
        logger.info("\n[2/3] Verifying API Methods...")
        methods = [m for m in dir(self.api) if not m.startswith('_') and callable(getattr(self.api, m))]
        logger.info(f"  Found {len(methods)} API methods")
        
        if len(methods) != 49:
            logger.warning(f"  [WARN] Expected 49 methods, found {len(methods)}")
        else:
            logger.info("  [PASS] All 49 API methods present")
        
        # Test 3: Quick smoke tests
        logger.info("\n[3/3] Running Quick Smoke Tests...")
        sample_tests = [
            ("geocode", lambda: self.api.geocode(address="1600 Pennsylvania Ave NW, Washington DC", country="USA")),
            ("verify_address", lambda: self.api.verify_address(address="1600 Pennsylvania Ave NW, Washington DC", country="USA")),
            ("verify_email", lambda: self.api.verify_email(email="test@example.com")),
        ]
        
        passed = 0
        for name, test_func in sample_tests:
            try:
                result = test_func()
                if result and not result.get("error"):
                    logger.info(f"  [PASS] {name}")
                    passed += 1
                else:
                    logger.warning(f"  [FAIL] {name}: {result.get('error', 'No response')}")
            except Exception as e:
                logger.warning(f"  [FAIL] {name}: {str(e)[:80]}")
        
        logger.info(f"\nLayer 1 Summary: {passed}/{len(sample_tests)} smoke tests passed")
        self.layer1_passed = (passed == len(sample_tests))
        return self.layer1_passed
    
    # ========================================
    # LAYER 2: MCP Server Testing
    # ========================================
    
    def test_layer2_mcp_server(self) -> bool:
        """
        Layer 2: Test the wrapper - are all tools exposed via MCP?
        - Load MCP server module
        - Verify 49 tool definitions
        - Cross-reference MCP tools with API methods
        """
        self.log_header("LAYER 2: MCP SERVER TESTING")
        
        logger.info("\n[1/2] Loading MCP Server Tool Definitions...")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "precisely_wrapper_server",
                "mcp_servers/precisely_wrapper_server.py"
            )
            server_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(server_module)
            
            tools = server_module.TOOLS
            logger.info(f"  [PASS] MCP server loaded: {len(tools)} tools defined")
            
            # Check for duplicates
            tool_names = [tool.name for tool in tools]
            duplicates = [name for name in tool_names if tool_names.count(name) > 1]
            
            if duplicates:
                logger.error(f"  [FAIL] Duplicate tools found: {set(duplicates)}")
                return False
            
            if len(tools) != 49:
                logger.warning(f"  [WARN] Expected 49 tools, found {len(tools)}")
            else:
                logger.info("  [PASS] All 49 MCP tools defined")
            
        except Exception as e:
            logger.error(f"  [FAIL] Failed to load MCP server: {e}")
            return False
        
        # Test 2: Cross-reference with API
        logger.info("\n[2/2] Cross-Referencing MCP Tools with API Methods...")
        
        api_methods = set([m for m in dir(self.api) if not m.startswith('_') and callable(getattr(self.api, m))])
        mcp_tools = set([tool.name for tool in tools])
        
        tools_not_in_api = mcp_tools - api_methods
        api_not_in_tools = api_methods - mcp_tools
        
        if tools_not_in_api:
            logger.warning(f"  [WARN] MCP tools without API methods: {tools_not_in_api}")
        
        if api_not_in_tools:
            logger.warning(f"  [WARN] API methods without MCP tools: {api_not_in_tools}")
        
        if not tools_not_in_api and not api_not_in_tools:
            logger.info("  [PASS] Perfect alignment: MCP tools <-> API methods")
            self.layer2_passed = True
        else:
            logger.warning("  [WARN] Alignment issues detected")
            self.layer2_passed = False
        
        return self.layer2_passed
    
    # ========================================
    # LAYER 3: Comprehensive Functional Testing
    # ========================================
    
    def run_functional_test(self, test_name: str, method_name: str, description: str, 
                           test_input: Dict[str, Any]) -> TestResult:
        """
        Run a single functional test with detailed logging
        Logs: query/description, payload/input, response/output
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"TEST: {test_name}")
        logger.info(f"Method: {method_name}")
        logger.info(f"Description: {description}")
        
        # Log the payload/input
        logger.info(f"Input: {json.dumps(test_input, indent=2)}")
        logger.debug(f"Full input parameters: {test_input}")
        
        start_time = time.time()
        
        try:
            # Get the API method
            if not hasattr(self.api, method_name):
                raise AttributeError(f"API method '{method_name}' not found")
            
            method = getattr(self.api, method_name)
            logger.info(f"Calling API method: {method_name}...")
            
            # Call the method
            response = method(**test_input)
            duration_ms = (time.time() - start_time) * 1000
            
            # Log the response
            logger.debug(f"Response: {json.dumps(response, indent=2, default=str)}")
            
            # Validate response
            if response is None:
                raise ValueError("API returned None")
            
            if isinstance(response, dict) and response.get("error"):
                error_msg = response["error"]
                logger.info(f"[FAIL] {error_msg} ({duration_ms:.0f}ms)")
                return TestResult(
                    test_name=test_name,
                    method_name=method_name,
                    description=description,
                    status="FAILED",
                    duration_ms=duration_ms,
                    query=description,
                    payload=test_input,
                    response=response,
                    error=error_msg
                )
            
            # Success
            logger.info(f"[PASS] ({duration_ms:.0f}ms)")
            return TestResult(
                test_name=test_name,
                method_name=method_name,
                description=description,
                status="PASSED",
                duration_ms=duration_ms,
                query=description,
                payload=test_input,
                response=response
            )
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = str(e)
            logger.info(f"[FAIL] {error_msg[:100]} ({duration_ms:.0f}ms)")
            logger.debug(f"Exception details: {error_msg}")
            
            return TestResult(
                test_name=test_name,
                method_name=method_name,
                description=description,
                status="FAILED",
                duration_ms=duration_ms,
                query=description,
                payload=test_input,
                error=error_msg
            )
    
    def test_layer3_functional(self) -> bool:
        """
        Layer 3: Comprehensive functional testing
        - Test all 49 tools with real API calls
        - Validate responses
        - Log every query, payload, and response
        """
        self.log_header("LAYER 3: COMPREHENSIVE FUNCTIONAL TESTING")
        
        logger.info(f"\nRunning {len(self.get_test_cases())} functional tests...")
        logger.info("Each test logs: Query -> Payload -> Response\n")
        
        test_cases = self.get_test_cases()
        
        for i, (name, method, desc, input_data) in enumerate(test_cases, 1):
            logger.info(f"\n[{i}/{len(test_cases)}]")
            result = self.run_functional_test(name, method, desc, input_data)
            self.results.append(result)
        
        # Generate summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASSED")
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        total_duration = sum(r.duration_ms for r in self.results)
        avg_duration = total_duration / total if total > 0 else 0
        
        self.log_separator()
        logger.info("TEST SUMMARY")
        self.log_separator()
        logger.info(f"Total:     {total}")
        logger.info(f"[PASS] Passed:  {passed}")
        logger.info(f"[FAIL] Failed:  {failed}")
        logger.info(f"Pass Rate: {pass_rate:.1f}%")
        logger.info(f"Duration:  {total_duration:.0f}ms (avg: {avg_duration:.0f}ms)")
        logger.info("")
        
        if failed > 0:
            logger.info("Failed Tests:")
            for r in self.results:
                if r.status == "FAILED":
                    logger.info(f"  [FAIL] {r.test_name} - {r.error}")
            logger.info("")
        
        self.log_separator()
        logger.info(f"Log saved: {log_filename}")
        self.log_separator()
        
        # Save JSON results
        json_file = log_filename.replace(".log", "_results.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "pass_rate": round(pass_rate, 2),
                    "total_duration_ms": round(total_duration, 2),
                    "avg_duration_ms": round(avg_duration, 2)
                },
                "results": [r.to_dict() for r in self.results],
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, default=str)
        
        logger.info(f"Results saved: {json_file}")
        
        return failed == 0
    
    def get_test_cases(self) -> List[tuple]:
        """
        Get all test cases (name, method, description, input)
        Test cases copied from automated_api_tests.py
        """
        return [
            # Name/Phone/Email Validation
            ("Parse Name", "parse_name", "Parse the name John Robert Smith into components",
             {"data": {"name": "John Robert Smith"}}),
            
            ("Validate Phone Number", "validate_phone", "Is 4144654885 a valid phone number in the US?",
             {"data": {"phoneNumber": "4144654885", "country": "US"}}),
            
            ("Validate Batch Phones", "validate_batch_phones", "Validate multiple phone numbers: 3035551234, 7205559999",
             {"data": {"phoneNumbers": [{"id": "1", "phoneNumber": "3035551234", "country": "US"}, {"id": "2", "phoneNumber": "7205559999", "country": "US"}]}}),
            
            ("Verify Email", "verify_email", "Is john.doe@company.com a valid email?",
             {"email": "john.doe@company.com"}),
            
            ("Verify Batch Emails", "verify_batch_emails", "Verify multiple emails: john@company.com, jane@company.com",
             {"emails": [{"id": "1", "email": "john@company.com"}, {"id": "2", "email": "jane@company.com"}]}),
            
            # Timezone
            ("Timezone by Address", "timezone_addresses", "What is the timezone for 1700 District Ave, Burlington, MA?",
             {"data": {"addresses": [{"timestamp": 1691138974831, "address": {"id": "1", "addressLines": ["1700 District Ave, Burlington, MA"], "country": "USA"}}]}}),
            
            ("Timezone by Location", "timezone_locations", "What is the timezone for coordinates -71.0589, 42.3601?",
             {"data": {"locations": [{"id": "1", "timestamp": 1691138974831, "geometry": {"coordinates": [-71.0589, 42.3601]}}]}}),
            
            # Geocoding & Address Services
            ("Geocode Address", "geocode", "What are the coordinates of 42 Valley Of The Sun Dr, Fairplay, CO 80440?",
             {"address": "42 Valley Of The Sun Dr, Fairplay, CO 80440", "country": "USA"}),
            
            ("Reverse Geocode", "reverse_geocode", "What is the address at coordinates 39.5501, -105.9999?",
             {"lat": 39.5501, "lon": -105.9999, "country": "USA"}),
            
            ("Verify Address", "verify_address", "Is 1600 Pennsylvania Ave, Washington DC a valid address?",
             {"address": "1600 Pennsylvania Ave, Washington DC", "country": "USA"}),
            
            ("Parse Address", "parse_address", "Parse 1700 District Ave #300, Burlington, MA 01803 into components",
             {"address": "1700 District Ave #300, Burlington, MA 01803"}),
            
            ("Parse Address Batch", "parse_address_batch", "Parse multiple addresses: 123 Main St Boston MA, 456 Oak Ave Denver CO",
             {"addresses": [{"id": "1", "address": "123 Main St, Boston, MA 02101"}, {"id": "2", "address": "456 Oak Ave, Denver, CO 80203"}]}),
            
            ("Autocomplete Address", "autocomplete", "Autocomplete address starting with 1700 District",
             {"address": {"addressLines": ["1700 District"], "country": "USA"}, "preferences": {"maxResults": 5}}),
            
            ("Autocomplete Postal City", "autocomplete_postal_city", "Autocomplete postal code 12180 in the USA",
             {"address": {"type": "POSTAL", "postAddress": "12180", "country": "USA"}, "preferences": {"maxResults": 5}}),
            
            ("Autocomplete V2", "autocomplete_v2", "Give me express autocomplete suggestions for 350 Jordan Street, USA",
             {"address": {"addressLines": ["350 Jordan"], "country": "USA"}, "preferences": {"maxResults": 5}}),
            
            ("Lookup by PreciselyID", "lookup", "Lookup address for PreciselyID P0000GL41OME",
             {"keys": [{"key": "P0000GL41OME", "country": "USA", "type": "PB_KEY"}]}),
            
            ("Lookup by Address", "lookup_by_address", "Get tax jurisdiction for 123 Main St, Boston, MA",
             {"address": {"addressLines": ["123 Main St, Boston, MA"]}}),
            
            ("Lookup by Location", "lookup_by_location", "Get tax jurisdiction for coordinates -71.0589, 42.3601",
             {"location": {"longitude": -71.0589, "latitude": 42.3601}}),
            
            ("Lookup Batch by Addresses", "lookup_by_addresses", "Get tax jurisdictions for multiple addresses",
             {"addresses": [{"addressLines": ["2001 Main St, Eagle Butte, SD 57625"]}, {"addressLines": ["2520 Columbia House Blvd #108, Vancouver, WA 98661"]}], "preferences": {}}),
            
            ("Lookup Batch by Locations", "lookup_by_locations", "Find tax jurisdictions for multiple coordinates",
             {"locations": [{"longitude": -98.401796, "latitude": 34.688726}, {"longitude": -92.9036, "latitude": 34.8192}], "preferences": {}}),
            
            # Geolocation
            ("Geolocate IP Address", "geo_locate_ip_address", "Where is IP address 8.8.8.8 located?",
             {"ip_address": "8.8.8.8"}),
            
            ("Geolocate WiFi Access Point", "geo_locate_wifi_access_point", "Geolocate WiFi access point with MAC address 00:22:75:10:d5:91",
             {"wifi_data": {"servingCell": {"mac": "00:22:75:10:d5:91", "rssi": "-90"}}}),
            
            # Emergency Services (PSAP)
            ("PSAP by Address", "psap_address", "What is the 911 service for 860 White Plains Road Trumbull CT 06611?",
             {"address": {"addressLines": ["860 White Plains Road"], "city": "Trumbull", "admin1": "CT", "postalCode": "06611"}}),
            
            ("PSAP by Location", "psap_location", "What is the 911 service for coordinates -71.0589, 42.3601?",
             {"location": {"coordinates": [-71.0589, 42.3601]}}),
            
            ("PSAP by FCC ID", "psap_ahj_fccid", "Get PSAP information for FCC ID 1404",
             {"fcc_id": "1404"}),
            
            ("PSAP AHJ by Address", "psap_ahj_address", "Get Authority Having Jurisdiction for 860 White Plains Road Trumbull CT 06611",
             {"address": {"addressLines": ["860 White Plains Road"], "city": "Trumbull", "admin1": "CT", "postalCode": "06611"}}),
            
            ("PSAP AHJ by Location", "psap_ahj_location", "Get Authority Having Jurisdiction for coordinates -71.0589, 42.3601",
             {"location": {"coordinates": [-71.0589, 42.3601]}}),
            
            # Property Information
            ("Get Property Data", "get_property_data", "What are the property details for 42 Valley Of The Sun Dr, Fairplay, CO 80440?",
             {"address": "42 Valley Of The Sun Dr, Fairplay, CO 80440", "country": "US"}),
            
            ("Get Detailed Address Info", "get_addresses_detailed", "Get comprehensive address details for 2755 Milwaukee St in Denver using GraphQL",
             {"data": {"query": "query GetAddressDetailed($address: String!, $country: String) { getByAddress(address: $address, country: $country) { addresses { data { preciselyID addressNumber streetName city admin1ShortName postalCode } } } }", "variables": {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}}}),
            
            ("Get Buildings by Address", "get_buildings_by_address", "What building information is available for 123 Main St, Boston, MA?",
             {"address": "123 Main St, Boston, MA", "country": "US"}),
            
            ("Get Parcels by Address", "get_parcels_by_address", "What parcel information is available for 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Parcel by Owner Detailed", "get_parcel_by_owner_detailed", "Find parcel information for owner with PreciselyID P0000GL41OME",
             {"data": {"query": "query GetParcelByOwner($id: String, $queryType: QueryType, $address: String, $distance: Float, $limit: Int) { getParcelByOwner(id: $id, queryType: $queryType, address: $address, distance: $distance, limit: $limit) { parcels { metadata { pageNumber pageCount totalPages count vintage } data { parcelID fips geographyID apn parcelArea longitude latitude elevation } } } }", "variables": {"id": "P0000GL41OME", "queryType": "PRECISELY_ID", "address": "Boston, MA", "distance": 1000.0, "limit": 50}}}),
            
            ("Get Neighborhoods", "get_neighborhoods_by_address", "What neighborhood is 123 Main St, Boston, MA in?",
             {"address": "123 Main St, Boston, MA", "country": "US"}),
            
            ("Get Schools by Address", "get_schools_by_address", "What schools are near 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            # Risk Assessment
            ("Get Wildfire Risk by Address", "get_wildfire_risk_by_address", "What is the wildfire risk at 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Earthquake Risk", "get_earth_risk", "What is the earthquake risk for 123 Main St, San Francisco, CA?",
             {"address": "123 Main St, San Francisco, CA", "country": "US"}),
            
            ("Get Coastal Risk", "get_coastal_risk", "What is the coastal risk for 100 Ocean Drive, Miami Beach, FL?",
             {"address": "100 Ocean Drive, Miami Beach, FL", "country": "US"}),
            
            ("Get Flood Risk by Address", "get_flood_risk_by_address", "Check flood risk for 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Fire Risk", "get_property_fire_risk", "What is the fire risk for 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Historical Weather Risk", "get_historical_weather_risk", "What historical weather risks exist for 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            # Demographics & Safety
            ("Get Demographics", "get_demographics", "What are the demographics for 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Crime Index", "get_crime_index", "What is the crime index for 42 Valley Of The Sun Dr, Fairplay, CO 80440?",
             {"address": "42 Valley Of The Sun Dr, Fairplay, CO 80440", "country": "US"}),
            
            ("Get PSYTE Geodemographics", "get_psyte_geodemographics_by_address", "What lifestyle segment lives at 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Ground View Demographics", "get_ground_view_by_address", "Show me census-level demographics for 999 Lake Shore Drive, Chicago, IL",
             {"address": "999 Lake Shore Drive, Chicago, IL", "country": "US"}),
            
            # Additional Property Services
            ("Get Replacement Cost", "get_replacement_cost_by_address", "What is the property replacement cost for 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            ("Get Property Attributes", "get_property_attributes_by_address", "How many bedrooms and bathrooms are at 2755 Milwaukee St, Denver, 80238 CO?",
             {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}),
            
            # GraphQL Advanced Queries
            ("Get Address Family", "get_address_family", "Show me related addresses for PreciselyID P00003PYY08O",
             {"data": {"query": "query GetAddressFamily($id: String!, $queryType: QueryType!) { getById(id: $id, queryType: $queryType) { addresses { data { preciselyID addressFamily(pageNumber: 1, pageSize: 20) { metadata { pageNumber pageCount totalPages count vintage } data { preciselyID addressNumber streetName city admin1ShortName postalCode } } } } } }", "variables": {"id": "P00003PYY08O", "queryType": "PRECISELY_ID"}}}),
            
            ("Get Serviceability", "get_serviceability", "What broadband services are available at 2755 Milwaukee St, Denver, 80238 CO?",
             {"data": {"query": "query GetServiceability($address: String!, $country: String) { getByAddress(address: $address, country: $country) { addresses(pageNumber: 1, pageSize: 1) { data { preciselyID serviceability { metadata { pageNumber pageCount totalPages count vintage } data { serviceabilityID preciselyID serviceableAddress } } } } } }", "variables": {"address": "2755 Milwaukee St, Denver, 80238 CO", "country": "US"}}}),
            
            ("Get Places by Address", "get_places_by_address", "What places and points of interest are near 123 Main St, Boston, MA 02101?",
             {"data": {"query": "query GetPlacesByAddress($address: String!, $country: String) { getByAddress(address: $address, country: $country) { places(pageNumber: 1, pageSize: 20) { metadata { pageNumber pageCount totalPages count vintage } data { PBID pointOfInterestID preciselyID businessName brandName city admin1ShortName postalCode formattedAddress longitude latitude phone email web lineOfBusiness sic8Description } } } }", "variables": {"address": "123 Main St, Boston, MA 02101", "country": "US"}}}),
        ]
    
    # ========================================
    # Main Test Runner
    # ========================================
    
    def run_all(self):
        """Run all 3 layers of testing"""
        self.log_header("PRECISELY MCP SERVER - UNIFIED TEST SUITE")
        logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Test Layers: 3 (API Core -> MCP Server -> Functional)")
        logger.info("")
        
        # Layer 1: API Core
        if not self.test_layer1_api_core():
            logger.error("\n[CRITICAL] Layer 1 failed - cannot proceed")
            return False
        
        # Layer 2: MCP Server
        if not self.test_layer2_mcp_server():
            logger.warning("\n[WARNING] Layer 2 issues detected - proceeding with caution")
        
        # Layer 3: Functional Tests
        success = self.test_layer3_functional()
        
        # Final summary
        self.log_separator("=")
        logger.info("FINAL SUMMARY")
        self.log_separator("=")
        logger.info(f"Layer 1 (API Core):      {'[PASS]' if self.layer1_passed else '[FAIL]'}")
        logger.info(f"Layer 2 (MCP Server):    {'[PASS]' if self.layer2_passed else '[WARN]'}")
        logger.info(f"Layer 3 (Functional):    {'[PASS]' if success else '[FAIL]'}")
        self.log_separator("=")
        
        return success


def main():
    """Main entry point"""
    try:
        suite = PreciselyMCPTestSuite()
        success = suite.run_all()
        
        print(f"\n{'='*80}")
        if success:
            print("[OK] All tests passed!")
        else:
            print("[FAIL] Some tests failed - check log for details")
        print(f"Log: {log_filename}")
        print(f"{'='*80}\n")
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n[ERROR] Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
