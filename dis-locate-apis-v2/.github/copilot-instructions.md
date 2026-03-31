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
- `test_new_tools.py` - Functional verification test for the 22 new spatial/OGC/tiling/mapping tools (root folder)
- `readme.md` - Project documentation with tool list (root folder)
- `implementation_user_prompts.txt` - User prompts for implementations (root folder)
- `.github/copilot-instructions.md` - These instructions

---

## Canonical Tool Manifest (22 New Tools)

Every implementation task corresponds to exactly one operationId from an OpenAPI spec file. This is the **authoritative list** — no tool may be added, skipped, or renamed without updating this table.

| # | operationId | Source Spec File | Spec URL |
|---|---|---|---|
| 1 | `spatialAnalysis_findNearestCandidates` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 2 | `spatialAnalysis_searchAtLocation` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 3 | `spatialAnalysis_overlaps` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 4 | `spatialAnalysis_getProducts` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 5 | `spatialAnalysis_listTables` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 6 | `spatialAnalysis_getTableMetadata` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 7 | `spatialAnalysis_summarizeData` | `openapi/SpatialFeatureApis.json` | https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json |
| 8 | `spatialFeatures_getLandingPage` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 9 | `spatialFeatures_getAPI` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 10 | `spatialFeatures_getFunctions` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 11 | `spatialFeatures_conformanceDeclaration` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 12 | `spatialFeatures_getCollectionsPage` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 13 | `spatialFeatures_getCollection` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 14 | `spatialFeatures_getSchema` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 15 | `spatialFeatures_getQueryables` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 16 | `spatialFeatures_getCollectionItems` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 17 | `spatialFeatures_getFeatureById` | `openapi/OGCFeatureApis.json` | https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json |
| 18 | `spatial-maps_handleGetRequest` | `openapi/mapping.json` | https://developer.cloud.precisely.com/openapi/mapping.json |
| 19 | `spatial-maps_postGetMap` | `openapi/mapping.json` | https://developer.cloud.precisely.com/openapi/mapping.json |
| 20 | `spatialTiling_wmtsRequest` | `openapi/tiling.json` | https://developer.cloud.precisely.com/openapi/tiling.json |
| 21 | `spatialTiling_restfulGetTileDefault` | `openapi/tiling.json` | https://developer.cloud.precisely.com/openapi/tiling.json |
| 22 | `spatialTiling_restfulGetTileSimpleProfile` | `openapi/tiling.json` | https://developer.cloud.precisely.com/openapi/tiling.json |

---

## OpenAPI Spec Sources (Source of Truth)

OpenAPI specs are available in TWO locations. Use whichever is accessible; they are identical:

1. **Local files** in `openapi/` folder:
   - `openapi/SpatialFeatureApis.json` — spatialAnalysis operations
   - `openapi/OGCFeatureApis.json` — spatialFeatures operations
   - `openapi/tiling.json` — spatialTiling operations
   - `openapi/mapping.json` — spatial-maps operations

2. **Remote URLs**:
   - https://developer.cloud.precisely.com/openapi/SpatialFeatureApis.json
   - https://developer.cloud.precisely.com/openapi/OGCFeatureApis.json
   - https://developer.cloud.precisely.com/openapi/tiling.json
   - https://developer.cloud.precisely.com/openapi/mapping.json

**Prefer local files** (`openapi/` folder) to avoid network issues. Fall back to URLs only if local files are missing.

---

## Phased Workflow (MANDATORY — Follow in Exact Order)

### Phase 0: Discovery

For EACH tool (processing prompts from `implementation_user_prompts.txt` sequentially):

1. **Locate the OpenAPI spec**: Use the Canonical Tool Manifest table above to find the correct spec file and operationId.
2. **Read the operation** from the spec: Find the path + method matching the operationId. Extract:
   - The operation's `description` field (verbatim — see NO PARAPHRASE rule below)
   - The operation's `parameters` / `requestBody` schema with all field `description` values
   - The operation's `responses` schema
   - Any `example` or `examples` values in the spec (for test cases and core docstring examples)
3. **Read the user prompt** from `implementation_user_prompts.txt`: Extract the "all-examples-to-include-in-tool-description-field:" section.
4. **Verify the operationId** matches the Canonical Tool Manifest row. If it does not, STOP and ask the user.

