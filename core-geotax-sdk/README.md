# GeoTax MCP Server

> 📦 **Download:** [geotax-sdk-mcp.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/geotax-sdk-mcp.v1.0)


Standalone MCP server for the **Precisely GeoTax SDK**.

Exposes GeoTax tax-rate lookups and a rich knowledge base (fields, datasets,
preferences, and status codes) as MCP tools and resources, letting AI assistants
(GitHub Copilot, Claude Desktop, VS Code) answer tax questions and explain the API
without any extra tooling.

---

## Overview

```
┌──────────────────────────────────────────────────────────┐
│   MCP Client (GitHub Copilot / Claude Desktop / VS Code) │
└──────────────────────────┬───────────────────────────────┘
                           │  MCP  (stdio / JSON-RPC 2.0)
                           ▼
┌──────────────────────────────────────────────────────────┐
│              GeoTax MCP Server  (Node.js)                │
│                                                          │
│  Tools                          Resources                │
│  ─────                          ─────────                │
│  • get_tax       tax rates      geotax://fields          │
│  • compare_tax   side-by-side   geotax://datasets        │
│  • get_tax_info  knowledge base geotax://preferences     │
│                                 geotax://status-codes    │
│                                 geotax://response-struct │
└──────────────────────────┬───────────────────────────────┘
                           │  HTTP REST
                           ▼
┌──────────────────────────────────────────────────────────┐
│          GeoTax SDK Service  (localhost:8080)            │
│          GET  /localtax/v1/taxrate/byaddress             │
└──────────────────────────────────────────────────────────┘
```

---

## What's inside

| Path | Purpose |
|------|---------|
| `src/index.js` | MCP stdio server that registers tools, resources, and prompts |
| `src/http-server.js` | HTTP layer (port 3001) for browser frontend and remote MCP clients |
| `src/tools/tax-tools.js` | `get_tax` / `compare_tax` tool implementations that call the GeoTax SDK REST API |
| `src/knowledge/geotax-knowledge.js` | In-memory knowledge base: response fields, datasets, preferences, status codes |

---

## Prerequisites

### 1. Node.js 18+

```powershell
node -v
```

