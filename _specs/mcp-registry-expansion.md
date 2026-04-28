# Specification: Precisely MCP Registry — Core Product Expansion

**Version:** 1.0.0  
**Date:** 2026-04-28  
**Branch:** `core-mcp-betas`  
**Status:** Draft

---

## 1. Overview

This specification defines the plan to evolve the `precisely-mcp-servers` repository from a single-server project into a **Precisely MCP Registry** — a central hub that:

- **Hosts** full MCP server implementations for products whose code lives directly in this repository.
- **Documents** MCP servers for products whose code lives in external repositories, providing high-level configuration guides, Claude Desktop config examples, and integration notes.
- **Serves** as the canonical reference for any AI assistant or developer who wants to connect to Precisely product data via the Model Context Protocol.

The registry will surface a **master table in `README.md`** listing every registered MCP server, its hosting location, status, transport options, and a link to its documentation.

---

## 2. Goals

| # | Goal |
|---|------|
| G1 | Establish a consistent folder and documentation structure for every registered server. |
| G2 | Add a registry table to the root `README.md` that is the single source of truth. |
| G3 | Define the seven new core Precisely product entries (see §4). |
| G4 | Provide `claude_desktop_config.json` snippet examples for every server. |
| G5 | Make it easy for future teams to onboard a new product server with minimal friction. |
| G6 | Keep the repository lightweight — not every product ships code here. |

---

## 3. Repository Structure (Target State)

```
precisely-mcp-servers/
│
├── README.md                         ← Master MCP Registry table + overview
├── _specs/                           ← Planning & specification documents
│   └── mcp-registry-expansion.md    ← This document
│
├── dis-locate-apis-v2/               ← HOSTED: DIS / Locate APIs (existing)
│   └── ...
│
├── core-spectrum/                    ← HOSTED or DOCUMENTED (see §4.1)
│   ├── README.md
│   └── claude_desktop_config.example.json
│
├── core-trillium-quality/            ← DOCUMENTED (external server)
│   ├── README.md
│   └── claude_desktop_config.example.json
│
├── core-dq-plus/                     ← DOCUMENTED (external server)
│   ├── README.md
│   └── claude_desktop_config.example.json
│
├── core-enterworks/                  ← DOCUMENTED (external server)
│   ├── README.md
│   └── claude_desktop_config.example.json
│
├── core-analyze/                     ← DOCUMENTED (external server)
│   ├── README.md
│   └── claude_desktop_config.example.json
│
├── core-ga-sdk/                      ← DOCUMENTED (external server)
│   ├── README.md
│   └── claude_desktop_config.example.json
│
└── core-geotax-sdk/                  ← DOCUMENTED (external server)
    ├── README.md
    └── claude_desktop_config.example.json
```

### 3.1 Per-Product Folder Contract

Every product folder — whether it hosts code or only documentation — **must** contain at minimum:

| File | Purpose |
|------|---------|
| `README.md` | Product overview, MCP tool summary, auth requirements, transport options, setup steps, and `claude_desktop_config.json` example. |
| `claude_desktop_config.example.json` | Ready-to-copy Claude Desktop configuration snippet. |

Folders that host a full server implementation additionally include source code, `requirements.txt`, and test files following the pattern established by `dis-locate-apis-v2/`.

---

## 4. Core Products to Register

### 4.1 Spectrum

| Attribute | Value |
|-----------|-------|
| **Product** | Spectrum Technology Platform |
| **Folder** | `core-spectrum/` |
| **Server Location** | TBD — determine whether to host here or link external repo |
| **Transport** | stdio / HTTP |
| **Auth** | Spectrum API credentials (host, port, username, password) |
| **Primary Capabilities** | Address validation, geocoding, data quality, routing, enterprise data integration |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `spectrum_geocode` — forward geocoding
- `spectrum_verify_address` — CASS/SERP address verification
- `spectrum_reverse_geocode` — coordinate → address
- `spectrum_route` — routing and distance calculations
- `spectrum_data_quality` — record matching and deduplication