### Phase 1: Instructions Compliance Checks (Pre-Flight)

Before writing ANY code, verify:

1. You have the OpenAPI operation `description` text copied into a scratchpad — compare character-by-character that it is verbatim.
2. You have identified the `Args` for the core method (parameter names, types, descriptions — all from OpenAPI spec).
3. You have identified the `Returns` structure (from OpenAPI response schema).
4. You have confirmed which example values will go where:
   - Core docstring `Example:` section → OpenAPI spec example values ONLY
   - Wrapper tool `description` examples → User-prompt examples (Request sections ONLY)
   - Test case inputs → OpenAPI spec example values ONLY
5. You have NOT confused user-prompt examples with OpenAPI spec examples.

### Phase 2: Code Changes

Execute these steps for EACH tool, in order:

#### Step 2a: Add method to `precisely_api_core.py`

The docstring MUST have these sections in this exact order:

```python
def method_name(self, param1: str, param2: Dict, **kwargs) -> Dict[str, Any]:
    """<OpenAPI operation description — verbatim, NO PARAPHRASE>

    Args:
        param1 (str): <OpenAPI parameter description — verbatim>
        param2 (Dict): <OpenAPI parameter/requestBody field description — verbatim>
        **kwargs: Additional keyword arguments passed to the API.

    Returns:
        Dict[str, Any]: <Description derived from OpenAPI response schema.
            Describe the top-level keys and their types.>

    Example:
        method_name(
            param1="value_from_openapi_spec_example",
            param2={"key": "value_from_openapi_spec_example"}
        )
    """
```

**Rules for `Args:`**:
- Every required parameter gets an entry.
- Optional parameters with defaults get an entry noting the default.
- Parameter descriptions are copied VERBATIM from the OpenAPI spec `description` field for that parameter/property.
- If the OpenAPI spec has no `description` for a parameter, write only the type — do NOT invent a description.

**Rules for `Returns:`**:
- Describe the return type and top-level structure based on the OpenAPI response schema.
- For JSON responses: `Dict[str, Any]: <describe structure>`
- For image responses: `Dict[str, Any]: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int)`
- For XML responses: `Dict[str, Any]: Dict with keys 'xml' (str), 'content_type' (str)`

**Rules for `Example:`**:
- Use OpenAPI spec example values ONLY. If the OpenAPI spec provides no example, OMIT the Example section entirely.
- NEVER use values from `implementation_user_prompts.txt` examples here.

#### Step 2b: Add Tool definition to `precisely_wrapper_server.py`

```python
Tool(
    name="method_name",  # Must match method name in precisely_api_core.py
    description="""<OpenAPI operation description — verbatim, NO PARAPHRASE>

Returns: <Description from OpenAPI response schema — what the tool returns>

<User-prompt examples from 'all-examples-to-include-in-tool-description-field:' — Request sections ONLY, copied verbatim>
""",
    inputSchema={...}  # JSON Schema matching method parameters; field descriptions from OpenAPI spec verbatim
)
```

**Rules for wrapper `description`**:
- First paragraph: OpenAPI operation `description` — verbatim.
- Then a `Returns:` line describing the response structure (from OpenAPI response schema).
- Then ALL examples from the user prompt's "all-examples-to-include-in-tool-description-field:" section — Request sections ONLY. Copy verbatim. Do NOT include Response sections.
- `inputSchema` field descriptions come from the OpenAPI spec VERBATIM. If the OpenAPI spec provides example values, include them via `"example"` keys in the JSON Schema.

#### Step 2c: Add test case to `test_new_tools.py`

- Use OpenAPI spec example "Request" values as test input arguments.
- Do NOT use user-prompt examples as test inputs.
- See "New Functional Verification Test Script" section below for details.

#### Step 2d: Add test case to `test_precisely_mcp.py`

- Add to `get_test_cases()` using OpenAPI spec example "Request" values.
- Do NOT use user-prompt examples.

#### Step 2e: Add tool to `readme.md`

- Add to the appropriate API category section.

#### Step 2f: Update tool counts

- Update ALL 6 count locations (see Tool Count Updates section).