Install from [nodejs.org](https://nodejs.org/) if not present.

### 2. GeoTax SDK service running on port 8080

The GeoTax SDK must be running before you start this MCP server.
`get_tax` and `compare_tax` will fail without it; `get_tax_info` works offline.

Verify the service is up:

```powershell
curl "http://localhost:8080/localtax/v1/taxrate/byaddress?address=1+Global+View+Troy+NY"
```

Refer to the GeoTax SDK documentation for startup instructions.

---

## Local setup

### Step 1: Clone and install

```powershell
git clone <repo-url>
cd geotax-mcp-server
npm install
```

### Step 2: Start the GeoTax SDK service

Start the GeoTax SDK Spring Boot service on port `8080`.
The MCP server will not be able to serve `get_tax` or `compare_tax` requests without it.

### Step 3: Register the MCP server in your AI client

See the [Client setup](#client-setup) section below.

---

## MCP tools

The server exposes **three tools**. Copilot / Claude pick the right one automatically
based on how you phrase your question — you never call them by name.

---

### `get_tax`: Tax rates for a US address

Calls `GET /localtax/v1/taxrate/byaddress` and returns a formatted breakdown of
tax rates and jurisdiction details for the given address.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Full US address (e.g. `30 Pleasant St Northampton MA` or `1 Global View Troy NY 12180`) |

**Returns**

Matched address · jurisdiction (state / county / city) · sales tax rates (total / state /
county / municipal) · use tax rates · PreciselyID · confidence score · coordinates ·
census block code and tract · GeoTax key · match and location codes.

**Example prompts**

```
"What is the tax rate for 30 Pleasant St Northampton MA?"
"Get tax info for 1 Global View Troy NY 12180."
"Look up sales tax for 500 Oracle Pkwy Redwood City CA."
```

---

### `compare_tax`: Side-by-side tax comparison

Calls the GeoTax SDK for both addresses in parallel and returns a side-by-side table.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address1` | string | Yes | First US address |
| `address2` | string | Yes | Second US address |

**Returns**

Side-by-side comparison of total, state, county, and municipal sales tax rates for
both addresses, including matched address and jurisdiction for each.

**Example prompts**

```
"Compare taxes between Troy NY and Northampton MA."
"Which city has a higher sales tax, Troy NY or Northampton MA?"
"Show me the tax difference between 1 Global View Troy NY and 30 Pleasant St Northampton MA."
```

---

### `get_tax_info`: Field, dataset, preference, and status-code reference

Answers questions about the GeoTax API from an **in-memory knowledge base** — no external call is made. Covers four areas:

| Area | Example questions |
|------|-------------------|
| **Response fields** | "What is preciselyId?", "Explain confidence score", "List all census fields" |
| **Datasets** | "What is the KLD dataset?", "What is GPM vs GPQ?", "Explain SPD and IPD datasets" |
| **Preferences** | "What values does matchMode accept?", "What does taxDistrict do?", "Explain output preferences" |
| **Status codes** | "What does ZERO_RESULTS mean?", "List all response status codes", "When does DATA_NOT_LICENSED occur?" |

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | Natural-language question about GeoTax |

**Example prompts**

```
"What is preciselyId?"
"What is the confidence score and how is it calculated?"
"List all tax rate fields in the GeoTax response."
"What datasets does GeoTax use?"
"Explain the difference between GPM and GPQ."
"What values does matchMode accept?"
"What does the taxDistrict preference do?"
"What are the valid values for salesTaxRateType?"
"How do I get Vertex cross-reference keys?"
"What does ZERO_RESULTS mean?"
"When would I get DATA_NOT_LICENSED?"
"List all output preferences."
"What is the difference between PAY and PTD?"
```

---

## MCP resources

The server also exposes five **resources** (static reference documents readable
by the MCP client):

| URI | Contents |
|-----|----------|
| `geotax://fields` | All response fields grouped by category, with ETM equivalents and descriptions |
| `geotax://datasets` | Licensed dataset catalog (GPM/GPQ, KLD, GTR, KSP, IPD, PXD, VLG, TCF, TRX, ...) |
| `geotax://preferences` | All request preference options with valid values and defaults (matching / geocoding / output) |
| `geotax://status-codes` | All `status` field values (OK, ZERO_RESULTS, INVALID_CONFIGURATION, ...) |
| `geotax://response-structure` | Annotated JSON response structure with example values |

---

## Preferences reference

Preferences are sent in the POST request body under the `preferences` key. The MCP
server's `get_tax_info` tool can explain any preference in detail.

### Matching preferences (`preferences.matching`)

| Preference | Default | Valid values |
|------------|---------|--------------|
| `matchMode` | `exact` | `exact` · `close` · `relaxed` |
| `useGeoTaxAuxiliaryFile` | `yes` | `yes` · `no` |
| `useUserAuxiliaryFile` | `yes` | `yes` · `no` |

### Geocoding preferences (`preferences.geocoding`)

| Preference | Default | Notes |
|------------|---------|-------|
| `usePointData` | `yes` | Set to `yes` to return a PreciselyID; requires the KLD dataset |
| `latLongAltFormat` | `DecimalSign` | Only supported format (signed decimal degrees) |
| `defaultBufferWidth` | `000005280` | Buffer in feet around district boundaries (default = 1 mile) |
| `userBoundaryBufferDistance` | `0` | Buffer in feet for user-defined boundaries |
| `latLongOffset` | `none` | Offset from street segment before boundary tests |
| `squeeze` | `yes` | Move point 50 ft toward segment centre to avoid edge cases |

### Output preferences (`preferences.output`)

| Preference | Default | Valid values |
|------------|---------|--------------|
| `taxDistrict` | `spd` | `spd` · `ipd` · `pay` |
| `taxCrossReferenceKey` | `none` | `none` · `Vertex` · `sovos` · `Thomson Reuters` |
| `salesTaxRateType` | `General` | `general` · `automotive` · `medical` · `construction` · `none` |
| `usePtc` | `no` | `yes` · `no` |
| `userBoundary` | `no` | `yes` · `no` |
| `outputCasing` | `upper` | `upper` · `mixed` |

> **Note:** When `taxCrossReferenceKey` is anything other than `none`, the SPD
> boundary file (KSP / `spd.txb`) must also be loaded.

---

## Dataset quick reference

| Code | Type | Required | Description |
|------|------|----------|-------------|
| GPM | Database | **Required** | GeoTAX Premium Masterfile (Monthly) |
| GPQ | Database | **Required** | GeoTAX Premium Masterfile (Quarterly, alternative to GPM) |
| KLD | Database | Optional | Master Location Data — enables PreciselyID (pbKey™) |
| GXF | Auxiliary | Optional | GeoTAX Auxiliary File — addresses not yet in the Premium Masterfile |
| GTR | Rate | Optional | Sales & Use Tax Rate file (general / automotive / medical / construction) |
| KSP | Boundary | Optional | Special Purpose Districts (`spd.txb`) — required with any cross-reference file |
| IPD | Boundary | Optional | Insurance Premium Districts (`ipd.txb`) |
| PXD | Boundary | Optional | Payroll Tax Districts (`pay.txb`) |
| VLG | Correspondence | Optional | Vertex L-Series cross-reference |
| VOG | Correspondence | Optional | Vertex O-Series cross-reference |
| VQG | Correspondence | Optional | Vertex Q-Series cross-reference |
| TCF | Correspondence | Optional | Sovos correspondence file |
| TRX | Correspondence | Optional | Thomson Reuters reference data |

---

## Client setup

### JetBrains: GitHub Copilot

Edit `%LOCALAPPDATA%\github-copilot\intellij\mcp.json`:

```json
{
  "servers": {
    "geotax": {
      "type": "stdio",
      "command": "node",
      "args": ["C:/Users/<your-user>/IdeaProjects/geotax-mcp-server/src/index.js"],
      "env": {
        "GEOTAX_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

Restart IntelliJ after saving.

### VS Code: GitHub Copilot

Edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "geotax": {
      "type": "stdio",
      "command": "node",
      "args": ["${workspaceFolder}/../geotax-mcp-server/src/index.js"],
      "env": {
        "GEOTAX_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

### Claude Code

Run once from any terminal:

```powershell
claude mcp add geotax -e GEOTAX_BASE_URL=http://localhost:8080 -- node "C:/gitviews/geotax/geotax-sdk-mcp/src/index.js"
```

Verify with:

```powershell
claude mcp list
# geotax: node C:/gitviews/geotax/geotax-sdk-mcp/src/index.js - Connected
```

### Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geotax": {
      "command": "node",
      "args": ["C:/Users/<your-user>/IdeaProjects/geotax-mcp-server/src/index.js"],
      "env": {
        "GEOTAX_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

---

## How it works

1. The MCP client spawns the server: `node src/index.js`
2. All client/server communication is **stdin / stdout** (JSON-RPC 2.0, MCP protocol)
3. `get_tax` and `compare_tax` make HTTP GET requests to the GeoTax SDK at `localhost:8080`
4. `get_tax_info` answers directly from the **in-memory knowledge base** with no external call needed; covers response fields, datasets, preferences (with valid values and defaults), and status codes

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `get_tax` returns an error | Verify the GeoTax SDK service is running: `curl "http://localhost:8080/localtax/v1/taxrate/byaddress?address=test"` |
| Wrong base URL | Set `GEOTAX_BASE_URL` env var in `mcp.json` to match your SDK service host and port |
| MCP server not showing in Copilot | Check `mcp.json` path, verify `node` is on your `PATH`, and restart the IDE |
| `node` not found | Install Node.js 18+ from [nodejs.org](https://nodejs.org/) and ensure it is on your `PATH` |
| `Cannot find module` | Run `npm install` in the `geotax-mcp-server` directory |
| `ZERO_RESULTS` for a valid address | GeoTax SDK may not have data loaded for that region; check SDK service logs |
| `DATA_NOT_LICENSED` | A required dataset is not loaded (e.g. KLD for PreciselyID, or KSP when using a cross-reference key) |
| `INVALID_CONFIGURATION` | Check `taxing.yaml`; a common cause is setting `taxCrossReferenceKey` without loading the SPD file |
| Port 3001 in use (Claude Code) | Pass `-e MCP_HTTP_PORT=3099` to `claude mcp add` to use a free port |

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEOTAX_BASE_URL` | `http://localhost:8080` | Base URL of the GeoTax SDK service |
| `MCP_HTTP_PORT` | `3001` | Port for the HTTP server (browser frontend / remote MCP) |

---

## License

ISC © Precisely