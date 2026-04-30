# Precisely Trillium Quality MCP Server

> **Registry Entry** | Server: `precisely-trillium` | Status: 🟡 Planned

Trillium Quality is Precisely's enterprise data quality platform offering data profiling, standardization, probabilistic matching, survivorship, and enrichment. This MCP server exposes Trillium Quality capabilities to AI assistants.

---

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `trillium_profile` | Profile a dataset and return quality metrics and statistics |
| `trillium_standardize` | Standardize name, address, and record fields |
| `trillium_match` | Probabilistic and deterministic record matching |
| `trillium_survive` | Survivorship and golden record creation |
| `trillium_enrich` | Enrich records with third-party reference data |

> ⚠️ Tool list is indicative. Final tool names and count will be confirmed during implementation.

---

## Prerequisites

- Trillium Quality installation (on-premise)
- Valid Trillium license file
- Database connection (for match and survive operations)
- Python 3.8+

---

## Authentication

| Environment Variable | Description |
|----------------------|-------------|
| `TRILLIUM_LICENSE_PATH` | Absolute path to the Trillium license file (e.g., `C:\trillium\license.dat`) |
| `TRILLIUM_DB_CONNECTION` | Database connection string for Trillium operations |
| `TRILLIUM_INSTALL_PATH` | Root installation directory of Trillium Quality |

---

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "precisely-trillium": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\trillium-quality-mcp",
      "env": {
        "TRILLIUM_LICENSE_PATH": "C:\\trillium\\license.dat",
        "TRILLIUM_DB_CONNECTION": "your_db_connection_string",
        "TRILLIUM_INSTALL_PATH": "C:\\Program Files\\Precisely\\Trillium"
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
    "precisely-trillium": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "${workspaceFolder}/../trillium-quality-mcp",
      "env": {
        "TRILLIUM_LICENSE_PATH": "${input:trillium-license-path}",
        "TRILLIUM_DB_CONNECTION": "${input:trillium-db-connection}"
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

- **Code:** External — link TBD once the Trillium Quality MCP repo is established
- **Issues:** [GitHub Issues](../../../issues)
- **Trillium Docs:** https://support.precisely.com/trillium

---

## License

Refer to the Trillium Quality license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).

