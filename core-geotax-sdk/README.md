# Precisely GeoTAX SDK MCP Server

> **Registry Entry** | Server: `precisely-geotax-sdk` | Status: 🟡 Planned

The GeoTAX SDK is Precisely's on-premise tax jurisdiction and rate lookup library. It determines the applicable tax jurisdictions (federal, state, county, city, district) and tax rates for any US address or coordinate, supporting sales tax compliance, SUT (Sales and Use Tax), and property tax workflows. This MCP server wraps the GeoTAX SDK for use with AI assistants.

---

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `geotax_lookup` | Look up tax jurisdiction(s) for an address or lat/lon coordinate |
| `geotax_rates` | Retrieve applicable tax rates for a jurisdiction code |
| `geotax_boundary` | Return tax boundary polygon(s) for a given location |
| `geotax_verify_address` | Address-level tax jurisdiction verification with standardization |
| `geotax_batch_lookup` | Batch tax jurisdiction lookups for multiple addresses |

> ⚠️ Tool list is indicative. Final tool names and count will be confirmed during implementation.

---

## Prerequisites

- Precisely GeoTAX SDK installed on the host machine
- Valid GeoTAX SDK license key
- GeoTAX reference data (PB TaxData) downloaded and accessible
- Python 3.8+
- GeoTAX SDK Python bindings (or REST wrapper) configured

---

## Authentication

| Environment Variable | Description |
|----------------------|-------------|
| `GEOTAX_INSTALL_PATH` | Absolute path to the GeoTAX SDK installation directory |
| `GEOTAX_LICENSE_KEY` | GeoTAX SDK license key |
| `GEOTAX_DATA_PATH` | Path to the GeoTAX reference data (PB TaxData) directory |

---

## Claude Desktop Configuration

> **Note:** The GeoTAX SDK MCP server runs as a **local stdio process** only, since it depends on a locally installed shared library and reference data.

```json
{
  "mcpServers": {
    "precisely-geotax-sdk": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\geotax-sdk-mcp",
      "env": {
        "GEOTAX_INSTALL_PATH": "C:\\PreciselySDK\\GeoTAX",
        "GEOTAX_LICENSE_KEY": "your_license_key",
        "GEOTAX_DATA_PATH": "C:\\PreciselySDK\\GeoTAX\\data"
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
    "precisely-geotax-sdk": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "${workspaceFolder}/../geotax-sdk-mcp",
      "env": {
        "GEOTAX_INSTALL_PATH": "${input:geotax-install-path}",
        "GEOTAX_LICENSE_KEY": "${input:geotax-license-key}",
        "GEOTAX_DATA_PATH": "${input:geotax-data-path}"
      }
    }
  }
}
```

---

## Transport Options

| Transport | Command | Best For |
|-----------|---------|----------|
| stdio | `python -m mcp_servers` | Claude Desktop, VS Code, Cursor, local scripts |

> ℹ️ HTTP transport is not recommended for SDK-based servers that rely on a local shared library. Use stdio for all GeoTAX SDK deployments.

---

## Supported Tax Types

| Tax Type | Supported |
|----------|-----------|
| State Sales Tax | ✅ |
| County Tax | ✅ |
| City / Municipal Tax | ✅ |
| Special District Tax | ✅ |
| Use Tax | ✅ |
| Property Tax Jurisdiction | ✅ |

---

## Data Updates

GeoTAX reference data requires updates to reflect legislative tax rate changes. Precisely publishes updated PB TaxData:
- **Quarterly** for major US rate changes
- **Monthly** for states with frequent changes (e.g., Louisiana, Colorado)

Refer to your Precisely data subscription for update procedures.

---

## Server Repository

- **Code:** External — link TBD once the GeoTAX SDK MCP repo is established
- **Issues:** [GitHub Issues](../../../issues)
- **GeoTAX Docs:** https://support.precisely.com/geotax-sdk

---

## License

The GeoTAX SDK is subject to a Precisely SDK license agreement. This MCP wrapper is subject to the license in [`dis-locate-apis-v2/LICENSE`](../dis-locate-apis-v2/LICENSE).