### Phase 3: Tests

After ALL tools are implemented (or after each batch), run:

```bash
# Syntax check all modified files
py -c "import ast; ast.parse(open('precisely_api_core.py', encoding='utf-8-sig').read()); print('Core OK'); ast.parse(open('mcp_servers/precisely_wrapper_server.py', encoding='utf-8-sig').read()); print('Wrapper OK'); ast.parse(open('test_precisely_mcp.py', encoding='utf-8-sig').read()); print('Test OK'); ast.parse(open('test_new_tools.py', encoding='utf-8-sig').read()); print('NewTest OK')"

# Run the new 22-tool functional test
py test_new_tools.py

```

Capture and review output. All tests must pass before marking a tool as complete.

---

## NO PARAPHRASE Rule (STRICT)

### What It Means
When the instructions say "verbatim" or "NO PARAPHRASE", the text MUST be an exact character-for-character copy from the OpenAPI spec. This applies to:

1. **Operation `description`** → copied into core method docstring AND wrapper tool `description`
2. **Parameter/property `description`** → copied into core `Args:` section AND wrapper `inputSchema` field descriptions
3. **No shortening**, no rewording, no synonym substitution, no reformatting of bullet points or markdown tables.
4. Preserve ALL formatting: bullet points, constraint lines, markdown tables, line breaks, punctuation.

### Enforcement Steps
1. **Copy-paste**: Always copy-paste directly from the spec JSON. Never retype from memory.
2. **Diff check**: After writing, mentally diff the pasted text against the spec source. If any word differs, fix it.
3. **If an operation has no `description` field**: Do NOT invent one. You may optionally fall back to the parent tag's `description`. NEVER paste `info.description` (the top-level API description) into per-tool docs.
4. **If a parameter has no `description` field**: Write only the type annotation — do NOT invent a description.

---

## Two Distinct Example Sources (CRITICAL - Do NOT Confuse)

There are TWO separate sources of example data. They serve DIFFERENT purposes and go to DIFFERENT files. NEVER mix them up:

### Source 1: OpenAPI Spec Examples (from spec files in `openapi/` folder or remote URLs)
- **Where to find**: The OpenAPI spec JSON for the operation (see Canonical Tool Manifest)
- **Where they go**:
  1. `precisely_api_core.py` — Use the OpenAPI spec example's "Request" values as arguments in a sample method call inside the method's `Example:` docstring section
  2. `test_precisely_mcp.py` / `test_new_tools.py` — Use the SAME OpenAPI spec example's "Request" values as test input arguments
- **Rule**: Copy values VERBATIM from the OpenAPI spec. Do NOT infer, customize, or substitute with values from user-prompt examples. If the OpenAPI spec provides NO example, OMIT the Example — do NOT synthesize values.

### Source 2: User-Prompt Examples (from "all-examples-to-include-in-tool-description-field:" section)
- **Where to find**: The "all-examples-to-include-in-tool-description-field:" section of each user prompt in `implementation_user_prompts.txt`
- **Where they go**: ONLY into the Tool's `description` field in `precisely_wrapper_server.py`
- **Rule**: Include ALL examples. Each example has "Request" and "Response" sections — include ONLY the "Request" sections. Copy verbatim without any modifications or customizations. Do NOT include "Response" sections.
- **NEVER use these as**: test case inputs, method docstring examples, `inputSchema` example values, or anywhere other than the Tool `description` field

### Why This Matters
User-prompt examples and OpenAPI spec examples often contain SIMILAR but DIFFERENT request payloads (different table names, geometries, coordinates, parameters). Using user-prompt examples as test inputs or docstring examples is WRONG — they must ONLY appear in the Tool `description`. The OpenAPI spec is the SOLE source for test cases and docstring example calls.

---

## Prompt Template

```
user-request:
Implement MCP tool for API at try-out link: https://developer.cloud.precisely.com/apis/products-try-out/[api_tryout_path]
status-updates-to-user:
[User instructions for status updates]
all-examples-to-include-in-tool-description-field:
[All examples — go ONLY in Tool description field in precisely_wrapper_server.py, nowhere else]
```

---

## Implementation Rules (STRICT - Follow for EVERY prompt)

