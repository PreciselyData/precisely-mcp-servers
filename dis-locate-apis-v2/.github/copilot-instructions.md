# Precisely MCP Server - AI Agent Instructions

## Architecture Overview

This is a **Model Context Protocol (MCP) server** exposing Precisely location intelligence APIs to AI assistants. Two-layer architecture:

1. **`precisely_api_core.py`** - Core API client with methods calling Precisely REST/GraphQL endpoints
2. **`mcp_servers/precisely_wrapper_server.py`** - MCP protocol wrapper exposing API methods as tools

**Data Flow**: MCP Client → `precisely_wrapper_server.py` (Tool definitions + routing) → `precisely_api_core.py` (HTTP calls) → Precisely Cloud APIs

**Key Files**:
- `precisely_api_core.py` - API methods (root folder)
- `mcp_servers/precisely_wrapper_server.py` - MCP tool definitions
- `test_precisely_mcp.py` - Unified 3-tier test suite (root folder)
- `readme.md` - Project documentation with tool list (root folder)
- `implementation_user_prompts.txt` - User prompts for implementations (root folder)
- `.github/copilot-instructions.md` - These instructions

## Two Distinct Example Sources (CRITICAL - Do NOT Confuse)

There are TWO separate sources of example data. They serve DIFFERENT purposes and go to DIFFERENT files. NEVER mix them up:

### Source 1: OpenAPI Spec Examples (from the try-out link)
- **Where to find**: Fetch the OpenAPI spec from the try-out link URL provided in "user-request:" section
- **Where they go**:
  1. `precisely_api_core.py` — Use the OpenAPI spec example's "Request" values as arguments in a sample method call inside the method's docstring
  2. `test_precisely_mcp.py` — Use the SAME OpenAPI spec example's "Request" values as test input arguments in `get_test_cases()`
- **Rule**: Copy values VERBATIM from the OpenAPI spec. Do NOT infer, customize, or substitute with values from user-prompt examples

### Source 2: User-Prompt Examples (from "all-examples-to-include-in-tool-description-field:" section)
- **Where to find**: The "all-examples-to-include-in-tool-description-field:" section of each user prompt
- **Where they go**: ONLY into the Tool's `description` field in `precisely_wrapper_server.py`
- **Rule**: Include ALL examples. Each example has "Request" and "Response" sections — include ONLY the "Request" sections. Copy verbatim without any modifications or customizations. Do NOT include "Response" sections.
- **NEVER use these as**: test case inputs, method docstring examples, or anywhere other than the Tool `description` field

### Why This Matters
User-prompt examples and OpenAPI spec examples often contain SIMILAR but DIFFERENT request payloads (different table names, geometries, coordinates, parameters). Using user-prompt examples as test inputs or docstring examples is WRONG — they must ONLY appear in the Tool `description`. The OpenAPI spec is the SOLE source for test cases and docstring example calls.

## Workflow for handling user requests:
1. User prompts are provided via chat or in `implementation_user_prompts.txt`
2. Each prompt has 3 sections: "user-request:", "status-updates-to-user:", "all-examples-to-include-in-tool-description-field:"
3. API try-out link is provided in "user-request:" section
4. Fetch OpenAPI spec from the try-out link to implement the MCP tool
5. Use entire API description, and entire field descriptions VERBATIM from OpenAPI spec - do not infer or customize
6. Section "all-examples-to-include-in-tool-description-field:" contains examples to be included ONLY in Tool's `description` field in `precisely_wrapper_server.py`. Include ALL examples. Each example has "Request" and "Response" section - include only the "Request" section. Do NOT include "Response" sections. Copy verbatim without any modifications or customizations. Do NOT use these examples anywhere else (not in test cases, not in docstrings)
7. Use values from OpenAPI spec example's "Request" section as arguments of `precisely_api_core.py` method call AND as test input arguments in `test_precisely_mcp.py`. Do NOT infer or customize argument values. Do NOT substitute with values from user-prompt examples
8. Use appropriate headers. For example, for `overlap` API, "Accept" header should be "application/geo+json"
9. Provide status updates per "status-updates-to-user:" section

## Prompt Template

```
user-request:
Implement MCP tool for API at try-out link: https://developer.cloud.precisely.com/apis/products-try-out/[api_tryout_path]
status-updates-to-user:
[User instructions for status updates]
all-examples-to-include-in-tool-description-field:
[All examples — go ONLY in Tool description field in precisely_wrapper_server.py, nowhere else]
```

## Implementation Rules (STRICT - Follow for EVERY prompt)

1. Process prompts from `implementation_user_prompts.txt` sequentially (user may specify starting line number)
2. For EACH prompt:
   a. Fetch OpenAPI spec from the try-out link FIRST
   b. Add method to `precisely_api_core.py` — use OpenAPI spec example "Request" values in the docstring example call
   c. Add Tool to `precisely_wrapper_server.py` — use user-prompt examples (Request sections only) in the `description` field
   d. Add test case to `test_precisely_mcp.py` `get_test_cases()` using the OpenAPI spec example's "Request" section values as test input arguments (NOT user-prompt examples)
   e. Add tool entry to the appropriate section in `readme.md`
   f. Update tool/method/test counts in ALL 6 locations (see Tool Count Updates section)
3. OpenAPI spec: Use entire API description, and entire field descriptions VERBATIM - NEVER invent or customize
4. User-prompt examples: Copy "Request" sections VERBATIM into Tool `description` ONLY. Do NOT include "Response" sections. Do NOT use these values in test cases or docstrings
5. If anything is not clear or there are conflicts, ask user instead of assuming

