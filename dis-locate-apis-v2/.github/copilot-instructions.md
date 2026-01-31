# Precisely MCP Server - AI Agent Instructions

## Architecture Overview

This is a **Model Context Protocol (MCP) server** exposing Precisely location intelligence APIs to AI assistants. Two-layer architecture:

1. **`precisely_api_core.py`** - Core API client with methods calling Precisely REST/GraphQL endpoints
2. **`mcp_servers/precisely_wrapper_server.py`** - MCP protocol wrapper exposing API methods as tools

**Data Flow**: MCP Client → `precisely_wrapper_server.py` (Tool definitions + routing) → `precisely_api_core.py` (HTTP calls) → Precisely Cloud APIs

**Key Files**:
- `precisely_api_core.py` - API methods (root folder)
- `mcp_servers/precisely_wrapper_server.py` - MCP tool definitions
- `implementation_user_prompts.txt` - User prompts for implementations (root folder)
- `.github/copilot-instructions.md` - These instructions

## Workflow for handling user requests:
1. User prompts are provided via chat or in `implementation_user_prompts.txt`
2. Each prompt has 3 sections: "user-request:", "status-updates-to-user:", "official-documentation:"
3. API try-out link is provided in "user-request:" section
4. Fetch OpenAPI spec from the try-out link to implement the MCP tool
5. "official-documentation:" contains copied documentation text (since pages are JS-rendered and cannot be fetched directly)
6. Use examples and field descriptions **verbatim** from OpenAPI spec and official-documentation - do not infer or customize
7. Include the "Request" example from OpenAPI spec inside method's docstring, like the `overlap` method in `precisely_api_core.py`
8. Use headers based on "Response Content-type:" in "official-documentation:". If conflict exists, ask user to choose
9. Include ALL "Request" examples from "official-documentation:" in Tool's `description` field, like the `overlap` Tool in `precisely_wrapper_server.py`
10. Do not include "Response" sections from examples
11. Provide status updates per "status-updates-to-user:" section

## Prompt Template

```
user-request:
Implement MCP tool for API at try-out link: https://developer.cloud.precisely.com/apis/products-try-out/[api_tryout_path]
status-updates-to-user:
[User instructions for status updates]
official-documentation:
[Copied documentation text including Request examples]
```

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
