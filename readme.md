# Precisely MCP Servers

> **The Precisely MCP Registry** — a central hub for Model Context Protocol (MCP) servers across the Precisely product portfolio. Some products host their full server implementation here; others are documented here with configuration examples while their code lives in dedicated repositories.

---

## MCP Server Registry

| Server | Product                     |  Tools  | Transport | Server Location | Docs | Status |
|--------|-----------------------------|:-------:|-----------|-----------------|------|:------:|
| `precisely-dis-locate` | DIS / Locate APIs v2        |   68    | stdio, HTTP | [`dis-locate-apis-v2/`](dis-locate-apis-v2/) | [README](dis-locate-apis-v2/readme.md) | ✅ Active |
| `precisely-spectrum` | Spectrum Technology Platform |   ~10   | stdio, HTTP | | [README](core-spectrum/README.md) | 🔵 Beta |
| `precisely-trillium` | Trillium Quality            |   ~25   | stdio, HTTP | | [README](core-trillium-quality/README.md) | 🔵 Beta |
| `precisely-trillium-discovery` | Trillium Discovery          |   ~25   | stdio, HTTP | | [README](core-trillium-discovery/README.md) | 🔵 Beta |
| `precisely-dqplus` | Data360 DQ+                 | Graphql | HTTP | | [README](core-dq-plus/README.md) | 🔵 Beta |
| `precisely-enterworks` | Enterworks                  | Grpahql | HTTP | | [README](core-enterworks/README.md) | 🔵 Beta |
| `precisely-analyze` | Data360 Analyze             |   ~5    | stdio, HTTP | | [README](core-analyze/README.md) | 🔵 Beta |
| `precisely-ga-sdk` | Geographic Addressing SDK   |   ~5    | stdio | | [README](core-ga-sdk/README.md) | 🔵 Beta |
| `precisely-geotax-sdk` | GeoTAX SDK                  |   ~5    | stdio | | [README](core-geotax-sdk/README.md) | 🔵 Beta |
| `precisely-B2BI` | B2Bi                        |    ?    | stdio, HTTP | | [README](core-b2bi/README.md) | 🟡 In Development |

**Status key:**
- ✅ **Active** — fully implemented, tested, and production-ready in this repo
- 🟡 **In Development** — actively being built; not yet ready for production use
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
├── core-ga-sdk/                     ← 🔵 Beta: Geographic Addressing SDK
└── core-geotax-sdk/                 ← 🔵 Beta: GeoTAX SDK
└── core-b2bi/                       ← 🟡 In Development: B2Bi
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
