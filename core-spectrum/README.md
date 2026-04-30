# Spectrum MCP Connector (Python POC)

> 📦 **Download:** [spectrum-mcp-server-beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/spectrum-mcp-server-beta.v1.0)

A Python MCP server that exposes Precisely Spectrum Platform capabilities using a **gateway model** — exactly 3 stable MCP tools instead of 1:1 endpoint mapping.

## Architecture

```
Client (Claude, Copilot, etc.)
  │
  ├── spectrum_actions_search    → Find actions by natural-language goal
  ├── spectrum_actions_describe  → Get full schema + examples for an action
  └── spectrum_actions_execute   → Run an action with validated arguments
  │
  └── Action Catalog (actions.seed.json) → 63 actions across 4 domains
        addressing (6):  addr.validate, addr.global_validate, addr.candidates, ...
        geocoding  (5):  geo.geocode, geo.reverse, geo.distance, ...
        data       (2):  data.us_database_lookup, data.parse_name
        management (50): mgmt.platform.*, mgmt.job.*, mgmt.dataflow.*,
                         mgmt.processflow.*, mgmt.datasource.*, mgmt.matching.*,
                         mgmt.geocode_config.*, mgmt.admin.*
```

The gateway model proves the architecture can scale to 100+ Spectrum APIs without growing the MCP tool surface.

## Prerequisites

- Python 3.11+
- Spectrum server running at `http://localhost:18080` (or set `SPECTRUM_BASE_URL`)

## Install

```bash
cd spectrum-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Configuration

Create a `.env` file in the project root (already gitignored):

```dotenv
SPECTRUM_BASE_URL=http://localhost:18080
SPECTRUM_USERNAME=admin
SPECTRUM_PASSWORD=admin
SPECTRUM_TOKEN_TTL=60        # optional — Bearer token lifetime in minutes (default 60)
```

The connector automatically fetches a Bearer token from Spectrum's security endpoint
(`GET /security/rest/token/access/{ttl}`) on first use, caches it, and refreshes it
transparently on 401 responses. Token is invalidated on clean shutdown.

## Run

```bash
# Reads credentials from .env automatically
python -m connector

# Or pass env vars directly
SPECTRUM_BASE_URL=http://my-host:18080 SPECTRUM_USERNAME=admin SPECTRUM_PASSWORD=admin python -m connector
```

The server starts on **stdio transport** (JSON-RPC 2.0). All diagnostic logging goes to stderr only.

## HTTP Mode (hosted deployment)

Set `MCP_TRANSPORT=http` to start an HTTP/SSE server instead of the stdio process:

```bash
MCP_TRANSPORT=http \
MCP_HTTP_PORT=8000 \
MCP_API_KEY=your-secret-key \
SPECTRUM_BASE_URL=http://127.0.0.1:18080 \
SPECTRUM_USERNAME=admin \
SPECTRUM_PASSWORD=admin \
python -m connector
```

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | `stdio` or `http` |
| `MCP_HTTP_HOST` | `0.0.0.0` | Bind host (HTTP mode only) |
| `MCP_HTTP_PORT` | `8000` | Bind port (HTTP mode only) |
| `MCP_API_KEY` | _(none)_ | Bearer key for auth; absent = unauthenticated (warning logged) |

**HTTP endpoints**:
- `GET /health` — liveness probe, no auth required
- `GET /sse` — MCP SSE stream
- `POST /messages` — MCP message posting

For full usage see [`specs/004-http-transport-docker/quickstart.md`](specs/004-http-transport-docker/quickstart.md).

### Connecting an MCP client to HTTP mode

```json
{
  "servers": {
    "spectrum-mcp": {
      "type": "sse",
      "url": "http://localhost:8000/sse",
      "headers": { "Authorization": "Bearer your-secret-key" }
    }
  }
}
```

## Docker

```bash
# Build
docker build -t spectrum-mcp:latest .

# Run (uses host network to reach Spectrum at 127.0.0.1:18080)
docker run --rm --network host \
  -e MCP_TRANSPORT=http \
  -e MCP_API_KEY=your-secret-key \
  -e SPECTRUM_BASE_URL=http://127.0.0.1:18080 \
  -e SPECTRUM_USERNAME=admin \
  -e SPECTRUM_PASSWORD=admin \
  spectrum-mcp:latest

