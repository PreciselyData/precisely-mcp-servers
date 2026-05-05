# MapInfo Pro MCP Server

> 📦 **Download:** Install via the [MapInfo Pro Marketplace](https://mapinfomarketplace.precisely.com/) or directly from inside MapInfo Pro v23 or later via the MapInfo Marketplace Button on the Home tab.

An in-process MCP server embedded in the **MapInfo-AI add-in for MapInfo Pro**. Once the add-in is loaded, it starts a local HTTP/SSE endpoint that MCP clients (Claude Desktop, GitHub Copilot, etc.) connect to — no separate process to manage.

In addition, there is an AI Assistant chat window available inside MapInfo Pro to let you interact and control most functionality of MapInfo.

---

## Architecture

```
MCP Client (Copilot / Claude / Custom)
  │
  └── HTTP/SSE  http://localhost:3100/sse
        │
        └── MapInfo-AI Add-in (MapInfo Pro process)
              │
              └── MapInfo Pro COM/MapBasic API
```

The server is embedded in MapInfo Pro. MapInfo Pro must be **running with the add-in loaded** before any MCP client can connect.

---

## Prerequisites

- **MapInfo Pro 2300 or later** — Windows only
- **MapInfo-AI add-in** — installed from the Marketplace ZIP (see Setup below)
- No external runtime required (no Node.js, Python, or Java)

---

## Setup

1. **Install the add-in:**
   - Open MapInfo Pro.
   - Go to **Home → Tools → Marketplace**, search for *MapInfo AI*, and click **Install**.
   - Alternatively, download `MapInfo-AI-marketplace.zip` from the release and install via **Home → Tools → Run MapBasic Program** — select the `.mbx` after unzipping it.

2. **Load the add-in:**
   - The add-in starts automatically on next launch if installed via Marketplace and if you mark it as auto-load in the tool manager registred tab.
   - A new **AI Assistant** ribbon button appears in MapInfo Pro home tab.

3. **Verify the server is running:**
   - Open a browser and navigate to `http://localhost:3100/`. You should see a JSON response confirming the server is live.

4. **Connect your MCP client** — see [MCP Client Quick Start](#mcp-client-quick-start) below.

---

## Configuration

Runtime settings are stored in `MapInfo-AI.config`, located in the same folder as `MapInfo-AI.dll`. Edit it with any text editor; changes take effect on the next MapInfo Pro restart.

| Setting | Default | Description |
|---------|---------|-------------|
| `McpPort` | `3100` | TCP port the HTTP/SSE server listens on |
| `McpToken` | _(none)_ | Optional shared-secret. When set, every request must include a matching `X-MCP-Token` header. Leave commented out to disable authentication. |
| `McpLog` | `false` | Set to `true` to write every JSON-RPC request and response to a log file |
| `McpLogPath` | `%TEMP%\MapInfoAI.log` | Full path to the log file (only used when `McpLog` is `true`) |
| `McpChatEndpoint` | GitHub Copilot | OpenAI-compatible chat endpoint for the built-in AI chat panel |
| `McpChatModel` | `claude-sonnet-4.6` | Model name sent to the chat endpoint |
| `McpInstructionsPath` | _(next to DLL)_ | Full path to a `mapinfo-instructions.md` file injected as system prompt context |

---

## Available Tools (~100)

The server exposes approximately 100 tools grouped by domain.

### Catalog / Tables

| Tool | Description |
|------|-------------|
| `catalog_list_tables` | List all open tables with schema and geometry info |
| `catalog_open_table` | Open a `.tab` file |
| `catalog_close_table` | Close an open table |
| `catalog_run_sql` | Execute a MapInfo SQL `SELECT` and return rows as JSON |
| `catalog_get_selection` | Return the current selected set |
| `catalog_get_selected_rows` | Return rows in the current selection |
| `catalog_export_table` | Export a table to GeoJSON, CSV, or other formats |
| `catalog_export_selection` | Export the current selection |
| `catalog_query_geojson` | Run a SQL query and return results as GeoJSON |
| `catalog_update_rows` | Update column values in a table |
| `catalog_save_table` | Save (commit) edits to a table |
| `catalog_revert_table` | Revert unsaved edits |
| `catalog_browse_table` | Open a Browser window for a table |
| `catalog_set_browse` | Set column visibility / width in a Browser |
| `catalog_alter_table` | Add or remove columns |
| `catalog_create_table` | Create a new empty table |
| `catalog_modify_table_structure` | Modify column definitions |

### Maps

| Tool | Description |
|------|-------------|
| `maps_list_maps` | List all open Map windows |
| `maps_get_map` | Get metadata for a Map window |
| `maps_zoom` | Set zoom level and centre |
| `maps_zoom_entire` | Zoom to the full extent of a layer or map |
| `maps_pan` | Pan the map by a given offset |
| `maps_create_map` | Create a new Map window |
| `maps_close_map` | Close a Map window |
| `maps_save_image` | Save the current map view as an image |
| `maps_get_properties` | Get map display properties |
| `maps_set_properties` | Set map display properties |
| `maps_set_time_properties` | Configure time-animation properties |
| `maps_add_adornment` | Add a north arrow, scale bar, or other adornment |
| `maps_add_scalebar` | Add a scale bar adornment |
| `maps_list_adornments` | List adornments on a map |

### Layers

| Tool | Description |
|------|-------------|
| `layers_list_layers` | List all layers in a Map window |
| `layers_set_visible` | Show or hide a layer |
| `layers_set_editable` | Make a layer editable |
| `layers_zoom_layer` | Zoom to the extent of a layer |
| `layers_add_layer` | Add a table as a layer to a Map window |
| `layers_remove_layer` | Remove a layer from a Map window |
| `layers_add_group` | Add a layer group |
| `layers_reorder` | Change the drawing order of layers |

### Themes

| Tool | Description |
|------|-------------|
| `themes_shade_ranges` | Apply a ranged (graduated colour) theme |
| `themes_shade_individual` | Apply an individual value theme |
| `themes_shade_dot_density` | Apply a dot density theme |
| `themes_shade_graduated` | Apply a graduated symbol theme |
| `themes_shade_pie` | Apply a pie chart theme |
| `themes_shade_bar` | Apply a bar chart theme |
| `themes_remove_theme` | Remove a theme from a layer |
| `themes_refresh_theme` | Refresh a theme after data changes |
| `themes_get_theme` | Get the current theme definition for a layer |

### Layout Designer

| Tool | Description |
|------|-------------|
| `layout_create` | Create a new Layout Designer window |
| `layout_set` | Configure page size and orientation |
| `layout_add_page` | Add a page to a multi-page layout |
| `layout_remove_page` | Remove a page |
| `layout_goto_page` | Navigate to a page |
| `layout_add_map_frame` | Add a Map frame |
| `layout_add_browser_frame` | Add a Browser (table) frame |
| `layout_add_image_frame` | Add an image frame |
| `layout_add_text` | Add a text frame |
| `layout_add_legend` | Add a legend frame |
| `layout_add_scale_bar` | Add a scale bar frame |
| `layout_run_frame_command` | Run a command on a frame |
| `layout_open_template` | Open a layout template |
| `layout_set_printer` | Configure printer/page settings |
| `layout_list_frames` | List all frames in a layout |
| `layout_get_item_info` | Get position/size of a frame |
| `layout_set_item_info` | Move or resize a frame |
| `layout_get_item_metadata_value` | Get a metadata value from a frame |
| `layout_remove_frame` | Remove a frame |
| `layout_save_as_image` | Save the layout as a PNG/JPG/PDF image |
| `layout_print_pdf` | Print or save as PDF |
| `layout_close` | Close the Layout Designer |

### MapBasic

| Tool | Description |
|------|-------------|
| `mapbasic_run` | Execute a MapBasic statement |
| `mapbasic_get_syntax` | Look up the syntax for a MapBasic statement |
| `mapinfo_get_function_syntax` | Look up the syntax for a MapBasic function |
| `mapbasic_eval` | Evaluate a MapBasic expression and return the result |
| `mapbasic_get_message_window` | Retrieve content from the MapBasic Message window |

### Workspace

| Tool | Description |
|------|-------------|
| `workspace_open` | Open a `.wor` workspace file |
| `workspace_current` | Return the path of the currently open workspace |
| `workspace_close_all` | Close all open tables and windows |
| `workspace_save` | Save the current workspace |

### Windows

| Tool | Description |
|------|-------------|
| `window_list_windows` | List all open windows |
| `window_get_docking_property` | Get docking state of a window |
| `window_set_docking_property` | Set docking state of a window |
| `window_create_tab_group` | Create a new tab group |
| `window_move_to_tab_group` | Move a window into a tab group |

### File System

| Tool | Description |
|------|-------------|
| `fs_read_file` | Read a text file |
| `fs_write_file` | Write a text file |
| `fs_append_file` | Append to a text file |
| `fs_delete_file` | Delete a file |
| `fs_list_directory` | List files in a directory |
| `fs_file_exists` | Check whether a file exists |
| `fs_create_directory` | Create a directory |
| `fs_move_file` | Move or rename a file |
| `fs_copy_file` | Copy a file |

### Data, UI & System

| Tool | Description |
|------|-------------|
| `data_scan_path` | Scan a folder for MapInfo-compatible data files |
| `data_open_file` | Open a spatial data file (auto-detects format) |
| `ui_input` | Show an input dialog to collect values from the user |
| `shell_run` | Run an external program or shell command |
| `system_get_preferences` | Return MapInfo Pro system preferences |

---

## MCP Client Quick Start

The server exposes an SSE endpoint at `http://localhost:3100/sse`. MapInfo Pro must be running with the add-in loaded before connecting.

### VS Code / GitHub Copilot

Add to your VS Code `mcp.json` (or workspace `.vscode/mcp.json`):

```json
{
  "servers": {
    "mapinfo-pro": {
      "type": "sse",
      "url": "http://localhost:3100/sse"
    }
  }
}
```

- **macOS/Linux:** `~/.vscode/mcp.json`
- **Windows:** `%APPDATA%\Code\User\mcp.json`

### Claude Desktop

Claude Desktop does not natively support SSE. Use [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) as a bridge (requires Node.js 18+):

```json
{
  "mcpServers": {
    "mapinfo-pro": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:3100/sse"
      ]
    }
  }
}
```

Open or create `claude_desktop_config.json`:

| Platform | Path |
|----------|------|
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |

Add the snippet above (merging with any existing `mcpServers` entries), then restart Claude Desktop.

> A ready-to-copy example is in [`claude_desktop_config.example.json`](claude_desktop_config.example.json).

### Other Clients (IntelliJ, Visual Studio, etc.)

Any client that supports SSE transport can connect directly:

| Setting | Value |
|---------|-------|
| Transport | SSE |
| URL | `http://localhost:3100/sse` |

If the client only supports stdio, use `mcp-remote` as shown in the Claude Desktop example above.

---

## Optional: Token Authentication

If the server is on a shared machine, set `McpToken` in `MapInfo-AI.config`:

```xml
<add key="McpToken" value="change-me-before-use" />
```

Clients must then pass the token as a request header:

```
X-MCP-Token: change-me-before-use
```

---

## Custom Instructions

Create or edit `mapinfo-instructions.md` next to `MapInfo-AI.dll` to inject organisation-specific context (data dictionary, preferred tools, conventions) into every AI session. The file is re-read on each new message — no restart needed.
