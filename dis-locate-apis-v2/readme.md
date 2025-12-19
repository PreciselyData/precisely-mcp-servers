# Precisely MCP Server

A Model Context Protocol (MCP) server that exposes 48 Precisely location intelligence APIs to AI assistants like Claude Desktop, VS Code, Cursor, LangChain, LlamaIndex, and custom applications.

## Features

- **48 Production-Ready API Tools**: Complete location intelligence suite
- **Dual Transport Support**: stdio (default) and Streamable HTTP transports
- **MCP Protocol**: Standard interface for AI assistants  
- **100% Test Coverage**: Comprehensive unified test suite with 48/48 tests passing
- **Enhanced Documentation**: GraphQL tools with complete query examples
- **Clean Architecture**: Zero duplicate code, optimized implementation
- **Detailed Logging**: Full request/response logging for debugging

## Transport Options

The server supports two transport methods:

| Transport | Use Case | Command |
|-----------|----------|---------|
| **stdio** (default) | Claude Desktop, VS Code, Cursor, local CLI tools | `python precisely_wrapper_server.py` |
| **Streamable HTTP** | LangChain, LlamaIndex, web apps, remote access | `python precisely_wrapper_server.py --transport http` |

## Prerequisites

1. **Python 3.8+**
2. **Precisely API Credentials** - Get them at https://developer.precisely.com
3. **Claude Desktop** - Download at https://claude.ai/desktop (for stdio transport)

## Installation

### 1. Clone or Download Repository

```
git clone https://github.com/PreciselyData/precisely-mcp-servers/tree/main/dis-locate-apis-v2
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Core dependencies (always required):
- mcp>=1.0.0 - Model Context Protocol
- requests>=2.32.0 - HTTP requests
- python-dotenv>=1.0.0 - Environment management
- typing-extensions>=4.0.0 - Type hints

HTTP transport dependencies (optional, only for `--transport http`):
- starlette>=0.27.0 - ASGI framework
- uvicorn>=0.23.0 - ASGI server
- sse-starlette>=1.6.0 - Server-Sent Events
- anyio>=4.0.0 - Async utilities

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

```bash
cd mcp_servers
.\setup_claude_desktop.ps1
```

Or manually edit %APPDATA%\Claude\claude_desktop_config.json

Close and reopen Claude Desktop. Click the menu icon in the bottom-left corner to see 'precisely' in your connectors list.

## Usage

### Option 1: stdio Transport (Default)

Best for: Claude Desktop, VS Code, Cursor, local development

```bash
# Default - stdio transport
python mcp_servers/precisely_wrapper_server.py

# Show help
python mcp_servers/precisely_wrapper_server.py --help
```

**Claude Desktop Configuration** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "precisely": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp_servers\\precisely_wrapper_server.py"],
      "env": {
        "PRECISELY_API_KEY": "your_api_key",
        "PRECISELY_API_SECRET": "your_api_secret"
      }
    }
  }
}
```

**VS Code Configuration** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "precisely": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/mcp_servers/precisely_wrapper_server.py"],
      "env": {
        "PRECISELY_API_KEY": "${input:api-key}",
        "PRECISELY_API_SECRET": "${input:api-secret}"
      }
    }
  }
}
```

### Option 2: Streamable HTTP Transport

Best for: LangChain, LlamaIndex, web applications, remote access, multi-client scenarios

```bash
# Start HTTP server on default port 8000
python mcp_servers/precisely_wrapper_server.py --transport http

# Custom port
python mcp_servers/precisely_wrapper_server.py --transport http --port 8080

# Allow remote access (bind to all interfaces)
python mcp_servers/precisely_wrapper_server.py --transport http --host 0.0.0.0 --port 8000
```

**MCP Endpoint**: `http://localhost:8000/mcp`

#### Testing HTTP Transport

```powershell
# PowerShell - Initialize request
Invoke-WebRequest -Uri "http://127.0.0.1:8000/mcp" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Accept"="application/json, text/event-stream"} `
  -Body '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}'
```

#### Python MCP Client

**For Python scripts:**
```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def test_http():
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List all 48 tools
            tools = await session.list_tools()
            print(f"Available tools: {len(tools.tools)}")
            
            # Call geocode tool
            result = await session.call_tool("geocode", {
                "address": "1600 Pennsylvania Ave, Washington DC",
                "country": "USA"
            })
            print(result)

