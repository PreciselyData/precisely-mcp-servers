# Precisely DQ+ MCP Server

> **Registry Entry** | Server: `precisely-dqplus` | Status: 🟡 Planned

DQ+ (Data Quality Plus) is Precisely's cloud-native data quality service, providing rule-based validation, cleansing, enrichment, and quality scoring via a GraphQL API. This MCP server exposes DQ+ capabilities to AI assistants.

---

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `dqplus_validate` | Validate records against DQ+ rule sets and return violations |
| `dqplus_cleanse` | Apply cleansing transformations to input records |
| `dqplus_enrich` | Enrich records with DQ+ reference data |
| `dqplus_score` | Return quality scores and metrics for input records |
| `dqplus_graphql` | Raw GraphQL passthrough for advanced DQ+ queries |

> ⚠️ Tool list is indicative. Final tool names and count will be confirmed during implementation.

---

## Prerequisites

- Access to a DQ+ instance (cloud or on-premise)
- Valid DQ+ API key
- Knowledge of your DQ+ GraphQL endpoint URL
- Python 3.8+

---

## Authentication

| Environment Variable | Description |
|----------------------|-------------|
| `DQPLUS_API_ENDPOINT` | DQ+ GraphQL endpoint URL (e.g., `https://your-dqplus-instance/graphql`) |
| `DQPLUS_API_KEY` | DQ+ API key for authentication |

---

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "precisely-dqplus": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\dq-plus-mcp",
      "env": {
        "DQPLUS_API_ENDPOINT": "https://your-dqplus-instance/graphql",
        "DQPLUS_API_KEY": "your_api_key"
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
    "precisely-dqplus": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "${workspaceFolder}/../dq-plus-mcp",
      "env": {
        "DQPLUS_API_ENDPOINT": "${input:dqplus-endpoint}",
        "DQPLUS_API_KEY": "${input:dqplus-api-key}"
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

## GraphQL Endpoint Formats

| Deployment Type | Endpoint Pattern |
|-----------------|-----------------|
| Cloud (SaaS) | `https://dqplus.precisely.com/graphql` |
| On-Premise | `https://your-host/dqplus/graphql` |
| Docker (local) | `http://localhost:8080/graphql` |

---

## Server Repository

- **Code:** External — link TBD once the DQ+ MCP repo is established
- **Issues:** [GitHub Issues](../../../issues)
- **DQ+ Docs:** https://support.precisely.com/dq-plus

---

## License

Refer to the DQ+ license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).

