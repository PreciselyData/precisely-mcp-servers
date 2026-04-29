# Precisely MCP Servers — Architecture

---

## Deployment Architecture

MCP servers in this registry span two deployment patterns — **on-premises SDK** servers (running locally alongside the AI client) and **cloud/enterprise web servers** (secured with TLS, SSO, and OAuth 2.1).

```mermaid
graph TB
    subgraph AI_Client["🤖 AI Client (Claude / Copilot / Custom)"]
        Client["MCP Client"]
    end

    subgraph OnPrem["🖥️ On-Premises / Local Deployment"]
        direction TB
        STDIO["stdio transport"]
        SDK_GA["precisely-ga-sdk\nGeographic Addressing SDK"]
        SDK_GTX["precisely-geotax-sdk\nGeoTAX SDK"]
        SDK_GA & SDK_GTX --> STDIO
    end

    subgraph Cloud["☁️ Cloud / Enterprise Web Deployment"]
        direction TB
        LB["Load Balancer / API Gateway"]

        subgraph Auth["🔐 Auth Layer"]
            TLS["TLS / SSL"]
            SSO["SSO / SAML 2.0"]
            OAUTH["OAuth 2.1 + PKCE"]
            TLS --> SSO --> OAUTH
        end

        subgraph Servers["MCP HTTP Servers"]
            DIS["precisely-dis-locate\nDIS / Locate APIs v2"]
            SPEC["precisely-spectrum\nSpectrum Platform"]
            TRIL["precisely-trillium\nTrillium Quality"]
            DQP["precisely-dqplus\nDQ+"]
            EW["precisely-enterworks\nProduct MDM"]
            ANA["precisely-analyze\nPrecisely Analyze"]
        end

        LB --> Auth --> Servers
    end

    subgraph PreciselyCloud["🌐 Precisely Cloud APIs"]
        API["developer.cloud.precisely.com"]
    end

    Client -- "stdio (local process)" --> STDIO
    Client -- "HTTPS + Bearer Token" --> LB
    Servers --> API
```

> **On-Premises SDKs** (`ga-sdk`, `geotax-sdk`) run as local processes communicating over **stdio** — no network exposure, credentials stay on-device.
> **Web servers** expose an **HTTP/SSE** or **Streamable HTTP** endpoint, protected by TLS termination at the gateway, SSO for identity federation, and OAuth 2.1 with PKCE for token-based access.

---

## Claude Desktop — Multi-Server Configuration Example

Add multiple Precisely MCP servers to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "precisely-dis-locate": {
      "command": "python",
      "args": ["-m", "mcp_servers"],
      "cwd": "C:\\path\\to\\dis-locate-apis-v2",
      "env": {
        "PRECISELY_API_KEY": "your_api_key",
        "PRECISELY_API_SECRET": "your_api_secret"
      }
    },
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

Each product folder contains a ready-to-copy `claude_desktop_config.example.json`.