## Tool Count Updates (MANDATORY after EACH tool added)

Update the count in ALL 6 locations across these files:

**In `precisely_wrapper_server.py`:**
1. Comment above `TOOLS` list: `# Tool definitions (XX tools...)`
2. `list_tools()` docstring: `"""List available tools (XX tools)..."""`
3. `run_stdio()` logger message
4. `run_http()` logger message

**In `test_precisely_mcp.py`:**
5. Layer 1 method count assertion (e.g., `if len(methods) != XX:`)
6. Layer 2 tool count assertion (e.g., `if len(tools) != XX:`)

## Adding New API Tools

When adding a new Precisely API endpoint as a tool:

1. **Add method to `precisely_api_core.py`**:
   - Use OpenAPI spec example's "Request" values in the docstring example call
   ```python
   def new_method(self, param1: str, param2: Dict, **kwargs) -> Dict[str, Any]:
       """Docstring describing the API (from OpenAPI spec, verbatim)
       
       Example:
           new_method(
               param1="value_from_openapi_spec",  # NOT from user-prompt examples
               param2={"key": "value_from_openapi_spec"}
           )
       """
       url = f"{self.base_url}/v1/endpoint"
       # Use appropriate headers. For example, for `overlap` API, "Accept" header should be "application/geo+json"
       headers = {"Accept": "application/geo+json"}
       response = self.session.post(url, json=json_data, headers=headers)
       return response.json()
   ```

2. **Add Tool definition to `precisely_wrapper_server.py`** in the `TOOLS` list:
   - Use user-prompt examples (Request sections only, verbatim) in the `description` field
   - Do NOT put OpenAPI spec examples here — only user-prompt examples go in `description`
   ```python
   Tool(
       name="new_method",  # Must match method name in core module
       description="Tool description + user-prompt examples (Request sections ONLY, copied verbatim from 'all-examples-to-include-in-tool-description-field:' section)",
       inputSchema={...}  # JSON Schema matching method parameters
   )
   ```

3. **Add test case to `test_precisely_mcp.py`** in `get_test_cases()`:
   - Use OpenAPI spec example's "Request" values as test input arguments
   - Do NOT use user-prompt examples as test inputs

4. **Add tool to `readme.md`** in the appropriate API category section

5. **Update tool counts** in ALL 6 locations: `TOOLS` comment, `list_tools()` docstring, `run_stdio()`, `run_http()`, and both assertions in `test_precisely_mcp.py`

## Handling Image/Binary Responses (Maps & Tiling APIs)

Some APIs (WMS GetMap, WMTS GetTile) return **image/png** binary data instead of JSON.

### In `precisely_api_core.py`:
- Do NOT call `response.json()` — the response is binary image data
- Base64-encode the image bytes and return a dict with metadata:
```python
import base64

def wms_get_map(self, ...) -> Dict[str, Any]:
    headers = {"Accept": "image/png"}
    response = self.session.get(url, params=params, headers=headers)
    response.raise_for_status()
    image_base64 = base64.b64encode(response.content).decode()
    return {
        "image_base64": image_base64,
        "content_type": response.headers.get("Content-Type", "image/png"),
        "size_bytes": len(response.content)
    }
```

### In `precisely_wrapper_server.py`:
- Import `ImageContent` from `mcp.types`:
```python
from mcp.types import Tool, TextContent, ImageContent
```
- In `call_tool()`, check if the result contains `image_base64` and return `ImageContent`:
```python
if isinstance(result, dict) and result.get("image_base64"):
    return [ImageContent(
        type="image",
        data=result["image_base64"],
        mimeType=result.get("content_type", "image/png")
    )]
```

### In `test_precisely_mcp.py`:
- Image-returning tests should validate that the response contains `image_base64` key with non-empty string value, instead of checking for absence of `"error"` key on a JSON dict

## Handling XML Responses (WMS/WMTS GetCapabilities)

Some APIs (WMS GetCapabilities, WMTS GetCapabilities) return **XML** instead of JSON.

### In `precisely_api_core.py`:
- Do NOT call `response.json()` — return the XML text as a string in a dict:
```python
def wms_get_capabilities(self, ...) -> Dict[str, Any]:
    response = self.session.get(url, params=params)
    response.raise_for_status()
    return {"xml": response.text, "content_type": response.headers.get("Content-Type", "text/xml")}
```

### In `precisely_wrapper_server.py`:
- XML responses are fine as `TextContent` — they are text strings

## Multi-Response Endpoints

Some API endpoints (WMS `handleGetRequest`, WMTS `wmtsRequest`) support **multiple REQUEST types** with different response formats:
- `GetCapabilities` → XML
- `GetMap` / `GetTile` → image/png
- `GetFeatureInfo` → JSON

The `precisely_api_core.py` method must detect the `REQUEST` parameter and handle the response format accordingly:
```python
if request_type.upper() == "GETMAP" or request_type.upper() == "GETTILE":
    # Binary image response
    return {"image_base64": base64.b64encode(response.content).decode(), ...}
elif request_type.upper() == "GETCAPABILITIES":
    # XML text response  
    return {"xml": response.text, ...}
else:
    # JSON response (e.g., GetFeatureInfo)
    return response.json()
```

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
- **"No acceptable representation"**: Need to use appropriate `Accept` header for endpoint
- **Tool disabled errors**: Restart MCP server after code changes
