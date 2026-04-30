# Analyze MCP Server

Analyze MCP Server exposes an MCP tool surface that lets an MCP client (for example, Copilot or Claude Desktop) discover, execute, and inspect Analyze dataflows through natural language.

## Prerequisites

- **Node.js 22 or higher** — [download here](https://nodejs.org/)
- **Analyze 3.18.0 or higher** with API access (network access and credentials)

## Setup

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-folder>
```

2. Edit `config.json` and set `analyzeUrl` to point at your Analyze instance:

```json
{
  "analyzeUrl": "http://your-analyze-host:8080",
  "tenantLocator": "object:!tenant:defaultTenant",
  "workspaceLocator": "",
  "publicDataLocator": "object:!tenant:defaultTenant~workspace:lavastormShared~data-collection:default-public"
}
```
Alternatively, you can set the `ANALYZE_URL` environment variable. Configuration using environment variables take precedence over properties in  `config.json`.
See configuration reference below for details on all available configuration options.

> [!CAUTION]
> Use `https://` if your Analyze instance supports it. Using `http://` means all requests, including credentials, will be sent in plain text and are not secure.


3. Run the server:

```bash
node server/server.js
```

The server listens on stdin/stdout (MCP stdio transport). Your MCP client must be configured to launch this process locally and communicate with it directly.

## Configuration Reference

Runtime settings can be provided through config.json and/or environment variables. Environment variables take precedence over `config.json`.

| `config.json` Field    | Env var                  | Description                                                                                                                              |
|-----------------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `analyzeUrl`          | `ANALYZE_URL`            | Base URL of your Analyze instance                                                                                                        |
| `tenantLocator`       | `ANALYZE_TENANT_LOCATOR` | Tenant ORL (default: `defaultTenant`)                                                                                                    |
| `workspaceLocator`    | `ANALYZE_WORKSPACE_LOCATOR` | Workspace ORL (optional)                                                                                                                 |
| `publicDataLocator`   | `ANALYZE_PUBLIC_DATA_LOCATOR` | Default upload target for file uploads                                                                                                   |
| `userDocumentsLocator` | `ANALYZE_USER_DOCS_LOCATOR` | User documents location (optional)                                                                                                       |
| `enabledTools`        | —                        | Optional list of tool names to enable; omit to enable all tools                                                                          |
| `allowedUploadRoots`  | `ANALYZE_ALLOWED_UPLOAD_ROOTS`| Optional list of absolute paths which can be used with `upload_data_file` call. Check Configuring `allowedUploadRoots` below for details. |

### Configuring `allowedUploadRoots`

To restrict which local directories the MCP server is permitted to upload files from, set `allowedUploadRoots` in `config.json` to a list of absolute path prefixes:

```json
{
  "allowedUploadRoots": ["/home/user/data", "/tmp/uploads"]
}
```

When the list is non-empty, any `upload_data_file` call whose `local_file_path` does not start with one of the listed roots will be rejected. Set it to an empty array (`[]`) to allow uploads from any path.

You can also set allowed roots via the `ANALYZE_ALLOWED_UPLOAD_ROOTS` environment variable as a comma-separated list of paths (e.g. `ANALYZE_ALLOWED_UPLOAD_ROOTS=/home/user/data,/tmp/uploads`). The environment variable takes precedence over the value in `config.json`.

## Setting Up Your MCP Client

Stdio transport MCP servers must run on the same machine as your client. Each client type has its own configuration method.

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "analyze": {
      "command": "node",
      "args": ["<absolute-path>/this-repo/server/server.js"],
      "env": {
        "ANALYZE_URL": "http://your-analyze-host:8080"
      }
    }
  }
}
```
Replace `<absolute-path>` with the full path to the cloned repository folder.

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### VS Code Copilot Configuration

Add to your VS Code `mcp.json`:

```json
{
  "servers": {
    "analyze": {
      "command": "node",
      "args": ["<absolute-path>/this-repo/server/server.js"],
      "env": {
        "ANALYZE_URL": "http://your-analyze-host:8080"
      }
    }
  }
}
```
Refer to VS Code [MCP configuration reference](https://code.visualstudio.com/docs/copilot/reference/mcp-configuration) for details. 

> [!NOTE]
> **Windows users:** Since backslashes (`\`) are escape characters in JSON, you must either escape them as `\\` (e.g., `"C:\\Users\\me\\repo\\server\\server.js"`) or use forward slashes instead (e.g., `"C:/Users/me/repo/server/server.js"`).

### Cloud Services (Copilot 365, etc.)

This server **cannot run in cloud-based AI services** like Copilot 365 or Microsoft 365 Copilot. These services cannot execute local processes. This MCP server requires a local machine to run on. For cloud deployment, you would need a remotely-hosted HTTP MCP server (a different architecture).

## Simple usage Examples

Once connected, you can talk to Claude or Copilot naturally:

1. "Log in to Analyze as admin"
2. "List all dataflows in /Projects/Demo"
3. "Run the CustomerEnrichment dataflow"
4. "Upload ./customers.csv to Public Documents/Public data"

## Exposed MCP Commands

The currently exposed commands are defined by `enabledTools` in `config.json`.

### Authentication

| Command | What It Does | Arguments |
|---|---|---|
| `analyze_login` | Authenticates against Analyze and returns a session token for other commands. | `username`, `password` |

### Dataflow Discovery

| Command | What It Does | Arguments |
|---|---|---|
| `list_dataflows` | Lists saved dataflows globally or by Analyze path, optionally recursive. | `session_token`, `filter?`, `path?`, `recursive?` |

### File Upload

| Command | What It Does | Arguments |
|---|---|---|
| `upload_data_file` | Uploads a local file into Analyze, optionally waiting for completion. | `session_token`, `local_file_path`, `filename?`, `target_locator?`, `overwrite?`, `wait_for_completion?` |

### Execution and Output Retrieval

| Command | What It Does | Arguments |
|---|---|---|
| `execute_dataflow` | Executes a saved dataflow via API path (headless/automation style). | `session_token`, `dataflow_locator`, `run_properties?`, `parent_run_property_set_locator?` |
| `get_dataflow_outputs` | Returns published Data Flow Output values from execution session. | `session_token`, `execution_session_locator` |
| `get_dataset` | Reads dataset rows by dataset ORL with optional filtering/paging. | `session_token`, `dataset_locator`, `filter?`, `offset?`, `limit?` |

## Practical Usage Patterns

### Pattern A: Execute Existing Saved Dataflow (Headless)

1. `analyze_login`
2. `list_dataflows` (optional discovery)
3. `execute_dataflow`
4. `get_dataflow_outputs`
5. `get_dataset` (for dataset outputs)

## Independent Command Examples

### Example: Login

```json
{
  "tool": "analyze_login",
  "arguments": {
    "username": "admin",
    "password": "***"
  }
}
```

### Example: List Dataflows in Folder Recursively

```json
{
  "tool": "list_dataflows",
  "arguments": {
    "session_token": "<token>",
    "path": "//admin/Projects",
    "recursive": true
  }
}
```

### Example: Upload Local File

```json
{
  "tool": "upload_data_file",
  "arguments": {
    "session_token": "<token>",
    "local_file_path": "./customer_accounts_min.csv",
    "wait_for_completion": true
  }
}
```

### Example: Execute Saved Dataflow and Read Dataset Output

```json
{
  "tool": "execute_dataflow",
  "arguments": {
    "session_token": "<token>",
    "dataflow_locator": "object:!tenant:defaultTenant~directory:...~graph:..."
  }
}
```

Then:

```json
{
  "tool": "get_dataflow_outputs",
  "arguments": {
    "session_token": "<token>",
    "execution_session_locator": "<execution-session-orl>"
  }
}
```

Then (for dataset output values):

```json
{
  "tool": "get_dataset",
  "arguments": {
    "session_token": "<token>",
    "dataset_locator": "<dataset-orl>",
    "limit": 100
  }
}
```

## Extended Agent Example (Single Business Task)

Goal: "Upload a source CSV, run a saved enrichment dataflow, and return the first 50 output rows."

Agent workflow:

1. `analyze_login`
2. `upload_data_file` (source CSV)
3. `list_dataflows` (find the target saved flow)
4. `execute_dataflow` (optionally with run properties)
5. `get_dataflow_outputs` (retrieve output values and dataset ORLs)
6. `get_dataset` (read and return first 50 rows from dataset output)

## Error Handling Guidance

- Treat authentication and locator errors as hard failures.
- For `execute_dataflow` failures, capture and surface any returned `execution_session_locator` for follow-up output checks.
- If `get_dataflow_outputs` includes dataset ORLs, use `get_dataset` with `limit`/`offset` to page results safely.

## Security and Logging

- Do not log credentials or tokens externally.
- Server-side tool call logging already redacts `session_token` and `password`.
- Prefer least-privilege Analyze users for production automation.

## Known Limitations

- Single-user only — no token isolation between conversations
- No input validation — errors surface as raw Analyze API response messages

## License

Copyright 2026 Precisely

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

> <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

