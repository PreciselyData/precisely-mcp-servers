# Analyze MCP Server — AI-Assisted Dataflow Automation

> 📦 **Download:** [data360-analyze-mcp-beta.v2.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/data360-analyze-mcp-beta.v2.0)

Analyze MCP lets your AI assistant (GitHub Copilot in VS Code, or Claude Desktop / Claude Code) discover, build, execute, and inspect Data360 Analyze dataflows through natural language.

This package includes:

- **MCP Server** — exposes Analyze capabilities as MCP tools
- **Flow Builder Agent** — an agent layer that builds and runs multi-node dataflows interactively

---

## Prerequisites

- **Node.js 22 or higher** — [download here](https://nodejs.org/)
- **Analyze 3.18.0 or higher** with API access (network access and credentials)
- **VS Code** (for Copilot agent usage) or **Claude Code** (Claude Desktop can work directly with the Analyze MCP server, however Analyze agent is only supported in Claude Code)

---

## Quick Start

### 1. Download from the link above, and unzip the contents
### 2. From the command line change directories into the extracted zip folder
### 3. Configure the URL to your Analyze instance

Edit `config.json` and set `analyzeUrl` to point at your Analyze instance:

```json
{
  "analyzeUrl": "https://your-analyze-host:8080",
  "tenantLocator": "object:!tenant:defaultTenant",
  "workspaceLocator": "",
  "publicDataLocator": "object:!tenant:defaultTenant~workspace:lavastormShared~data-collection:default-public"
}
```

Alternatively, set the `ANALYZE_URL` environment variable (environment variables take precedence over `config.json`).

> [!CAUTION]
> Use `https://` if your Analyze instance supports it. Using `http://` means all requests, including credentials, will be sent in plain text and are not secure.

### 4. Connect Your AI Client

#### VS Code (GitHub Copilot Chat)
Open the current directory in VS Code. The agent should get automatically detected by VS Code.

1. Open the chat panel.
2. Select the **@analyze-vscode** agent from the agent picker (or type `@analyze-vscode` at the start of your message).
3. Ask your question — e.g. `@analyze-vscode login to analyze and list all available dataflows`.
4. The agent will automatically start the bundled Analyze MCP Server and proceed to execute your prompt.

#### Claude Code

1. From the project directory, invoke the agent:
   ```
   claude --agent analyze-claude
   ```
2. Select "Yes, I trust this folder" when prompted.
3. Ask your question — e.g. `login to analyze and list all available dataflows`.
4. The agent will automatically start the bundled Analyze MCP Server and proceed to execute your prompt.

#### Claude Desktop

> [!NOTE]
> Claude Desktop does not support agents, so the `@analyze-claude` agent workflow is not available. However, you can still configure the MCP server and use all MCP tools directly through natural language (login, list dataflows, execute, upload, etc.).

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "analyze": {
      "command": "node",
      "args": ["<absolute-path-to-this-folder>/server/server.js"],
      "env": {
        "ANALYZE_URL": "https://your-analyze-host:8080"
      }
    }
  }
}
```

Replace `<absolute-path-to-this-folder>` with the full path to where you extracted this package.

Config file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Cloud Services (Copilot 365, etc.)

This server **cannot run in cloud-based AI services** like Copilot 365 or Microsoft 365 Copilot. These services cannot execute local processes. For cloud deployment, you would need a remotely-hosted HTTP MCP server (a different architecture).


**Building dataflows (via the @analyze agent in VS Code or Claude Code):**

In VS Code:
```
@analyze-vscode Build a dataflow that reads customer data, deduplicates, and exports
```

In Claude Code:
```
Build a dataflow that reads customer data, deduplicates, and exports
```

The agent will discover node types, build the flow step-by-step, set properties, execute, and report results.

---

## Configuration Reference

Runtime settings can be provided through `config.json` and/or environment variables. Environment variables take precedence over `config.json`.

| `config.json` Field    | Env var                  | Description                                                                                                                              |
|-----------------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `analyzeUrl`          | `ANALYZE_URL`            | Base URL of your Analyze instance                                                                                                        |
| `tenantLocator`       | `ANALYZE_TENANT_LOCATOR` | Tenant ORL (default: `defaultTenant`)                                                                                                    |
| `workspaceLocator`    | `ANALYZE_WORKSPACE_LOCATOR` | Workspace ORL (optional)                                                                                                                 |
| `publicDataLocator`   | `ANALYZE_PUBLIC_DATA_LOCATOR` | Default upload target for file uploads                                                                                                   |
| `userDocumentsLocator` | `ANALYZE_USER_DOCS_LOCATOR` | User documents location (optional)                                                                                                       |
| `enabledTools`        | —                        | Optional list of tool names to enable; omit to enable all tools                                                                          |
| `allowedUploadRoots`  | `ANALYZE_ALLOWED_UPLOAD_ROOTS`| Optional list of absolute paths which can be used with `upload_data_file` call. Check Configuring `allowedUploadRoots` below for details. |

#### Configuring `allowedUploadRoots`

To restrict which local directories the MCP server is permitted to upload files from, set `allowedUploadRoots` in `config.json` to a list of absolute path prefixes:

```json
{
  "allowedUploadRoots": ["/home/user/data", "/tmp/uploads"]
}
```

When the list is non-empty, any `upload_data_file` call whose `local_file_path` does not start with one of the listed roots will be rejected. Set it to an empty array (`[]`) to allow uploads from any path.

You can also set allowed roots via the `ANALYZE_ALLOWED_UPLOAD_ROOTS` environment variable as a comma-separated list of paths (e.g. `ANALYZE_ALLOWED_UPLOAD_ROOTS=/home/user/data,/tmp/uploads`). The environment variable takes precedence over the value in `config.json`.

---

## Using Analyze MCP Server directly without Analyze Agent

> [!NOTE]
> If you are using Claude Desktop, you will have to connect directly to Analyze MCP server as Claude Desktop does not support agents.


### Setting Up Your MCP Client

The MCP server can be used directly with your MCP client - VS Code or Claude Desktop. However we recommend using the Analyze agent to interact with the MCP Server.
Stdio transport MCP servers must run on the same machine as your client. Each client type has its own configuration method.

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "analyze": {
      "command": "node",
      "args": ["<absolute-path>/this-folder/server/server.js"],
      "env": {
        "ANALYZE_URL": "https://your-analyze-host:8080"
      }
    }
  }
}
```
Replace `<absolute-path>` with the full path to the cloned repository folder.

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### VS Code Copilot Configuration

