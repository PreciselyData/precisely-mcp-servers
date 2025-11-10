# Precisely MCP Server

A Model Context Protocol (MCP) server that exposes 48 Precisely location intelligence APIs to AI assistants like Claude Desktop.

## Features

- **48 Production-Ready API Tools**: Complete location intelligence suite
- **MCP Protocol**: Standard interface for AI assistants  
- **100% Test Coverage**: Comprehensive unified test suite with 48/48 tests passing
- **Enhanced Documentation**: GraphQL tools with complete query examples
- **Clean Architecture**: Zero duplicate code, optimized implementation
- **Detailed Logging**: Full request/response logging for debugging

## Prerequisites

1. **Python 3.8+**
2. **Precisely API Credentials** - Get them at https://developer.precisely.com
3. **Claude Desktop** - Download at https://claude.ai/desktop

## Installation

### 1. Clone or Download Repository

```
git clone https://github.com/PreciselyData/precisely-mcp-servers/tree/main/dis-locate-apis-v2
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

Only 4 dependencies:
- mcp>=1.0.0 - Model Context Protocol
- requests>=2.32.0 - HTTP requests
- python-dotenv>=1.0.0 - Environment management
- typing-extensions>=4.0.0 - Type hints

### 3. Configure Credentials

```
# Copy the template
cp .env.template .env

# Edit .env with your credentials
# PRECISELY_API_KEY=your_api_key_here
# PRECISELY_API_SECRET=your_api_secret_here
```

### 4. Setup in Claude Desktop

For Windows PowerShell:

```
cd mcp_servers
.\setup_claude_desktop.ps1
```

Or manually edit %APPDATA%\Claude\claude_desktop_config.json

Close and reopen Claude Desktop. Click the menu icon in the bottom-left corner to see 'precisely' in your connectors list.

## Testing

### Unified Test Suite

Run the comprehensive 3-tier test suite:

```
python test_precisely_mcp.py
```

Test Architecture:

1. **Layer 1 - API Core**: Validates initialization and core functionality
2. **Layer 2 - MCP Server**: Verifies all 48 tools are properly defined
3. **Layer 3 - Functional**: Tests all 48 tools with real API calls

Test Features:

- Single unified test file
- 100% coverage (48/48 tools)
- Comprehensive logging (query, payload, response)
- Detailed test reports in test_logs/
- JSON results for CI/CD integration

Sample Output:

```
Layer 1 (API Core):      [PASS]
Layer 2 (MCP Server):    [PASS]
Layer 3 (Functional):    [PASS] 48/48 tests

