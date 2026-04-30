# GeoTax MCP Server

> 📦 **Download:** [geotax-sdk-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/geotax-sdk-mcp.beta.v1.0)

A standalone **Model Context Protocol (MCP)** server that exposes GeoTax SDK capabilities as tools and resources for LLM-based applications.

**Transport:** stdio (tested and working with GitHub Copilot & Claude Desktop)

---

## Overview

This MCP server provides programmatic access to GeoTax tax calculation, comparison, and knowledge base features through the standardized MCP protocol. It can be used with MCP-compatible clients such as Claude Desktop, VS Code Copilot, JetBrains Copilot, and custom LLM applications.

---

## Prerequisites

- Node.js 18+
- GeoTax SDK service running and reachable (default: `http://localhost:8080`)

---

## Installation

```bash
cd geotax-mcp-server
npm install
```

---

## Configuration

Set environment variable to point to your GeoTax service:

```bash
# Default: http://localhost:8080
export GEOTAX_BASE_URL=http://localhost:8080
```

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_tax` | Get tax rate and jurisdiction information for a US address |
| `compare_tax` | Compare tax rates between two US addresses |
| `get_tax_info` | Get information about GeoTax API response fields, datasets, or system |

### `get_tax`

**Input:**
```json
{ "address": "30 Pleasant St Northampton MA" }
```

### `compare_tax`

**Input:**
```json
{
  "address1": "1 Global View Troy NY",
  "address2": "30 Pleasant St Northampton MA"
}
```

### `get_tax_info`

**Input:**
```json
{ "question": "what is preciselyId?" }
```

---

## MCP Resources

| URI | Description |
|-----|-------------|
| `geotax://fields` | Complete list of all GeoTax API response fields |
| `geotax://datasets` | Information about GeoTax datasets (SPD, IPD, etc.) |
| `geotax://response-structure` | Full API response JSON structure |

---

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "precisely-geotax-sdk": {
      "command": "node",
      "args": ["C:/path/to/geotax-mcp-server/src/index.js"],
      "env": {
        "GEOTAX_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

---

## VS Code Configuration

```json
{
  "servers": {
    "precisely-geotax-sdk": {
      "type": "stdio",
      "command": "node",
      "args": ["./src/index.js"],
      "cwd": "${workspaceFolder}/core-geotax-sdk",
      "env": {
        "GEOTAX_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

---

## Integration with JetBrains (GitHub Copilot)

```json
{
  "servers": {
    "precisely-geotax-sdk": {
      "type": "stdio",
      "command": "node",
      "args": ["C:/path/to/geotax-mcp-server/src/index.js"],
      "env": {
        "GEOTAX_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

---

## Transport

| Transport | Command | Best For |
|-----------|---------|----------|
| stdio | `node src/index.js` | Claude Desktop, VS Code, JetBrains Copilot |

---

## Server Repository

- **Release:** [geotax-sdk-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/geotax-sdk-mcp.beta.v1.0)
- **Issues:** [GitHub Issues](../../../issues)
- **GeoTAX Docs:** https://support.precisely.com/geotax-sdk

---

## License

The GeoTAX SDK is subject to a Precisely SDK license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).
