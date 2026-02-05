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

## Implementation Rules (STRICT - Follow for EVERY prompt)

1. Process prompts from `implementation_user_prompts.txt` sequentially (user may specify starting line number)
2. For EACH prompt:
   a. Fetch OpenAPI spec from the try-out link FIRST
   b. Add method to `precisely_api_core.py` (match `overlap` method pattern EXACTLY)
   c. Add Tool to `precisely_wrapper_server.py` (match `overlap` Tool pattern EXACTLY)
   d. Update tool counts in ALL 4 locations (see Tool Count Updates section)
   e. Commit with message: "Added <tool_name>. Committed by GitHub Copilot"
3. Copy examples and field descriptions VERBATIM - NEVER invent or customize example data
4. If unsure, refer to `overlap` implementation as the canonical reference
5. After completing ALL prompts, push to remote

## Git Commit Rules (MANDATORY for EVERY commit)

**Files to commit:**
- `precisely_api_core.py` - Stage fully
- `mcp_servers/precisely_wrapper_server.py` - Stage EXCEPT line 48 (dev BASE_URL)

**Line 48 contains dev URL (NEVER commit):**
```python
BASE_URL = 'https://api-dev.cloud.precisely.services/'
```
Line 47 already has prod URL, so simply delete line 48 before commit, restore after.

**Before EVERY commit, execute these steps:**
1. Delete line 48 in `mcp_servers/precisely_wrapper_server.py` (the dev BASE_URL line)
2. Stage both files:
   ```bash
   git add precisely_api_core.py
   git add mcp_servers/precisely_wrapper_server.py
   ```
3. Commit:
   ```bash
   git commit -m "Added <tool_name>. Committed by GitHub Copilot"
   ```
4. Restore line 48 immediately after commit:
   ```python
   BASE_URL = 'https://api-dev.cloud.precisely.services/'
   ```
   (Add this line back after `BASE_URL = "https://api.cloud.precisely.com"`)

## Tool Count Updates (MANDATORY after EACH tool added)

Update the count in ALL 4 locations in `precisely_wrapper_server.py`:
1. Comment above `TOOLS` list: `# Tool definitions (XX tools...)`
2. `list_tools()` docstring: `"""List available tools (XX tools)..."""`
3. `run_stdio()` logger message
4. `run_http()` logger message

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