1. Process prompts from `implementation_user_prompts.txt` sequentially (user may specify starting line number).
2. For EACH prompt, follow the Phased Workflow (Phase 0 → Phase 1 → Phase 2 → Phase 3).
3. OpenAPI spec: Use entire operation `description`, and entire field `description` values VERBATIM — NEVER invent, shorten, or customize (see NO PARAPHRASE rule).
4. User-prompt examples: Copy "Request" sections VERBATIM into Tool `description` ONLY. Do NOT include "Response" sections. Do NOT use these values in test cases or docstrings.
5. If anything is not clear or there are conflicts, ask user instead of assuming.
6. Each core method docstring MUST contain `Args:` and `Returns:` sections BEFORE the `Example:` section.
7. Each wrapper tool `description` MUST contain a `Returns:` line describing the response structure.
8. The `Args:` descriptions in core AND the `inputSchema` field descriptions in wrapper MUST come from the OpenAPI spec verbatim.

### Scope Guard: "Do not touch other files when asked to edit instructions only"
- When the user asks to update ONLY `.github/copilot-instructions.md`, do NOT modify any other files.

---

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

---

## Adding New API Tools (Detailed Template)

When adding a new Precisely API endpoint as a tool:

### 1. Add method to `precisely_api_core.py`

```python
def new_method(self, param1: str, param2: Dict, **kwargs) -> Dict[str, Any]:
    """<OpenAPI operation description — VERBATIM, NO PARAPHRASE>

    Args:
        param1 (str): <OpenAPI parameter description — VERBATIM>
        param2 (Dict): <OpenAPI requestBody/property description — VERBATIM>
        **kwargs: Additional keyword arguments passed to the API.

    Returns:
        Dict[str, Any]: <Describe return structure from OpenAPI response schema.>

    Example:
        new_method(
            param1="value_from_openapi_spec",  # NOT from user-prompt examples
            param2={"key": "value_from_openapi_spec"}
        )
    """
    url = f"{self.base_url}/v1/endpoint"
    # Use appropriate headers per endpoint
    headers = {"Accept": "application/json"}
    response = self.session.post(url, json=json_data, headers=headers)
    return response.json()
```

### 2. Add Tool definition to `precisely_wrapper_server.py`

```python
Tool(
    name="new_method",  # Must match method name in core module
    description="""<OpenAPI operation description — VERBATIM, NO PARAPHRASE>

Returns: <Response structure description from OpenAPI response schema>

<All user-prompt examples — Request sections ONLY, copied VERBATIM>
""",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "<OpenAPI parameter description — VERBATIM>"
            },
            "param2": {
                "type": "object",
                "description": "<OpenAPI property description — VERBATIM>"
            }
        },
        "required": ["param1", "param2"]
    }
)
```

### 3. Add test case to `test_precisely_mcp.py` `get_test_cases()`

- Use OpenAPI spec example's "Request" values as test input arguments
- Do NOT use user-prompt examples as test inputs

### 4. Add test case to `test_new_tools.py`

- Use OpenAPI spec example's "Request" values as test input arguments
- See "New Functional Verification Test Script" section below

### 5. Add tool to `readme.md`

- Add to the appropriate API category section

### 6. Update tool counts in ALL 6 locations

---

## New Functional Verification Test Script (`test_new_tools.py`)

A new test script MUST be created to exercise all 22 new tools independently. Requirements:

### Configuration
- **`base_url`**: `'https://api-dev.cloud.precisely.services/'`
- **Credentials**: Load from `.env` file (dev credentials: `PRECISELY_API_KEY`, `PRECISELY_API_SECRET`)
- Use `dotenv` to load environment variables

### Structure
- Model after `test_precisely_mcp.py :: test_layer3_functional`
- Create a `PreciselyAPI` instance with the dev base_url and dev creds
- Define a test function for each of the 22 tools
- Each test:
  1. Calls the corresponding core method with OpenAPI spec example input values
  2. Validates the response is not an error (or for image endpoints: validates `image_base64` is a non-empty string)
  3. Logs the test name, input, response summary, and pass/fail status
- Generate a summary at the end: total, passed, failed, pass rate