# For regular Python scripts
asyncio.run(test_http())
```

**For Jupyter notebooks:**
```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def test_http():
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List all 48 tools
            tools = await session.list_tools()
            print(f"Available tools: {len(tools.tools)}")
            
            # Call geocode tool
            result = await session.call_tool("geocode", {
                "address": "1600 Pennsylvania Ave, Washington DC",
                "country": "USA"
            })
            print(result)

# For Jupyter notebooks (use await directly)
await test_http()
```

#### LangChain Integration

```python
# pip install langchain-mcp-adapters
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def use_with_langchain():
    # Create client (no context manager needed)
    client = MultiServerMCPClient({
        "precisely": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http"
        }
    })
    
    # Get all 48 tools as LangChain tools
    tools = await client.get_tools()
    print(f"LangChain tools: {len(tools)} tools available")
    
    # Use tools with any LangChain agent
    # from langchain.agents import create_tool_calling_agent
    # agent = create_tool_calling_agent(llm, tools, prompt)

asyncio.run(use_with_langchain())
```

#### LlamaIndex Integration

```python
# pip install llama-index-tools-mcp
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from llama_index.tools.mcp import McpToolSpec

async def use_with_llamaindex():
    # Connect via MCP client and create tool spec
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Create LlamaIndex tool spec from session
            tool_spec = McpToolSpec(client=session)
            tools = await tool_spec.to_tool_list_async()
            print(f"LlamaIndex tools: {len(tools)} tools available")
            
            # Use with LlamaIndex agents
            # from llama_index.core.agent import ReActAgent
            # agent = ReActAgent.from_tools(tools, llm=llm)

asyncio.run(use_with_llamaindex())
```

### CLI Reference

```
usage: precisely_wrapper_server.py [-h] [--transport {stdio,http}] [--host HOST] [--port PORT]

Precisely MCP Server - Location Intelligence APIs

options:
  -h, --help            show this help message and exit
  --transport {stdio,http}
                        Transport type: stdio (default) or http
  --host HOST           HTTP host (default: 127.0.0.1, use 0.0.0.0 for remote access)
  --port PORT           HTTP port (default: 8000)

Examples:
  # stdio transport (default, for Claude Desktop)
  python precisely_wrapper_server.py

  # HTTP transport (for LangChain, LlamaIndex, web clients)
  python precisely_wrapper_server.py --transport http --port 8000

  # HTTP with custom host (for remote access)
  python precisely_wrapper_server.py --transport http --host 0.0.0.0 --port 8080
```

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
 requirements.txt                   # Python dependencies (core + HTTP transport)
 .env.template                      # Credential configuration template
 readme.md                          # This file
 mcp_servers/
    precisely_wrapper_server.py   # MCP server wrapper (840 lines, 48 tools, dual transport)
    setup_claude_desktop.ps1      # Windows setup script (UTF-8 no-BOM)
 logs/                              # Application logs (automatically generated)
 test_logs/                         # Test results and reports (automatically generated)
```

## Recent Changes (v9.0 - December 2025)

### Dual Transport Support

- Added Streamable HTTP transport alongside stdio
- CLI arguments for transport selection (`--transport`, `--host`, `--port`)
- Optional HTTP dependencies (graceful fallback for stdio-only users)
- Compatible with LangChain, LlamaIndex, and custom MCP clients

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

### Issue: HTTP transport not available

Solution:
1. Install HTTP dependencies: `pip install starlette uvicorn sse-starlette anyio`
2. Verify installation: `python -c "from mcp.server.streamable_http_manager import StreamableHTTPSessionManager; print('OK')"`

### Issue: Port already in use

Solution:
1. Use a different port: `python precisely_wrapper_server.py --transport http --port 8001`
2. Or stop the process using the port: `netstat -ano | findstr :8000`

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
- Dual transport support (stdio + HTTP)
- Comprehensive error handling
- Detailed logging (application + tests)
- Clean architecture (minimal dependencies)
- Zero duplicate code
- Well-documented APIs with complete examples
- Secure credential management
- Optimized file sizes
- Compatible with major AI frameworks (LangChain, LlamaIndex)

---

**Version**: 9.0 Production  
**Last Updated**: December 19, 2025  
**Tool Count**: 48 APIs  
**Transports**: stdio (default), Streamable HTTP  
**Test Coverage**: 100% (48/48 passing)
