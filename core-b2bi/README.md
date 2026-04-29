# Precisely B2Bi MCP Server

> **Registry Entry** | Server: `precisely-B2BI` | Status: 🟡 In Development

B2Bi is Precisely's enterprise B2B integration platform, enabling organizations to manage, transform, and exchange business documents and data across trading partner networks. This MCP server exposes B2Bi capabilities to AI assistants.

---

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `b2bi_list_partners` | List configured trading partners and their connection status |
| `b2bi_send_document` | Submit a business document (EDI, XML, JSON) to a trading partner |
| `b2bi_get_transaction_status` | Retrieve the status of an in-flight or historical transaction |
| `b2bi_map_document` | Transform a document from one format to another using a B2Bi map |
| `b2bi_list_maps` | List available document transformation maps |
| `b2bi_validate_document` | Validate a document against a schema or trading partner profile |

> ⚠️ Tool list is indicative. Final tool names and count will be confirmed during implementation.

---

## Prerequisites

- Precisely B2Bi installation (on-premise or hosted)
- Valid B2Bi license
- Trading partner profiles configured in B2Bi
- Python 3.8+

---

## Authentication

| Environment Variable | Description |
|----------------------|-------------|
| `B2BI_API_ENDPOINT` | Base URL of the B2Bi REST/GraphQL API (e.g., `https://your-b2bi-instance/api`) |
| `B2BI_API_KEY` | API key for authenticating with the B2Bi platform |
| `B2BI_INSTALL_PATH` | Root installation directory of B2Bi (on-premise only) |

---

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "precisely-B2BI": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\b2bi-mcp",
      "env": {
        "B2BI_API_ENDPOINT": "https://your-b2bi-instance/api",
        "B2BI_API_KEY": "your_api_key",
        "B2BI_INSTALL_PATH": "C:\\Program Files\\Precisely\\B2Bi"
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
    "precisely-B2BI": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "${workspaceFolder}/../b2bi-mcp",
      "env": {
        "B2BI_API_ENDPOINT": "${input:b2bi-api-endpoint}",
        "B2BI_API_KEY": "${input:b2bi-api-key}"
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

- **Code:** External — link TBD once the B2Bi MCP repo is established
- **Issues:** [GitHub Issues](../../../issues)
- **B2Bi Docs:** https://support.precisely.com/b2bi

---

## License

Refer to the B2Bi license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).