### Maintenance Rule
- **Every time a new tool is added**, a corresponding test MUST be added to `test_new_tools.py`.
- This is in ADDITION to adding the test case to `test_precisely_mcp.py`.

### Example skeleton

```python
"""
Functional Verification Tests for 22 New Spatial/OGC/Tiling/Mapping Tools
Uses dev credentials and dev base_url.
"""
import os, sys, json, time, logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precisely_api_core import PreciselyAPI

API_KEY = os.getenv("PRECISELY_API_KEY")
API_SECRET = os.getenv("PRECISELY_API_SECRET")
BASE_URL = "https://api-dev.cloud.precisely.services/"

api = PreciselyAPI(API_KEY, API_SECRET, BASE_URL)

def test_find_nearest_candidates():
    """Test spatialAnalysis_findNearestCandidates with OpenAPI spec example values"""
    result = api.find_nearest_candidates(
        tableName="...",  # from OpenAPI spec example
        attributes=[...],
        location={...},
        withinDistance="..."
    )
    assert "error" not in str(result).lower() or isinstance(result, dict)
    return result

# ... one function per tool ...

if __name__ == "__main__":
    tests = [test_find_nearest_candidates, ...]  # all 22
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS: {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"  FAIL: {t.__name__}: {e}")
    print(f"\nResults: {passed} passed, {failed} failed, {passed+failed} total")
```

---

## Definition of Done Checklist

A tool implementation is NOT complete until ALL of the following are verified with measurable evidence:

### Checklist Item 1: Manifest Completeness
- [ ] All 22 tools from the Canonical Tool Manifest have been implemented
- **Evidence**: Run `grep -c "def " precisely_api_core.py` and verify the 22 new methods exist. Cross-reference method names against the manifest table.

### Checklist Item 2: Args/Returns Sections Exist in Core
- [ ] Every new core method docstring contains `Args:` and `Returns:` sections
- **Evidence**: Run these grep commands and verify count = 22 for each:
```bash
py -c "import re; content=open('precisely_api_core.py',encoding='utf-8-sig').read(); print('Args count:', len(re.findall(r'Args:', content)))"
py -c "import re; content=open('precisely_api_core.py',encoding='utf-8-sig').read(); print('Returns count:', len(re.findall(r'Returns:', content)))"
```
(Note: existing methods may not have Args/Returns, so verify the count increased by 22 from baseline.)

### Checklist Item 3: Returns Section Exists in Wrapper Tool Descriptions
- [ ] Every new wrapper tool `description` contains a `Returns:` line
- **Evidence**: Run:
```bash
py -c "import re; content=open('mcp_servers/precisely_wrapper_server.py',encoding='utf-8-sig').read(); print('Returns in descriptions:', len(re.findall(r'Returns:', content)))"
```
Verify count >= 22.

### Checklist Item 4: OpenAPI Descriptions Are Verbatim (NO PARAPHRASE)
- [ ] Each core method docstring's first paragraph matches the OpenAPI operation `description` exactly
- [ ] Each wrapper tool `description`'s first paragraph matches the OpenAPI operation `description` exactly
- **Evidence**: For each tool, manually compare the first paragraph of the docstring/description against the OpenAPI spec. Document any deviations and fix them.

### Checklist Item 5: Example Source Separation
- [ ] Core `Example:` sections contain ONLY OpenAPI spec example values (or are omitted if no spec example exists)
- [ ] Wrapper `description` examples contain ONLY user-prompt examples (Request sections only, no Response sections)
- [ ] Test inputs use ONLY OpenAPI spec example values
- **Evidence**: Spot-check at least 5 tools. For each, verify the example values in the core docstring match the OpenAPI spec and differ from the user-prompt examples.

### Checklist Item 6: Tests Pass
- [ ] `test_new_tools.py` passes all 22 tests
- **Evidence**: Capture terminal output:
```bash
py test_new_tools.py
```
Paste the summary lines (total/passed/failed) as evidence.

### Checklist Item 7: Syntax Checks Pass
- [ ] All 4 Python files parse without syntax errors
- **Evidence**:
```bash
py -c "import ast; ast.parse(open('precisely_api_core.py', encoding='utf-8-sig').read()); print('Core OK'); ast.parse(open('mcp_servers/precisely_wrapper_server.py', encoding='utf-8-sig').read()); print('Wrapper OK'); ast.parse(open('test_precisely_mcp.py', encoding='utf-8-sig').read()); print('Test OK'); ast.parse(open('test_new_tools.py', encoding='utf-8-sig').read()); print('NewTest OK')"
```

