# Trillium Realtime MCP

> 📦 **Download:** [trillium-quality-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/trillium-quality-mcp.beta.v1.0)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes [Trillium Realtime](https://www.trilliumsoftware.com/) data-quality operations as tool calls for LLM agents such as GitHub Copilot.

---

## Overview

The server bridges MCP clients (e.g. Claude Desktop) to the Trillium Realtime REST API. It runs as a stdio MCP process and registers seven tools — three of which build their parameter schemas dynamically from the live project's field definitions, so agents always see the correct project-specific field names.

```
MCP Client ──stdio (JSON-RPC)──► FastMCP Server ──► Tool Handlers ──► HttpClient ──httpx──► Trillium REST API
```

### Tools

| Tool | Description |
|------|-------------|
| `ping` | Verify the backing service is reachable and measure latency |
| `get_project_description` | Return the operator-configured description for this server instance (set via `TRILLIUM_PROJECT_DESCRIPTION`), useful when multiple servers are deployed side-by-side |
| `get_project_metadata` | Retrieve the project's input, output, and match field schemas |
| `cleanse_record` | Standardize a data record using the configured Trillium project |
| `window_match` | Match one or more candidate records against each other |
| `reference_match` | Match candidate records against a master reference record |
| `get_request_stats` | Return cumulative cleansing/matching counts for the configured web key |

`cleanse_record`, `window_match`, and `reference_match` have **dynamic schemas** — parameter names are populated from the project's field definitions at server startup.

> **Field name casing**: `cleanse_record`, `window_match`, and `reference_match` accept record field names in any casing (e.g. `firstname`, `FirstName`, or `FIRSTNAME`). The MCP layer normalizes them to the canonical project casing before forwarding to the Trillium API.

---

## Prerequisites

1. **`uv` is installed** — MCP clients invoke `uvx --from <wheel>` to launch the server on demand. `uvx` creates a temporary isolated environment, installs the wheel, and runs the server automatically; no separate installation step is required. Install `uv` from [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/) if not already present.

2. **The wheel file is available** at a known absolute path on the machine where the MCP client runs.

3. **A running Trillium Realtime instance** with a **running** project.

---

## Configuration

The server is configured entirely via environment variables.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRILLIUM_BASE_URL` | Yes | — | Root URL of the Trillium service, e.g. `http://host:8080` |
| `TRILLIUM_PROJECT_DESCRIPTION` | No | `""` | Human-readable description of this server instance; used by agents to distinguish between multiple co-deployed servers |
| `TRILLIUM_API_KEY` | No | — | Web key passed as `?webKey=` on every REST call. Required when a web access key has been configured for the Trillium Realtime service (set in the TSI Web Server Administration settings) |
| `TRILLIUM_REQUEST_TIMEOUT_SECONDS` | No | `60` | Per-request HTTP timeout in seconds |
| `TRILLIUM_CA_BUNDLE` | No | — | Path to a PEM CA certificate file (or directory) used to verify TLS when `TRILLIUM_BASE_URL` is `https://`. Leave unset for the default system trust store or when using `http://`. |

> **Note:** The Trillium project must be in **Running** status (via Trillium Administrator) before the server can start. The server will exit with a descriptive error if the project is not running or returns empty field lists.

---

## MCP Client Quick Start

The primary configuration snippet for all clients uses `uvx --from` with the wheel file. Use the **absolute path** to the wheel. `TRILLIUM_API_KEY` can be omitted if no web access key has been configured for the Trillium service:

**macOS/Linux:**
```json
{
  "command": "uvx",
  "args": ["--from", "/absolute/path/to/trillium_realtime_mcp-{version}-py3-none-any.whl", "trillium-realtime-mcp"],
  "env": {
    "TRILLIUM_BASE_URL": "http://your-trillium-host:8080",
    "TRILLIUM_API_KEY": "your_trillium_web_key"
  }
}
```

**Windows:**
```json
{
  "command": "uvx",
  "args": ["--from", "C:\\absolute\\path\\to\\trillium_realtime_mcp-{version}-py3-none-any.whl", "trillium-realtime-mcp"],
  "env": {
    "TRILLIUM_BASE_URL": "http://your-trillium-host:8080",
    "TRILLIUM_API_KEY": "your_trillium_web_key"
  }
}
```

For detailed per-client configuration (VS Code / GitHub Copilot, IntelliJ, JetBrains AI Assistant, Microsoft Visual Studio), see [deployment-clients.md](deployment-clients.md).

### Claude Desktop

Open or create the Claude Desktop config file:

| Platform | Path |
|----------|------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |

Add the following (merging with any existing `mcpServers` entries):

**macOS/Linux:**
```json
{
  "mcpServers": {
    "trillium-realtime-mcp": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/trillium_realtime_mcp-{version}-py3-none-any.whl", "trillium-realtime-mcp"],
      "env": {
        "TRILLIUM_BASE_URL": "http://your-trillium-host:8080",
        "TRILLIUM_API_KEY": "your_trillium_web_key"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "trillium-realtime-mcp": {
      "command": "uvx",
      "args": ["--from", "C:\\absolute\\path\\to\\trillium_realtime_mcp-{version}-py3-none-any.whl", "trillium-realtime-mcp"],
      "env": {
        "TRILLIUM_BASE_URL": "http://your-trillium-host:8080",
        "TRILLIUM_API_KEY": "your_trillium_web_key"
      }
    }
  }
}
```

Fully quit Claude Desktop and relaunch after saving.

---

## Troubleshooting

**Server doesn't appear in Claude Desktop**
- Verify the config file exists and the JSON is valid (no missing commas, no unescaped backslashes).
- Fully quit Claude Desktop using File → Quit (macOS) or system tray → Quit (Windows) and relaunch — closing the window is not enough.
- Confirm `uvx` is on PATH: run `uvx --version` in your terminal. If missing, install [uv](https://docs.astral.sh/uv/getting-started/installation/).

**`Project not running` error on startup**
- The Trillium project must be in **Running** status via Trillium Administrator before the server can start.

**Tools return no results or connection errors**
- Confirm `TRILLIUM_BASE_URL` is reachable: `curl http://<host>:<port>/TrilliumSOAP/REST/ping`
- Check `TRILLIUM_REQUEST_TIMEOUT_SECONDS` — increase it if the Trillium service is slow to respond.

**Server crashes silently / MCP client sees no tools**
- Ensure nothing in the environment writes to stdout. The stdio MCP transport uses stdout exclusively for JSON-RPC; any stray output will corrupt the protocol.
- MCP clients suppress server stderr, so startup errors are invisible. Run the server directly in a terminal (see [Manual Installation (for Debugging)](#manual-installation-for-debugging) below) to see full error output.

**TLS certificate error when using `https://`**
- Set `TRILLIUM_CA_BUNDLE` to the path of your PEM CA bundle (e.g. `/etc/ssl/my-corp-ca.pem`).
- Verify the path exists and the file is a valid PEM certificate.

**`uvx` not found**
- Install `uv` following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/). `uvx` is included with `uv`.

**`uvx --from <wheel>` fails with path error**
- Use an **absolute path** to the wheel file. Relative paths may not resolve correctly depending on how the MCP client launches the process.

---

## Manual Installation (for Debugging)

> **Not required for MCP client integration.** MCP clients launch the server directly via `uvx --from <wheel>` — no separate installation step is needed. See [MCP Client Quick Start](#mcp-client-quick-start) above. Use manual installation only when you need to run the server outside of an MCP client to diagnose a problem.

### When to install manually

Installing the server locally lets you:

- **See server stderr in your terminal** — MCP clients swallow stderr; running the server directly in a terminal surfaces startup errors, connection failures, and Python tracebacks that would otherwise be invisible.
- **Verify environment variables interactively** — set `TRILLIUM_BASE_URL`, `TRILLIUM_API_KEY`, etc. in your shell and confirm the server connects to Trillium before touching MCP client config.
- **Confirm the project is reachable** — the server fetches field schemas at startup; a clean start proves the Trillium project is running and that the URL and key are correct.
- **Inspect tool schemas** — a running server accepts MCP JSON-RPC on stdin; tools such as [MCP Inspector](https://github.com/modelcontextprotocol/inspector) (`npx @modelcontextprotocol/inspector`) can connect to it for interactive tool testing without any MCP client.

### Option 1 — `uv tool install` from wheel (recommended)

Installs the server as a `uv`-managed tool, making `trillium-realtime-mcp` available on PATH:

```bash
uv tool install trillium_realtime_mcp-{version}-py3-none-any.whl
```

Replace `{version}` with the actual version number (e.g. `0.1.0`). Then run with environment variables set:

**macOS/Linux:**
```bash
export TRILLIUM_BASE_URL=http://your-trillium-host:8080
export TRILLIUM_API_KEY=your_web_key   # omit if no key is configured
trillium-realtime-mcp
```

**Windows (PowerShell):**
```powershell
$env:TRILLIUM_BASE_URL = "http://your-trillium-host:8080"
$env:TRILLIUM_API_KEY  = "your_web_key"   # omit if no key is configured
trillium-realtime-mcp
```

A server that starts successfully waits for JSON-RPC on stdin and prints nothing to stderr. Any startup error (bad URL, project not running, missing env var) appears immediately on stderr.

To uninstall: `uv tool uninstall trillium-realtime-mcp`

> **Requires `uv`**: Install it from [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/).

### Option 2 — Virtual environment with `pip`

Use this when `uv` is not available or you want a throwaway isolated environment.

**macOS/Linux:**
```bash
python -m venv .venv-debug
source .venv-debug/bin/activate
pip install httpx mcp pydantic
pip install trillium_realtime_mcp-{version}-py3-none-any.whl

export TRILLIUM_BASE_URL=http://your-trillium-host:8080
export TRILLIUM_API_KEY=your_web_key   # omit if no key is configured
trillium-realtime-mcp
```

**Windows (PowerShell):**
```powershell
python -m venv .venv-debug
.venv-debug\Scripts\Activate.ps1
pip install httpx mcp pydantic
pip install trillium_realtime_mcp-{version}-py3-none-any.whl

$env:TRILLIUM_BASE_URL = "http://your-trillium-host:8080"
$env:TRILLIUM_API_KEY  = "your_web_key"   # omit if no key is configured
trillium-realtime-mcp
```

Replace `{version}` with the actual version number (e.g. `0.1.0`). Discard the environment when done: `deactivate`, then delete `.venv-debug`.

---

## See Also

- [deployment-clients.md](deployment-clients.md) — Per-client deployment guide (VS Code, JetBrains, Visual Studio)
- [Trillium Software](https://www.trilliumsoftware.com/) — Trillium Realtime product page
- [Model Context Protocol documentation](https://modelcontextprotocol.io/) — MCP specification and client guides