# Or with Docker Compose (starts nginx proxy + connector together)
cp .env.example .env   # fill in real values
docker compose up -d
```

Copy `.env.example` to `.env` and fill in your credentials — it is gitignored.



`.idea/mcp.json` is already committed. Credentials are read from `.env` automatically:

```json
{
  "servers": {
    "spectrum-mcp": {
      "type": "stdio",
      "command": "/path/to/spectrum-mcp/.venv/bin/python",
      "args": ["-m", "connector"],
      "cwd": "/path/to/spectrum-mcp",
      "autoStart": true
    }
  }
}
```

Restart IntelliJ IDEA, open Copilot Chat, switch to **Agent mode**.

## Using with GitHub Copilot (VS Code)

```json
{
  "servers": {
    "spectrum-mcp": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["-m", "connector"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Example MCP Calls

### 1. Search

```json
{ "tool": "spectrum_actions_search", "arguments": { "goal": "validate a US address", "domain_hint": "addressing", "max_results": 5 } }
```

### 2. Describe

```json
{ "tool": "spectrum_actions_describe", "arguments": { "action_id": "addr.validate" } }
```

### 3. Execute

```json
{
  "tool": "spectrum_actions_execute",
  "arguments": {
    "action_id": "geo.geocode",
    "arguments": { "mainAddressLine": "1 Global View Troy NY 12180", "country": "USA" }
  }
}
```

## Demo Flow

```
1. search: "geocode an address"                    → finds geo.geocode
2. describe: geo.geocode                           → shows inputs_schema, examples
3. execute: geo.geocode + {mainAddressLine, ...}   → lat/lng from live Spectrum
```

## Authentication Flow

```
1. First execute call → session manager fetches Bearer token
   GET /security/rest/token/access/60?noCache={ts}   (Basic Auth)
   ← JWT { access_token: "eyJ..." }

2. All Spectrum API calls use:
   Authorization: Bearer eyJ...

3. On 401 → clear cached token → re-fetch → retry once

4. On shutdown:
   GET /security/rest/token/logout   (Bearer)
```

## Testing

```bash
pytest tests/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v
python scripts/smoke_test.py    # verify exactly 3 tools registered
```

## Action Catalog

### Addressing & Data (13 actions — REST)

| Action ID | Domain | Spectrum Endpoint |
|-----------|--------|-------------------|
| `addr.validate` | addressing | `GET /rest/ValidateAddress/results.json` |
| `addr.global_validate` | addressing | `GET /rest/GlobalAddressValidation/result.json` |
| `addr.candidates` | addressing | `GET /rest/GetCandidateAddresses/results.json` |
| `addr.typeahead` | addressing | `GET /rest/GlobalTypeAhead/result.json` |
| `addr.city_state_from_zip` | addressing | `GET /rest/GetCityStateProvince/results.json` |
| `addr.postal_codes_for_city` | addressing | `GET /rest/GetPostalCodes/results.json` |
| `geo.geocode` | geocoding | `POST /rest/GlobalGeocode/geocode` |
| `geo.reverse` | geocoding | `GET /rest/ReverseGeoTAXInfoLookup/results.json` |
| `geo.assign_tax_info` | geocoding | `GET /rest/AssignGeoTAXInfo/results.json` |
| `geo.distance` | geocoding | `GET /rest/CalculateDistance/results.json` |
| `geo.enrichment_lookup` | geocoding | `GET /rest/GeoEnrichmentLookup/result.json` |
| `data.us_database_lookup` | data | `GET /rest/USDatabaseLookup/result.json` |
| `data.parse_name` | data | `GET /rest/OpenNameParser/results.json` |

### Management (50 actions — SOAP + REST)

| Category | Actions | Transport |
|----------|---------|-----------|
| Platform Info (`mgmt.platform.*`) | `version`, `license`, `server_info`, `gateway_config`, `runtime_status` | SOAP + REST |
| Geocode Config (`mgmt.geocode_config.*`) | `dictionaries`, `countries`, `capabilities`, `typeahead_dbs`, `full_config` | SOAP + REST |
| Job Management (`mgmt.job.*`) | `list`, `get`, `submit`, `cancel`, `pause`, `resume` | SOAP |
| Dataflow (`mgmt.dataflow.*`) | `list`, `get`, `validate`, `expose`, `unexpose`, `export`, `import`, `list_stages`, `list_adapters` | SOAP |
| Process Flow (`mgmt.processflow.*`) | `list`, `status`, `start`, `stop`, `export`, `import` | SOAP |
| Data Sources (`mgmt.datasource.*`) | `list`, `get`, `test`, `create`, `delete`, `list_file_servers`, `browse_files` | SOAP |
| Matching (`mgmt.matching.*`) | `list_rules`, `get_rule`, `list_bob_rules`, `get_bob_rule`, `list_libraries`, `evaluate` | SOAP |
| Administration (`mgmt.admin.*`) | `license`, `version_history`, `list_folders`, `check_permission`, `notification_status`, `list_reports` | SOAP |

## Logging

All logging goes to **stderr only** — stdout is reserved for MCP JSON-RPC frames.

## License

Proprietary — Precisely Software Inc.