**`claude_desktop_config.json` example:**
```json
{
  "mcpServers": {
    "precisely-spectrum": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\core-spectrum",
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

---

### 4.2 Trillium Quality

| Attribute | Value |
|-----------|-------|
| **Product** | Trillium Quality |
| **Folder** | `trillium-quality/` |
| **Server Location** | External — link to Trillium Quality MCP repo |
| **Transport** | stdio / HTTP |
| **Auth** | Trillium license file path + DB connection |
| **Primary Capabilities** | Data profiling, standardization, matching, survivorship, enrichment |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `trillium_profile` — data profiling and quality scoring
- `trillium_standardize` — name, address, and record standardization
- `trillium_match` — probabilistic and deterministic record matching
- `trillium_survive` — survivorship and golden record creation
- `trillium_enrich` — third-party data enrichment

**`claude_desktop_config.json` example:**
```json
{
  "mcpServers": {
    "precisely-trillium": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\trillium-quality-mcp",
      "env": {
        "TRILLIUM_LICENSE_PATH": "C:\\trillium\\license.dat",
        "TRILLIUM_DB_CONNECTION": "your_db_connection_string"
      }
    }
  }
}
```

---

### 4.3 DQ+

| Attribute | Value |
|-----------|-------|
| **Product** | DQ+ (Data Quality Plus) |
| **Folder** | `dq-plus/` |
| **Server Location** | External — link to DQ+ MCP repo |
| **Transport** | stdio / Streamable HTTP |
| **Auth** | DQ+ API endpoint + API key |
| **Primary Capabilities** | Data quality rules, validation, cleansing, enrichment via DQ+ GraphQL API |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `dqplus_validate` — validate records against DQ+ rule sets
- `dqplus_cleanse` — apply cleansing transformations
- `dqplus_enrich` — enrich records with reference data
- `dqplus_score` — return quality scores for input records
- `dqplus_graphql` — raw GraphQL passthrough for advanced queries

**`claude_desktop_config.json` example:**
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

---

### 4.4 Enterworks

| Attribute | Value |
|-----------|-------|
| **Product** | Enterworks (Product MDM / PIM) |
| **Folder** | `enterworks/` |
| **Server Location** | External — link to Enterworks MCP repo |
| **Transport** | stdio / Streamable HTTP |
| **Auth** | Enterworks host URL + username/password |
| **Primary Capabilities** | Master data management, product information, hierarchy browsing, attribute lookup, workflow |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `enterworks_search_products` — search the MDM product catalog
- `enterworks_get_product` — retrieve a product by ID with all attributes
- `enterworks_list_hierarchies` — browse product category hierarchies
- `enterworks_get_attributes` — retrieve attribute definitions for a repository
- `enterworks_graphql` — raw GraphQL passthrough for advanced MDM queries

**`claude_desktop_config.json` example:**
```json
{
  "mcpServers": {
    "precisely-enterworks": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\enterworks-mcp",
      "env": {
        "ENTERWORKS_HOST": "https://your-enterworks-instance",
        "ENTERWORKS_USERNAME": "your_username",
        "ENTERWORKS_PASSWORD": "your_password"
      }
    }
  }
}
```

---

### 4.5 Analyze

| Attribute | Value |
|-----------|-------|
| **Product** | Precisely Analyze |
| **Folder** | `analyze/` |
| **Server Location** | External — link to Analyze MCP repo |
| **Transport** | stdio / HTTP |
| **Auth** | Analyze API endpoint + API key or OAuth token |
| **Primary Capabilities** | Spatial analytics, location-based insights, territory management, map layer queries |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `analyze_spatial_query` — run spatial queries against datasets
- `analyze_buffer` — create buffers around points/polygons
- `analyze_territory` — query and manage territory definitions
- `analyze_demographic_summary` — pull demographic summaries for an area
- `analyze_layer_info` — list available map layers and metadata

**`claude_desktop_config.json` example:**
```json
{
  "mcpServers": {
    "precisely-analyze": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\analyze-mcp",
      "env": {
        "ANALYZE_API_ENDPOINT": "https://your-analyze-instance/api",
        "ANALYZE_API_KEY": "your_api_key"
      }
    }
  }
}
```

---

### 4.6 GA SDK (Geographic Addressing SDK)

| Attribute | Value |
|-----------|-------|
| **Product** | Geographic Addressing SDK (GA SDK) |
| **Folder** | `ga-sdk/` |
| **Server Location** | External — link to GA SDK MCP repo |
| **Transport** | stdio |
| **Auth** | Local SDK installation path + license key |
| **Primary Capabilities** | On-premise address verification, geocoding, postal validation, rooftop precision geocoding |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `gasdk_geocode` — high-precision on-premise geocoding
- `gasdk_verify` — postal address verification and correction
- `gasdk_reverse_geocode` — reverse geocoding from coordinates
- `gasdk_parse` — parse raw address strings into structured components
- `gasdk_batch_geocode` — batch geocoding for multiple addresses

**`claude_desktop_config.json` example:**
```json
{
  "mcpServers": {
    "precisely-ga-sdk": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\ga-sdk-mcp",
      "env": {
        "GASDK_INSTALL_PATH": "C:\\PreciselySDK\\GA",
        "GASDK_LICENSE_KEY": "your_license_key",
        "GASDK_DATA_PATH": "C:\\PreciselySDK\\GA\\data"
      }
    }
  }
}
```

---

### 4.7 GeoTAX SDK

| Attribute | Value |
|-----------|-------|
| **Product** | GeoTAX SDK |
| **Folder** | `geotax-sdk/` |
| **Server Location** | External — link to GeoTAX SDK MCP repo |
| **Transport** | stdio |
| **Auth** | Local SDK installation path + license key |
| **Primary Capabilities** | On-premise tax jurisdiction lookup, sales tax rates, use tax, SUT compliance, PB tax data |
| **Status** | 🟡 Planned |

**Key MCP Tools (anticipated):**
- `geotax_lookup` — look up tax jurisdiction for an address or coordinate
- `geotax_rates` — retrieve applicable tax rates for a jurisdiction
- `geotax_boundary` — return tax boundary polygon for a location
- `geotax_verify_address` — address-level tax jurisdiction verification
- `geotax_batch_lookup` — batch tax lookups for multiple addresses

**`claude_desktop_config.json` example:**
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

---

## 5. README.md Registry Table (Target Design)

The root `README.md` will be updated to lead with a registry table. Below is the exact target format:

```markdown
## Precisely MCP Server Registry