Add to your VS Code `mcp.json`:

```json
{
  "servers": {
    "analyze": {
      "command": "node",
      "args": ["<absolute-path>/this-folder/server/server.js"],
      "env": {
        "ANALYZE_URL": "https://your-analyze-host:8080"
      }
    }
  }
}
```
Refer to VS Code [MCP configuration reference](https://code.visualstudio.com/docs/copilot/reference/mcp-configuration) for details.

> [!NOTE]
> **Windows users:** Since backslashes (`\`) are escape characters in JSON, you must either escape them as `\\` (e.g., `"C:\\Users\\me\\repo\\server\\server.js"`) or use forward slashes instead (e.g., `"C:/Users/me/repo/server/server.js"`).

#### Cloud Services (Copilot 365, etc.)

This server **cannot run in cloud-based AI services** like Copilot 365 or Microsoft 365 Copilot. These services cannot execute local processes. This MCP server requires a local machine to run on. For cloud deployment, you would need a remotely-hosted HTTP MCP server (a different architecture).

### Starting Analyze MCP Server from CLI
In addition to configure your MCP client to start the Analyze MCP server you can start the MCP server directly from the CLI.

1. Edit `config.json` and set `analyzeUrl` to point at your Analyze instance:

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


2. Run the server:

```bash
node <path-to-this-folder>/server/server.js
```

The server listens on stdin/stdout (MCP stdio transport). Your MCP client must be configured to launch this process locally and communicate with it directly.

### Simple Usage Examples

Once connected, you can talk to Claude or Copilot naturally:

1. "Log in to Analyze as admin"
2. "List all dataflows in /Projects/Demo"
3. "Run the CustomerEnrichment dataflow"
4. "Upload ./customers.csv to Public Documents/Public data"

### Exposed MCP Commands

The currently exposed commands are defined by `enabledTools` in `config.json`.

#### Authentication

| Command | What It Does | Key Arguments |
|---|---|---|
| `analyze_login` | Authenticates against Analyze and returns a session token for other commands. | `username`, `password` |
| `analyze_logout` | Invalidates a session token and logs out. | `token` |

#### Dataflow Discovery & Inspection

| Command | What It Does | Key Arguments |
|---|---|---|
| `list_dataflows` | Lists saved dataflows globally or by Analyze path, optionally recursive. | `session_token`, `filter?`, `path?`, `recursive?` |
| `analyze_get_dataflow` | Retrieves details of a dataflow including name, run properties, and output definitions. | `session_token`, `dataflow_locator`, `include_metadata?` |

#### Node Type Discovery

| Command | What It Does | Key Arguments |
|---|---|---|
| `list_node_types` | Lists available node types for dataflow building, with optional filtering. | `filter?`, `exact_name?`, `include_best_effort?` |
| `describe_node_type` | Describes a node type's properties, ports, and serializer metadata. | `session_token?`, `name?`, `node_type_id?` |

#### Dataflow Building (Interactive Edit Session)

| Command | What It Does | Key Arguments |
|---|---|---|
| `open_dataflow` | Opens or creates a dataflow for interactive editing. Returns a `session_id`. | `session_token`, `name?`, `saved_locator?`, `path?` |
| `add_node` | Adds a node to the current dataflow. Returns `node_id` and port labels. | `session_token`, `session_id`, `node_type_id`, `node_id?`, `x?`, `y?` |
| `set_node_property` | Sets a single property on a node (raw value or structured serializer). | `session_token`, `session_id`, `node_id`, `property_name`, `value?`, `serializer?`, `structured_value?` |
| `set_node_properties` | Sets multiple properties across one or more nodes in a single call. | `session_token`, `session_id`, `properties[]` |
| `get_node_properties` | Reads back current resolved properties for a node. | `session_token`, `session_id`, `node_id` |
| `connect_nodes` | Connects two nodes using human-readable port labels. | `session_token`, `session_id`, `source_node_id`, `source_port_label`, `dest_node_id`, `dest_port_label` |
| `move_node` | Sets the canvas position of a node. | `session_token`, `session_id`, `node_id`, `x`, `y` |
| `delete_node` | Removes a node from the dataflow. | `session_token`, `session_id`, `node_id` |
| `add_input_port` | Adds a dynamic input port to a node. | `session_token`, `session_id`, `node_id`, `port_label` |
| `add_output_port` | Adds a dynamic output port to a node. | `session_token`, `session_id`, `node_id`, `port_label` |
| `delete_input_port` | Deletes an input port from a node by label. | `session_token`, `session_id`, `node_id`, `port_label` |
| `delete_output_port` | Deletes an output port from a node by label. | `session_token`, `session_id`, `node_id`, `port_label` |
| `save_dataflow` | Persists the current dataflow and returns the saved locator. | `session_token`, `session_id`, `name?`, `destination_locator?`, `overwrite?` |
| `close_dataflow` | Closes the edit session and releases the edit lock. | `session_token`, `session_id` |

#### Execution (Interactive Edit Session)

| Command | What It Does | Key Arguments |
|---|---|---|
| `run_dataflow` | Runs all nodes in the current edit session and polls until complete. | `session_token`, `session_id` |
| `rerun_node` | Clears a node's state and re-executes it within the active session. | `session_token`, `session_id`, `node_id`, `timeout_ms?` |
| `clear_node_state` | Clears the cached execution state for one node. | `session_token`, `session_id`, `node_id` |
| `stop_run` | Stops the active execution session. | `session_token`, `session_id` |
| `get_node_state` | Gets execution state for a node (run status, record counts, output data refs). | `session_token`, `session_id`, `node_id` |
| `get_dataflow_snapshot` | Returns the full dataflow structure, execution state, and optional output previews. | `session_token`, `session_id`, `include_properties?`, `preview_node_ids?`, `max_rows?` |

#### Execution (Headless / API-Driven)

| Command | What It Does | Key Arguments |
|---|---|---|
| `execute_dataflow` | Executes a saved dataflow via REST API (no edit session required). | `session_token`, `dataflow_locator`, `run_properties?`, `parent_run_property_set_locator?` |
| `analyze_get_run_status` | Gets the status of a running or completed execution. | `session_token`, `execution_locator` |
| `analyze_stop_dataflow` | Stops a currently running dataflow execution. | `session_token`, `execution_locator` |
| `get_dataflow_outputs` | Retrieves published Data Flow Output values from a completed execution. | `session_token`, `execution_session_locator` |
| `get_dataset` | Reads dataset rows by ORL with optional FIQL filtering and pagination. | `session_token`, `dataset_locator`, `filter?`, `offset?`, `limit?` |

#### File Upload

| Command | What It Does | Key Arguments |
|---|---|---|
| `upload_data_file` | Uploads a local file into Analyze, optionally waiting for completion. | `session_token`, `local_file_path`, `filename?`, `target_locator?`, `overwrite?`, `wait_for_completion?` |

### Practical Usage Patterns

#### Pattern A: Execute Existing Saved Dataflow

1. `analyze_login`
2. `list_dataflows` (optional discovery)
3. `execute_dataflow`
4. `get_dataflow_outputs`
5. `get_dataset` (for dataset outputs)

### Independent Command Examples

#### Example: Login

```json
{
  "tool": "analyze_login",
  "arguments": {
    "username": "admin",
    "password": "***"
  }
}
```

#### Example: List Dataflows in Folder Recursively

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

#### Example: Upload Local File

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

#### Example: Execute Saved Dataflow and Read Dataset Output

```json
{
  "tool": "execute_dataflow",
  "arguments": {
    "session_token": "<token>",
    "dataflow_locator": "<dataflow locator>"
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

---

## Security Notes

- Do not log credentials or tokens externally.
- Server-side tool call logging already redacts `session_token` and `password`.
- Prefer least-privilege Analyze users for production automation.

## Known Limitations

- **stdio transport only** — no concurrent requests; one agent at a time
- **Local execution only** — client and server must be on the same machine
- **Single-user only** — no token isolation between conversations

---

## License

Copyright 2026 Precisely

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

> <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