### Checklist Item 8: Tool Counts Updated
- [ ] All 6 count locations are updated and consistent
- **Evidence**: Grep for the count number in all 4 files and verify they match.

---

## Handling Image/Binary Responses (Maps & Tiling APIs)

Some APIs (WMS GetMap, WMTS GetTile) return **image/png** binary data instead of JSON.

### In `precisely_api_core.py`:
- Do NOT call `response.json()` — the response is binary image data
- Base64-encode the image bytes and return a dict with metadata:
```python
import base64

def wms_get_map(self, ...) -> Dict[str, Any]:
    """<OpenAPI description verbatim>

    Args:
        ...

    Returns:
        Dict[str, Any]: Dict with keys 'image_base64' (str), 'content_type' (str), 'size_bytes' (int).
    """
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

### In `test_new_tools.py` and `test_precisely_mcp.py`:
- Image-returning tests should validate that the response contains `image_base64` key with non-empty string value, instead of checking for absence of `"error"` key on a JSON dict

## Handling XML Responses (WMS/WMTS GetCapabilities)

Some APIs (WMS GetCapabilities, WMTS GetCapabilities) return **XML** instead of JSON.

### In `precisely_api_core.py`:
- Do NOT call `response.json()` — return the XML text as a string in a dict:
```python
def wms_get_capabilities(self, ...) -> Dict[str, Any]:
    """<OpenAPI description verbatim>

    Args:
        ...

    Returns:
        Dict[str, Any]: Dict with keys 'xml' (str), 'content_type' (str).
    """
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

---

## Critical Patterns

### Authentication
- Uses Base64-encoded `api_key:api_secret` in `Authorization: Apikey <encoded>` header
- Credentials from environment variables: `PRECISELY_API_KEY`, `PRECISELY_API_SECRET`

### GraphQL APIs
Many tools use GraphQL via `/data-graph/graphql`. Query structure is embedded in method implementations. See `get_property_data()`, `get_flood_risk_by_address()` for patterns.

### Headers
- Use appropriate `Accept` headers per endpoint:
  - JSON endpoints: `"Accept": "application/json"`
  - GeoJSON endpoints (e.g., overlap): `"Accept": "application/geo+json"`
  - Image endpoints: `"Accept": "image/png"`
  - XML endpoints: no special Accept header needed (or `"Accept": "text/xml"`)

---

## Development Commands

```bash
# Install dependencies
py -m pip install -r requirements.txt

# Run MCP server (stdio - for Claude Desktop/VS Code)
py mcp_servers/precisely_wrapper_server.py

# Run MCP server (HTTP - for LangChain/web apps)
py mcp_servers/precisely_wrapper_server.py --transport http --port 8000

# Run the 22 new tools test
py test_new_tools.py

# Run full test suite
py test_precisely_mcp.py

# Syntax check all files
py -c "import ast; ast.parse(open('precisely_api_core.py', encoding='utf-8-sig').read()); print('Core OK'); ast.parse(open('mcp_servers/precisely_wrapper_server.py', encoding='utf-8-sig').read()); print('Wrapper OK'); ast.parse(open('test_precisely_mcp.py', encoding='utf-8-sig').read()); print('Test OK'); ast.parse(open('test_new_tools.py', encoding='utf-8-sig').read()); print('NewTest OK')"
```

## VS Code MCP Configuration

Edit `.vscode/mcp.json` to configure credentials. Switch between prod/dev by commenting/uncommenting credential blocks. **Restart MCP server after credential changes**.

## Logging

Logs written to `logs/app_<uuid>.log` with RotatingFileHandler (10MB, 5 backups). Enable DEBUG level for full request/response logging.

## Common Issues

- **503/404 on spatial APIs**: Check if credentials have spatial API access (dev vs prod)
- **"No acceptable representation"**: Need to use appropriate `Accept` header for endpoint
- **Tool disabled errors**: Restart MCP server after code changes