| Server | Product | Tools | Transport | Server Location | Docs | Status |
|--------|---------|-------|-----------|-----------------|------|--------|
| `precisely-dis-locate` | DIS / Locate APIs v2 | 68 | stdio, HTTP | This repo → `dis-locate-apis-v2/` | [README](dis-locate-apis-v2/README.md) | ✅ Active |
| `precisely-spectrum` | Spectrum Technology Platform | ~10 | stdio, HTTP | TBD | [README](core-spectrum/README.md) | 🟡 Planned |
| `precisely-trillium` | Trillium Quality | ~5 | stdio, HTTP | External repo | [README](core-trillium-quality/README.md) | 🟡 Planned |
| `precisely-dqplus` | DQ+ (Data Quality Plus) | ~5 | stdio, HTTP | External repo | [README](core-dq-plus/README.md) | 🟡 Planned |
| `precisely-enterworks` | Enterworks (Product MDM) | ~5 | stdio, HTTP | External repo | [README](core-enterworks/README.md) | 🟡 Planned |
| `precisely-analyze` | Precisely Analyze | ~5 | stdio, HTTP | External repo | [README](core-analyze/README.md) | 🟡 Planned |
| `precisely-ga-sdk` | Geographic Addressing SDK | ~5 | stdio | External repo | [README](core-ga-sdk/README.md) | 🟡 Planned |
| `precisely-geotax-sdk` | GeoTAX SDK | ~5 | stdio | External repo | [README](core-geotax-sdk/README.md) | 🟡 Planned |
```

**Status key:**
- ✅ Active — fully implemented, tested, and production-ready in this repo
- 🟡 Planned — folder and docs exist; full implementation in progress or external
- 🔵 External — implemented in a separate repository; docs and config here only
- 🔴 Deprecated — no longer maintained

---

## 6. Standard README Template for Each Product Folder

Each product `README.md` will follow this template:

```markdown
# Precisely [Product Name] MCP Server

