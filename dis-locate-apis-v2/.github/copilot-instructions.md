# Precisely MCP Server - AI Agent Instructions

## Architecture Overview

This is a **Model Context Protocol (MCP) server** exposing Precisely location intelligence APIs to AI assistants. Two-layer architecture:

1. **`precisely_api_core.py`** - Core API client with methods calling Precisely REST/GraphQL endpoints
2. **`mcp_servers/precisely_wrapper_server.py`** - MCP protocol wrapper exposing API methods as tools

**Data Flow**: MCP Client → `precisely_wrapper_server.py` (Tool definitions + routing) → `precisely_api_core.py` (HTTP calls) → Precisely Cloud APIs

## Workflow for handling user requests:
1. Each user prompt will have 3 self-explanatory sections, "user-request:", "status-updates-to-user:", "official-documentation:"
2. API's https://developer.cloud.precisely.com/apis/products-try-out/ link which needs to be implemented as MCP tool is provided in "user-request:" section
3. Fetch and use the OpenAPI spec from the link provided in "user-request:" section to implement the MCP tool
4. Use examples and field descriptions **verbatim** from the fetched OpenAPI spec - do not infer or customize
5. Include the "Request" example from fetched OpenAPI spec inside method's docstring as a method call example, just like the code for overlap method in `precisely_api_core.py`
6. Use any headers required based on value of response "Content-type:", mentioned in "official-documentation:" section of the user prompt. In case of conflict, ask user to select from choices, highlighting recommendation
7. Include ALL "Request" examples found in "official-documentation:" section of the user prompt in Tool definition's `description` field, just like the code for overlap Tool in `precisely_wrapper_server.py`
8. Do not include the "Response" section of examples
9. Provide status updates to user according to "status-updates-to-user:" section of the user prompt

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

### GraphQL APIs
Many tools use GraphQL via `/data-graph/graphql`. Query structure is embedded in method implementations. See `get_property_data()`, `get_flood_risk_by_address()` for patterns.

## Development Commands

```bash
# Install dependencies
py -m pip install -r requirements.txt

# Run MCP server (stdio - for Claude Desktop/VS Code)
py mcp_servers/precisely_wrapper_server.py

# Run MCP server (HTTP - for LangChain/web apps)
py mcp_servers/precisely_wrapper_server.py --transport http --port 8000

# Run test suite
py test_precisely_mcp.py
```

## VS Code MCP Configuration

Edit `.vscode/mcp.json` to configure credentials. Switch between prod/dev by commenting/uncommenting credential blocks. **Restart MCP server after credential changes**.

## Logging

Logs written to `logs/app_<uuid>.log` with RotatingFileHandler (10MB, 5 backups). Enable DEBUG level for full request/response logging.

## Common Issues

- **503/404 on spatial APIs**: Check if credentials have spatial API access (dev vs prod)
- **"No acceptable representation"**: Missing `Accept: application/geo+json` header for spatial endpoints
- **Tool disabled errors**: Restart MCP server after code changes
