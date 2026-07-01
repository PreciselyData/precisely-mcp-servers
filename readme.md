# Precisely MCP Servers

> **The Precisely MCP Registry** — a central hub for Model Context Protocol (MCP) servers across the Precisely product portfolio. Some products host their full server implementation here; others are documented here with configuration examples while their code lives in dedicated repositories.

---

## MCP Server Registry

| Server                         | Product                     |  Tools  | Transport | Server Location                                                                                                                                    | Docs | Status |
|--------------------------------|-----------------------------|:-------:|-------|----------------------------------------------------------------------------------------------------------------------------------------------------|------|:------:|
| `precisely-dis-locate`         | DIS / Locate APIs v2        |   68    | stdio, HTTP | [`dis-locate-apis-v2/`](dis-locate-apis-v2/)                                                                                                       | [README](dis-locate-apis-v2/readme.md) | ✅ Active |
| `precisely-spectrum`           | Spectrum Technology Platform |   ~10   | stdio, HTTP | [spectrum-mcp-server-beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/spectrum-mcp-server-beta.v1.0)                 | [README](core-spectrum/README.md) | 🔵 Beta |
| `precisely-trillium-quality`   | Trillium Quality            |    7    | stdio | [trillium-quality-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/trillium-quality-mcp.beta.v1.0)               | [README](core-trillium-quality/README.md) | 🔵 Beta |
| `precisely-trillium-discovery` | Trillium Discovery          |   11    | stdio | [trillium-discovery-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/trillium-discovery-mcp.beta.v1.0)           | [README](core-trillium-discovery/README.md) | 🔵 Beta |
| `precisely-dqplus`             | Data360 DQ+                 | Graphql | HTTP | hosted only                                                                                                                                        | [README](core-dq-plus/README.md) | 🔵 Beta |
| `precisely-enterworks`         | Enterworks                  | GraphQL | HTTP | [enterworks-mcp-beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/enterworks-mcp-beta.v1.0)                           | [README](core-enterworks/README.md) | 🔵 Beta |
| `precisely-analyze`            | Data360 Analyze             |    6    | stdio | [data360-analyze-mcp-beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/data360-analyze-mcp-beta.v1.0)                 | [README](core-analyze/README.md) | 🔵 Beta |
| `precisely-ga-sdk`             | Geographic Addressing SDK   |    3    | stdio | [ga-sdk-mcp-server.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/ga-sdk-mcp-server.v1.0)                               | [README](core-ga-sdk/README.md) | ✅ Active |
| `precisely-geotax-sdk`         | GeoTAX SDK                  |    3    | stdio | [geotax-sdk-mcp.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/geotax-sdk-mcp.v1.0)                                     | [README](core-geotax-sdk/README.md) | ✅ Active |
| `precisely-matching-sdk`       | Data Quality Matching SDK   |    5    | stdio | [core-data-quality-matching-sdk.v1.3.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/core-data-quality-matching-sdk.v1.3.0) | [README](core-data-quality-matching-sdk/README.md) | ✅ Active |
| `precisely-dis-mcp`            | Data Integrity Suite (DIS)  |    3    | HTTP  | hosted only                                                                                                                                        | [README](data-integrity-suite/README.md) | 🔵 Beta |
| `precisely-mapinfo-pro`        | MapInfo Pro                 |  ~100   | HTTP/SSE | [mapinfo-pro-mcp-beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/mapinfo-pro-mcp-beta.v1.0)                         | [README](core-mapinfo-pro/README.md) | 🔵 Beta |
| `precisely-connect-appmod`     | Connect ETL/AppMod          |    1    |   stdio  | [di-appmod-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/di-appmod-mcp.beta.v1.0)                             | [README](core-connect-appmod/README.md) | 🔵 Beta |

**Status key:**
- ✅ **Active** — fully implemented, tested, and production-ready in this repo
- 🔵 **Beta** — folder and docs scaffolded; full implementation in progress or external
- 🔴 **Deprecated** — no longer maintained

---

## Deployment Architecture

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for the full deployment architecture diagram, covering on-premises SDK servers (stdio) and cloud/enterprise web servers (TLS, SSO, OAuth 2.1).

---

## Quick Start

### Use an Active Server (DIS / Locate APIs v2)

```bash
cd dis-locate-apis-v2
pip install -r requirements.txt
```

Then follow [`dis-locate-apis-v2/readme.md`](dis-locate-apis-v2/readme.md) for full setup.

### Claude Desktop — Multi-Server Configuration Example

See **[ARCHITECTURE.md](ARCHITECTURE.md#claude-desktop--multi-server-configuration-example)** for a ready-to-copy multi-server `claude_desktop_config.json`. Each product folder also contains its own `claude_desktop_config.example.json`.

---

## Repository Structure

```
precisely-mcp-servers/
│
├── README.md                        ← This file — MCP Registry
│
├── dis-locate-apis-v2/              ← ✅ HOSTED: DIS / Locate APIs (68 tools)
├── core-spectrum/                   ← 🔵 Beta: Spectrum Technology Platform
├── core-trillium-quality/           ← 🔵 Beta: Trillium Quality
├── core-trillium-discovery/         ← 🔵 Beta: Trillium Discovery
├── core-dq-plus/                    ← 🔵 Beta: DQ+
├── core-enterworks/                 ← 🔵 Beta: Enterworks MDM
├── core-analyze/                    ← 🔵 Beta: Precisely Analyze
├── core-ga-sdk/                     ← ✅ Active: Geographic Addressing SDK
├── core-geotax-sdk/                 ← ✅ Active: GeoTAX SDK
├── core-data-quality-matching-sdk/  ← ✅ Active: Data Quality Matching SDK
├── core-mapinfo-pro/                ← 🔵 Beta: MapInfo Pro (~90 tools, HTTP/SSE)
├── data-integrity-suite/            ← 🔵 Beta: Data Integrity Suite (DIS) — hosted MCP
└── core-connect-appmod/             ← 🔵 Beta: Connect ETL/AppMod
```

---

## Authentication

Each product uses its own credentials. Refer to the individual product `README.md` for environment variable names and setup instructions. The DIS / Locate server requires:

- `PRECISELY_API_KEY`
- `PRECISELY_API_SECRET`

Get Precisely API credentials at [developer.cloud.precisely.com](https://developer.cloud.precisely.com/apis).

---

## Contributing / Adding a New Server

Refer to the registry expansion specification for folder and naming conventions, standard `README.md` templates, implementation phases, and open questions.

---

## Support

- Precisely API docs: https://developer.cloud.precisely.com/apis
- Issues: Use this repository's [GitHub Issues](../../issues)

## License

See [`dis-locate-apis-v2/LICENSE`](dis-locate-apis-v2/LICENSE).