Total:     48
Passed:    48
Failed:    0
Pass Rate: 100.0%
```

## Available APIs (48 Tools)

### Geocoding & Address (9 tools)

1. geocode - Convert address to coordinates
2. reverse_geocode - Convert coordinates to address
3. verify_address - Verify and standardize addresses
4. autocomplete - Address autocomplete suggestions
5. autocomplete_postal_city - Postal code and city autocomplete
6. autocomplete_v2 - Express autocomplete (V2)
7. lookup - Lookup address by PreciselyID
8. parse_address - Parse single address into components
9. parse_address_batch - Parse multiple addresses

### Property Information (7 tools)

10. get_property_data - Detailed property information
11. get_property_attributes_by_address - Property attributes
12. get_replacement_cost_by_address - Property replacement cost estimates
13. get_buildings_by_address - Building information
14. get_parcels_by_address - Parcel/lot information
15. get_neighborhoods_by_address - Neighborhood details
16. get_schools_by_address - Nearby schools information

### Risk Assessment (6 tools)

17. get_flood_risk_by_address - Flood zone and risk assessment
18. get_wildfire_risk_by_address - Wildfire risk analysis
19. get_earth_risk - Earthquake risk assessment
20. get_coastal_risk - Coastal hazard analysis
21. get_property_fire_risk - Fire risk assessment
22. get_historical_weather_risk - Historical weather patterns

### Demographics & Safety (4 tools)

23. get_demographics - Population and demographic data
24. get_crime_index - Crime statistics and safety index
25. get_psyte_geodemographics_by_address - Lifestyle segmentation
26. get_ground_view_by_address - Census block-level demographics

### Tax & Jurisdiction (10 tools)

27. lookup_by_address - Tax jurisdiction by address
28. lookup_by_location - Tax jurisdiction by coordinates
29. lookup_by_addresses - Batch tax jurisdiction lookup (addresses)
30. lookup_by_locations - Batch tax jurisdiction lookup (coordinates)
31. psap_address - Emergency services (911/PSAP) by address
32. psap_location - Emergency services by coordinates
33. psap_ahj_fccid - PSAP info by FCC ID
34. psap_ahj_address - Authority Having Jurisdiction by address
35. psap_ahj_location - Authority Having Jurisdiction by coordinates
36. geo_locate_ip_address - Geolocation by IP address

### Validation & Verification (3 tools)

37. verify_email - Email address verification
38. verify_batch_emails - Batch email verification
39. parse_name - Name parsing into components

### Phone Services (2 tools)

40. validate_phone - Phone number validation
41. validate_batch_phones - Batch phone validation

### Geolocation (1 tool)

42. geo_locate_wifi_access_point - WiFi access point geolocation

### Timezone (2 tools)

43. timezone_addresses - Get timezone for addresses
44. timezone_locations - Get timezone for coordinates

### GraphQL Advanced Queries (4 tools)

45. get_addresses_detailed - Comprehensive address details via GraphQL
46. get_parcel_by_owner_detailed - Parcel ownership queries via GraphQL
47. get_address_family - Related addresses via GraphQL
48. get_serviceability - Broadband/utility serviceability via GraphQL

## Project Structure

```
 precisely_api_core.py              # Core API implementation (1,672 lines, 48 methods)
 test_precisely_mcp.py              # Unified 3-tier test suite (596 lines, 48 tests)
 requirements.txt                   # Python dependencies (4 packages)
 .env.template                      # Credential configuration template
 readme.md                          # This file
 mcp_servers/
    precisely_wrapper_server.py   # MCP server wrapper (668 lines, 48 tools)
    setup_claude_desktop.ps1      # Windows setup script (UTF-8 no-BOM)
 logs/                              # Application logs(Automatically generated)
 test_logs/                         # Test results and reports(Automatically generated)
```

## Recent Changes (v8.0 - November 2025)

### Code Quality Improvements

- Removed 3 duplicate methods (145 lines saved)
- Enhanced 4 GraphQL tools with complete query examples
- Fixed 4 parameter structure mismatches
- Synchronized 20+ tool examples with test cases

### Architecture Changes

- Perfect tool alignment: 48 methods = 48 tools = 48 tests
- File size reductions: precisely_api_core.py 8% smaller
- Removed redundant files

### Bug Fixes

- Fixed UTF-8 BOM issue in setup_claude_desktop.ps1
- Standardized credential naming
- Updated test suite for 48 tools

## Configuration

Environment Variables:

```
PRECISELY_API_KEY=your_api_key_here
PRECISELY_API_SECRET=your_api_secret_here
PRECISELY_API_BASE_URL=https://api.cloud.precisely.com
```

Logging:

- Application logs: logs/app_uuid.log
- Test logs: test_logs/

## Troubleshooting

### Issue: 'precisely' not showing in Claude Desktop

Solution:
1. Verify claude_desktop_config.json syntax (valid JSON)
2. Check file encoding (UTF-8 without BOM)
3. Use absolute paths (not relative)
4. Restart Claude Desktop completely

### Issue: Authentication failures

Solution:
1. Verify credentials in .env file or claude_desktop_config.json
2. Check variable names: PRECISELY_API_KEY and PRECISELY_API_SECRET
3. Ensure no extra spaces or quotes
4. Test with: python test_precisely_mcp.py

### Issue: Import errors

Solution: pip install -r requirements.txt --upgrade

### Issue: Tool not found errors

Solution: Verify tool count matches 48

### Issue: Test failures

Solution:
1. Check API credentials are valid
2. Verify internet connectivity
3. Review test logs in test_logs/
4. Ensure all 48 methods exist in precisely_api_core.py

## Production-Ready Checklist

- 100% test coverage (48/48 tests passing)
- Comprehensive error handling
- Detailed logging (application + tests)
- Clean architecture (4 dependencies only)
- Zero duplicate code
- Well-documented APIs with complete examples
- Secure credential management
- Optimized file sizes

---

**Version**: 8.0 Production  
**Last Updated**: November 9, 2025  
**Tool Count**: 48 APIs  
**Test Coverage**: 100% (48/48 passing)
