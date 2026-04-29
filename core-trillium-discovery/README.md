# Precisely Trillium Discovery MCP Server

> **Registry Entry** | Server: `precisely-trillium-discovery` | Status: 🟡 Planned

Trillium Discovery is Precisely's enterprise data discovery and profiling platform, enabling organizations to understand, catalog, and assess data quality across diverse data sources. This MCP server exposes Trillium Discovery capabilities to AI assistants.

---

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `trillium_discovery_scan` | Scan a data source and discover available datasets and schemas |
| `trillium_discovery_profile` | Profile a dataset and return quality metrics, statistics, and anomalies |
| `trillium_discovery_catalog` | Retrieve or update the data catalog with discovered asset metadata |
| `trillium_discovery_classify` | Classify data elements by type, sensitivity, or domain (e.g., PII detection) |
| `trillium_discovery_lineage` | Trace data lineage across sources and transformations |

> ⚠️ Tool list is indicative. Final tool names and count will be confirmed during implementation.

---

## Prerequisites

- Trillium Discovery installation (on-premise or hosted)
- Valid Trillium Discovery license file
- Database / data source connectivity
- Python 3.8+

---

## Authentication

| Environment Variable | Description |
|----------------------|-------------|
| `TRILLIUM_DISCOVERY_LICENSE_PATH` | Absolute path to the Trillium Discovery license file (e.g., `C:\trillium-discovery\license.dat`) |
| `TRILLIUM_DISCOVERY_INSTALL_PATH` | Root installation directory of Trillium Discovery |
| `TRILLIUM_DISCOVERY_DB_CONNECTION` | Database connection string for discovery operations |

---

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "precisely-trillium-discovery": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\trillium-discovery-mcp",
      "env": {
        "TRILLIUM_DISCOVERY_LICENSE_PATH": "C:\\trillium-discovery\\license.dat",
        "TRILLIUM_DISCOVERY_INSTALL_PATH": "C:\\Program Files\\Precisely\\Trillium Discovery",
        "TRILLIUM_DISCOVERY_DB_CONNECTION": "your_db_connection_string"
      }
    }
  }
}
```

See [`claude_desktop_config.example.json`](claude_desktop_config.example.json) for a ready-to-copy file.

---

## VS Code Configuration

```json
{
  "servers": {
    "precisely-trillium-discovery": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "${workspaceFolder}/../trillium-discovery-mcp",
      "env": {
        "TRILLIUM_DISCOVERY_LICENSE_PATH": "${input:trillium-discovery-license-path}",
        "TRILLIUM_DISCOVERY_DB_CONNECTION": "${input:trillium-discovery-db-connection}"
      }
    }
  }
}
```

---

## Transport Options

| Transport | Command | Best For |
|-----------|---------|----------|
| stdio | `python -m mcp_servers` | Claude Desktop, VS Code, Cursor |
| Streamable HTTP | `python -m mcp_servers --transport http` | LangChain, LlamaIndex, web apps |

---

## Server Repository

- **Code:** External — link TBD once the Trillium Discovery MCP repo is established
- **Issues:** [GitHub Issues](../../../issues)
- **Trillium Docs:** https://support.precisely.com/trillium

---

## License

Refer to the Trillium Discovery license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).