> **Registry Entry** | Server: `precisely-[server-id]` | Status: 🟡 Planned

Brief one-paragraph description of the product and what it enables via MCP.

## MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `tool_name` | What it does |

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## Authentication

| Variable | Description |
|----------|-------------|
| `ENV_VAR` | Description |

## Claude Desktop Configuration

```json
{ ... claude_desktop_config.json snippet ... }
```

## VS Code Configuration

```json
{ ... .vscode/mcp.json snippet ... }
```

## Transport Options

| Transport | Command | Use Case |
|-----------|---------|----------|
| stdio | ... | Claude Desktop, local |
| HTTP | ... | LangChain, web apps |

## Server Repository

- **Code:** [Link to external repo or "This repository"]
- **Issues:** [Link]
- **Docs:** [Link to product docs]

## License

[License info]
```

---

## 7. Implementation Phases

### Phase 1 — Registry Foundation (this branch: `core-mcp-betas`)
- [x] Create `_specs/mcp-registry-expansion.md` (this document)
- [ ] Update root `README.md` with registry table (8 rows)
- [ ] Create placeholder folders for all 7 new products
- [ ] Add `README.md` + `claude_desktop_config.example.json` to each folder

### Phase 2 — External Server Documentation
- [ ] Coordinate with each product team to confirm external repo URLs
- [ ] Update registry table with confirmed external links
- [ ] Add product-specific tool lists as they become available
- [ ] Add VS Code `mcp.json` examples to each product folder

### Phase 3 — Hosted Server Implementations
- [ ] Determine which products will host full server code here (vs. external)
- [ ] Implement and test hosted servers following `dis-locate-apis-v2/` pattern
- [ ] Update registry status from 🟡 Planned → ✅ Active as each ships

### Phase 4 — Registry Automation (future)
- [ ] GitHub Actions workflow to validate all `claude_desktop_config.example.json` files
- [ ] Auto-generate registry table from a `registry.yaml` manifest
- [ ] Publish registry as a GitHub Pages site

---

## 8. Conventions and Standards

### Folder Naming
- Use lowercase kebab-case: `trillium-quality`, `ga-sdk`, `geotax-sdk`
- Match the MCP server ID prefix: `precisely-{folder-name}`

### Environment Variable Naming
- Prefix all env vars with the product abbreviation in UPPER_SNAKE_CASE
- Examples: `SPECTRUM_HOST`, `TRILLIUM_LICENSE_PATH`, `GEOTAX_DATA_PATH`

### MCP Tool Naming
- Prefix all tool names with the product abbreviation in snake_case
- Examples: `spectrum_geocode`, `trillium_match`, `geotax_lookup`

### Versioning
- Each product folder may version its MCP server independently
- The registry table tracks the current stable version of each server

### Transport Defaults
- **SDK-based products** (GA SDK, GeoTAX SDK): stdio only (local process)
- **API/Service-based products**: stdio + Streamable HTTP

---

## 9. Open Questions

| # | Question | Owner | Due |
|---|----------|-------|-----|
| Q1 | Will Spectrum ship code here or in an external repo? | Spectrum Team | TBD |
| Q2 | Are there existing Trillium MCP repos to link? | DQ Team | TBD |
| Q3 | What is the canonical DQ+ GraphQL endpoint format for different deployment types? | DQ+ Team | TBD |
| Q4 | Does Enterworks have an existing MCP or GraphQL bridge? | Enterworks Team | TBD |
| Q5 | Will GA SDK and GeoTAX SDK servers require Docker for distribution? | SDK Team | TBD |
| Q6 | Should this registry be published to MCP.so or another public registry? | Platform Team | TBD |

---

## 10. References

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Anthropic MCP Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [Precisely Developer Portal](https://developer.cloud.precisely.com/apis)
- [Existing DIS/Locate MCP Server](../dis-locate-apis-v2/readme.md)
- [Claude Desktop Config Reference](https://docs.anthropic.com/en/docs/agents-and-tools/mcp#connecting-to-mcp-servers)

