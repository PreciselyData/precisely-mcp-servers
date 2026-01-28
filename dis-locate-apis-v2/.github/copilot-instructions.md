# Precisely MCP Server - AI Agent Instructions

## Architecture Overview

This is a **Model Context Protocol (MCP) server** exposing Precisely location intelligence APIs to AI assistants. Two-layer architecture:

1. **`precisely_api_core.py`** - Core API client with 52 methods calling Precisely REST/GraphQL endpoints
2. **`mcp_servers/precisely_wrapper_server.py`** - MCP protocol wrapper exposing API methods as tools

**Data Flow**: MCP Client → `precisely_wrapper_server.py` (Tool definitions + routing) → `precisely_api_core.py` (HTTP calls) → Precisely Cloud APIs

## Adding New API Tools

When adding a new Precisely API endpoint as a tool:

1. **Add method to `precisely_api_core.py`**:
   ```python
   def new_method(self, param1: str, param2: Dict, **kwargs) -> Dict[str, Any]:
       """Docstring describing the API"""
       url = f"{self.base_url}/v1/endpoint"
       # For spatial APIs, use Accept: application/geo+json header
       headers = {"Accept": "application/geo+json"}  # Only for spatial endpoints
       response = self.session.post(url, json=json_data, headers=headers)
       return response.json()
   ```

2. **Add Tool definition to `precisely_wrapper_server.py`** in the `TOOLS` list:
   ```python
   Tool(
       name="new_method",  # Must match method name in core module
       description="Description with example JSON payloads",
       inputSchema={...}  # JSON Schema matching method parameters
   )
   ```

3. **Update tool counts** in: comment at `TOOLS`, `list_tools()` docstring, `run_stdio()`, `run_http()`

## Critical Patterns

### Authentication
- Uses Base64-encoded `api_key:api_secret` in `Authorization: Apikey <encoded>` header
- Credentials from environment variables: `PRECISELY_API_KEY`, `PRECISELY_API_SECRET`

### Spatial API Headers
Spatial endpoints (`/v1/spatial/*`) require `Accept: application/geo+json` header:
- `find_nearest_candidates` - `/v1/spatial/findNearest`
- `search_at_location` - `/v1/spatial/searchAtLocation`  
- `overlap` - `/v1/spatial/overlap`

### GraphQL APIs
Many tools use GraphQL via `/data-graph/graphql`. Query structure is embedded in method implementations. See `get_property_data()`, `get_flood_risk_by_address()` for patterns.

### Location Formats
```python
# WKT format (spatial APIs)
location = {"format": "WKT", "value": "POINT(-118.25 34.05)"}  # lon, lat order

# Address format
location = {"format": "ADDRESS", "value": "123 Main St, City, ST"}
```

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run MCP server (stdio - for Claude Desktop/VS Code)
python mcp_servers/precisely_wrapper_server.py

# Run MCP server (HTTP - for LangChain/web apps)
python mcp_servers/precisely_wrapper_server.py --transport http --port 8000

# Run test suite
python test_precisely_mcp.py
```

## VS Code MCP Configuration

Edit `.vscode/mcp.json` to configure credentials. Switch between prod/dev by commenting/uncommenting credential blocks. **Restart MCP server after credential changes**.

## Logging

Logs written to `logs/app_<uuid>.log` with RotatingFileHandler (10MB, 5 backups). Enable DEBUG level for full request/response logging.

## Common Issues

- **503/404 on spatial APIs**: Check if credentials have spatial API access (dev vs prod)
- **"No acceptable representation"**: Missing `Accept: application/geo+json` header for spatial endpoints
- **Tool disabled errors**: Restart MCP server after code changes
