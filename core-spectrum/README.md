# Precisely Spectrum MCP Server

> **Registry Entry** | Server: `precisely-spectrum` | Status: 🟡 Planned

Spectrum Technology Platform is Precisely's enterprise data quality and location intelligence platform. This MCP server exposes Spectrum's address verification, geocoding, routing, data quality, and enterprise integration capabilities to AI assistants.

---

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `spectrum_geocode` | Forward geocoding — convert an address to coordinates |
| `spectrum_reverse_geocode` | Reverse geocoding — convert coordinates to a structured address |
| `spectrum_verify_address` | CASS/SERP address verification and standardization |
| `spectrum_route` | Point-to-point routing and distance calculation |
| `spectrum_data_quality` | Record matching, deduplication, and data quality scoring |

> ⚠️ Tool list is indicative. Final tool names and count will be confirmed during implementation.

---

## Prerequisites

- Spectrum Technology Platform instance (on-premise or hosted)
- Spectrum API service enabled on the target instance
- Network access from the MCP host to the Spectrum host/port
- Python 3.8+

---

## Authentication

| Environment Variable | Description |
|----------------------|-------------|
| `SPECTRUM_HOST` | Hostname or IP of your Spectrum instance (e.g., `spectrum.company.com`) |
| `SPECTRUM_PORT` | HTTP port of the Spectrum API (default: `8080`) |
| `SPECTRUM_USERNAME` | Spectrum user account |
| `SPECTRUM_PASSWORD` | Spectrum user password |

---

## Claude Desktop Configuration

Copy and paste into `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "precisely-spectrum": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\spectrum-mcp",
      "env": {
        "SPECTRUM_HOST": "your-spectrum-host",
        "SPECTRUM_PORT": "8080",
        "SPECTRUM_USERNAME": "your_username",
        "SPECTRUM_PASSWORD": "your_password"
      }
    }
  }
}
```

See [`claude_desktop_config.example.json`](claude_desktop_config.example.json) for a ready-to-copy file.

---

## VS Code Configuration

Add to `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "precisely-spectrum": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "${workspaceFolder}/../spectrum-mcp",
      "env": {
        "SPECTRUM_HOST": "${input:spectrum-host}",
        "SPECTRUM_PORT": "8080",
        "SPECTRUM_USERNAME": "${input:spectrum-user}",
        "SPECTRUM_PASSWORD": "${input:spectrum-password}"
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

- **Code:** TBD — to be confirmed (this repo or external)
- **Issues:** [GitHub Issues](../../../issues)
- **Spectrum Docs:** https://support.precisely.com/spectrum

---

## License

Refer to the Spectrum Technology Platform license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).

