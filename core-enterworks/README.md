# Enterworks GraphQL MCP Server

The **enable-mcp** module exposes an Enterworks MDM (Master Data Management)
system as both a GraphQL API and an
[MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server.
AI assistants such as Claude Desktop can query and mutate MDM data through
natural-language tool calls, while traditional HTTP clients can use the
standard GraphQL endpoint.

---

## Table of Contents

1. [Why GraphQL for MDM?](#why-graphql-for-mdm)
2. [Mode 1 — Enterprise SSO (OAuth 2.1 PKCE)](#mode-1--enterprise-sso-oauth-21-pkce)
3. [Mode 2 — Personal / Desktop](#mode-2--personal--desktop)
4. [Mode 3 — Shared Lab Server, No SSO (standalone)](#mode-3--shared-lab-server-no-sso-standalone)
5. [Mode 4 — Cloud-Connected / Zero-Install (Custom MCP Connector)](#mode-4--cloud-connected--zero-install-custom-mcp-connector)
6. [Command-Line Reference](#command-line-reference)
7. [Sub-Packages](#sub-packages)
8. [Experimental Extensions](#experimental-extensions)

---

## Why GraphQL for MDM?

Every Enterworks implementation is different.  Repositories, attributes,
relationships, and hierarchies are configured by each customer to model
*their* data — products, locations, suppliers, assets, or whatever the
domain requires.  There is no single fixed API contract that describes what
"an Enterworks system" looks like.

This is the fundamental challenge: **how do you let an AI assistant
understand a system whose shape is only known at runtime?**

### The Dynamic Schema

When the MCP server starts, it connects to the target Enterworks instance,
reads the repository metadata (types, attributes, links, hierarchies), and
**generates a GraphQL schema on the fly** — one that is unique to that
customer's configuration.  A retailer's schema might expose `Product`,
`Supplier`, and `Category` types; a healthcare deployment might expose
`ClinicalTrial`, `Compound`, and `RegulatorySubmission`.

The schema is not hand-written.  It is a faithful projection of whatever the
MDM administrator has configured, rebuilt automatically every time the server
restarts.

### Why This Matters for AI

Large language models already understand GraphQL.  It is one of the most
well-represented API patterns in their training data.  By projecting the MDM
into a GraphQL schema, we give the LLM something it can reason about
immediately:

- **Typed fields with meaningful names** — the LLM can read the schema and
  understand that `Product.brandName` is a string, `Product.supplier` is a
  relationship to a `Supplier`, and `Product.retailPrice` is a number,
  without any documentation or prompt engineering.

- **Introspection** — the LLM can query the schema itself to discover what
  repositories exist, what fields they have, and how they relate to each
  other.  This is built into the GraphQL specification.

- **Precise queries** — instead of dumping every field of every record, the
  LLM constructs a query that asks for exactly the data it needs.  This
  keeps token usage low and responses focused.

- **Mutations with validation** — GraphQL's type system means the LLM can
  construct an update or create operation that matches the expected shape,
  and the server can reject malformed requests before they reach MDM.

Traditional REST or SOAP APIs for MDM systems tend to be generic — you pass
repository IDs and attribute codes as opaque strings.  The AI can call them,
but it has no structural understanding of *what* it is calling.  GraphQL
closes that gap: the schema **is** the documentation, and LLMs are
remarkably good at using it.

### In Practice

When a user asks Claude *"show me all products from supplier Acme with a
retail price over $50"*, the LLM:

1. Introspects the schema to find the `Product` type and its fields.
2. Constructs a GraphQL query with the appropriate filters.
3. Sends it through the MCP tool call.
4. Receives structured, typed JSON back.
5. Presents the results in natural language.

None of this requires the user to know GraphQL, or even to know what
repositories exist.  The schema gives the AI enough context to figure it out.

---

## Mode 1 — Enterprise SSO (OAuth 2.1 PKCE)

> **Audience:** Production or near-production deployments where each user
> authenticates individually through an Identity Provider (Azure AD, Okta,
> etc.) and the MCP server honours per-user MDM permissions.
>
> **Requires** the latest version of the enable2020 web server, which
> includes built-in PKCE authentication and MCP proxying support.

### Architecture

```
┌──────────────┐     HTTPS      ┌──────────────────────┐   HTTP    ┌─────────────────┐
│ Claude       │ ──────────────▶│ enable2020 Web Server │─────────▶│ MCP Server      │
│ Desktop      │                │  (PKCE + reverse      │          │  --mode          │
│              │◀──────────────│   proxy at /mcp)      │◀─────────│   proxy-token    │
└──────────────┘                └──────────────────────┘           └─────────────────┘
                                        │
                                        │  OAuth 2.1 PKCE
                                        ▼
                                ┌──────────────────┐
                                │ Identity Provider │
                                │ (Azure AD / Okta) │
                                └──────────────────┘
```

1. The **enable2020 web server** handles the OAuth 2.1 Authorization Code +
   PKCE flow, exchanging the authorization code for tokens and establishing
   MDM session cookies (`ewtoken`, `epimresttoken`).

2. It exposes a **reverse proxy** at a configurable path (e.g. `/mcp`) that
   injects those cookies into every request before forwarding to the
   MCP server.

3. The **MCP server** runs in **`proxy-token` mode** — it never holds
   credentials itself.  It extracts the forwarded cookies from each request
   and passes them to MDM, so every query/mutation runs under the
   authenticated user's identity and permissions.

### Starting the MCP Server (proxy-token mode)

```cmd
enable2020-mcp-server-service.exe ^
  --enterworks-url https://mdm.example.com ^
  --port 8082 ^
  --repository-group-ids "2,10006" ^
  --mode proxy-token ^
  --mdm-insecure-skip-verify
```

`--login` and `--password` are still required — the server uses these
credentials at startup to authenticate and load repository metadata
(types, attributes, links) so it can generate the GraphQL schema.  Once
running, the server does **not** use these credentials for client requests;
instead it forwards the per-user tokens from each inbound request to MDM.

### Starting the Web Server (PKCE + reverse proxy)

```cmd
enable2020-web-server-service.exe ^
  -enablePKCE=1 ^
  -samlSsoSettings="enable2020|url|https://login.microsoftonline.com/{tenant}/..." ^
  -mcpProxy="/mcp;http://localhost:8082" ^
  ...other existing flags...
```

The `-mcpProxy` flag is in the format `"{path};{targetURL}"`.  After PKCE
authentication the proxy automatically injects the session cookies.

### Claude Desktop Configuration

```jsonc
{
  "mcpServers": {
    "enterworks": {
      "url": "https://your-web-server.example.com/mcp"
    }
  }
}
```

### TLS Certificates and `--mdm-insecure-skip-verify`

In production you should use properly-signed certificates.  In practice,
many Enterworks deployments use **self-signed** or **internally-signed** TLS
certificates — especially in staging environments or on-prem installations
where purchasing public CA certificates is not prioritised.

This creates two separate TLS trust issues that both need to be addressed:

#### Issue 1: MCP Server → MDM (Go HTTP client)

The MCP server's outbound HTTPS calls to MDM will fail with certificate
verification errors.  Add `--mdm-insecure-skip-verify` to the MCP server
command line to skip Go's TLS certificate verification for MDM connections.

> The MCP server has additional configuration options for being less strict
> with certificate validation when enterprise CA configurations cause
> unexpected verification failures.

#### Issue 2: Claude Desktop → Web Server (Node.js / Electron)

Claude Desktop is an Electron application.  When it connects to an HTTPS
endpoint with a self-signed certificate, the underlying Node.js runtime will
reject the connection by default.

To work around this, set the `NODE_TLS_REJECT_UNAUTHORIZED` environment
variable **in the Claude Desktop config**:

```jsonc
{
  "mcpServers": {
    "enterworks": {
      "url": "https://your-web-server.internal:443/mcp",
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "0"
      }
    }
  }
}
```

**What this does:**  Tells the Node.js process inside Claude Desktop to skip
TLS certificate validation for connections to this MCP server.

**Why it's necessary on a budget:**  A properly-signed wildcard or SAN
certificate from a public CA eliminates this entirely.  But if your
organisation uses a private PKI, self-signed certs, or the MDM appliance
ships with its own CA, the Claude Desktop Electron runtime has no way to
trust that CA without this override.

> ⚠️ **Security trade-off:** Setting `NODE_TLS_REJECT_UNAUTHORIZED=0`
> disables certificate validation for the Claude Desktop process.  In a
> controlled internal network this is an acceptable pragmatic compromise.
> On an untrusted network it exposes you to man-in-the-middle attacks.
> The proper fix is to install your internal CA's root certificate into the
> operating system's trust store so both Go and Electron trust it natively.

---

## Mode 2 — Personal / Desktop

> **Audience:** A power user who wants Claude Desktop to talk directly to an
> Enterworks MDM instance that is not configured for SSO.

### How It Works

When Claude Desktop (in developer mode) launches the EXE, the server
automatically figures out that it is being used directly by Claude — a
direct, single-user connection between Claude and your MDM instance.

### Setup

1. **Download the binary** from the GitHub release:

   > **Release tag:** [`enterworks-mcp-beta.v1.0`](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/enterworks-mcp-beta.v1.0)

   | Platform | Binary |
   |----------|--------|
   | Windows  | `enable2020-mcp-server-service-windows-amd64.exe` |
   | Linux    | `enable2020-mcp-server-service-linux-amd64` |
   | macOS    | `enable2020-mcp-server-service-darwin-amd64` |

   Place the binary in a convenient local folder, e.g.:
   - **Windows:** `C:\Enterworks\mcp-server\`
   - **Linux / macOS:** `~/enterworks/mcp-server/`

   On Linux and macOS, make the binary executable after downloading:
   ```bash
   chmod +x enable2020-mcp-server-service-linux-amd64
   # or
   chmod +x enable2020-mcp-server-service-darwin-amd64
   ```

2. **Edit `claude_desktop_config.json`:**

   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

   Add an entry under `"mcpServers"` — adjust the path and binary name for your platform:

   **Windows:**
   ```jsonc
   {
     "mcpServers": {
       "enterworks": {
         "command": "C:\\Enterworks\\mcp-server\\enable2020-mcp-server-service-windows-amd64.exe",
         "args": [
           "--enterworks-url", "https://your-mdm-server.example.com",
           "--login", "your_username",
           "--password", "your_password",
           "--repository-group-ids", "2,10006"
         ]
       }
     }
   }
   ```

   **Linux / macOS:**
   ```jsonc
   {
     "mcpServers": {
       "enterworks": {
         "command": "/home/you/enterworks/mcp-server/enable2020-mcp-server-service-linux-amd64",
         "args": [
           "--enterworks-url", "https://your-mdm-server.example.com",
           "--login", "your_username",
           "--password", "your_password",
           "--repository-group-ids", "2,10006"
         ]
       }
     }
   }
   ```

3. **Restart Claude Desktop.**  You should see the 🔌 icon indicating the MCP
   server connected.

### Connecting to Multiple Enterworks Environments

A single copy of the EXE on your computer can connect to any Enterworks
instance you have access to — development, staging, production, different
clients — without installing anything on those remote machines.  Just add
one entry per environment in `claude_desktop_config.json`:

```jsonc
{
  "mcpServers": {
    "enterworks-dev": {
      "command": "C:\\Enterworks\\mcp-server\\enable2020-mcp-server-service-windows-amd64.exe",
      "args": [
        "--enterworks-url", "https://dev-mdm.example.com",
        "--login", "your_username",
        "--password", "your_password",
        "--repository-group-ids", "2,10006"
      ]
    },
    "enterworks-prod": {
      "command": "C:\\Enterworks\\mcp-server\\enable2020-mcp-server-service-windows-amd64.exe",
      "args": [
        "--enterworks-url", "https://prod-mdm.example.com",
        "--login", "prod_user",
        "--password", "prod_password",
        "--repository-group-ids", "2,10006"
      ]
    }
  }
}
```

Claude Desktop will launch a separate instance of the server for each
environment.  All of them appear as distinct tool sets in the Claude
interface, so you can query or compare data across environments in a single
conversation.

### Notes

| Setting | Why |
|---------|-----|
| `--login` / `--password` | Required in the default **standalone** mode.  Every query runs as this user. |
| `--repository-group-ids` | Comma-separated list of MDM repository-group IDs that control which repositories appear in the generated GraphQL schema. |

> **Auto-detection:** When the server detects that Claude Desktop launched
> it, it automatically handles TLS certificate issues and broker
> configuration.  You do not need to pass any extra flags beyond what is
> shown above.

---

## Mode 3 — Shared Lab Server, No SSO (standalone)

> **Audience:** A team that wants to host a shared MCP endpoint on an internal
> server.  **This is a proof-of-concept / lab configuration** — every client
> shares the same MDM credentials and there is no per-user authentication.

### How It Works

The server starts in **HTTP mode** on the configured `--port` and
authenticates to MDM once at startup with a fixed `--login` / `--password`.
All inbound requests — whether from Claude Desktop's MCP client, a browser
GraphQL explorer, or `curl` — execute under that single identity.

### Installation as a Windows Service

```cmd
sc create EWGraphQL binPath= "D:\Enterworks\enable2020\mcp-server\enable2020-mcp-server-service.exe --enterworks-url https://localhost/ --port 8082 --repository-group-ids \"2,10006\" --mode standalone --login system --password system --mdm-insecure-skip-verify --no-broker" start= auto
```

Or start interactively for testing:

```cmd
enable2020-mcp-server-service.exe ^
  --enterworks-url https://your-mdm-server.example.com ^
  --port 8082 ^
  --repository-group-ids "2,10006" ^
  --mode standalone ^
  --login system ^
  --password system ^
  --no-broker ^
  --mdm-insecure-skip-verify
```

### Connecting Claude Desktop to a Remote Standalone Server

Because the server is HTTP-based, you configure Claude Desktop to reach it as
a **remote MCP server URL** rather than launching a local process:

```jsonc
{
  "mcpServers": {
    "enterworks-cloud": {
      "url": "http://your-server.internal:8082/mcp"
    }
  }
}
```

### ⚠️ Security Warning

This mode is **inherently insecure** for anything beyond a PoC:

- A single set of credentials serves all clients — there is no audit trail
  per user.
- No OAuth, no SSO, no token rotation.
- The HTTP endpoint has no built-in authentication; anyone who can reach the
  port can issue GraphQL mutations.

**Do not expose this to the public internet.**  Use Mode 1 for production.

---

## Mode 4 — Cloud-Connected / Zero-Install (Custom MCP Connector)

> **Audience:** End users who should never have to download an EXE, edit a
> config file, or think about infrastructure.  This is the **premium
> deployment model** — the most seamless user experience, but also the most
> expensive to stand up because it requires cloud-accessible infrastructure
> with proper TLS and OAuth.

### Why This Is the Most Expensive Option

In Modes 1–3 the MCP server runs close to the MDM instance — on the same
machine, on the same network, or on the user's own desktop.  In Mode 4, the
Enterworks environment must be **reachable from the public internet** (or at
least from Anthropic's cloud), because Claude Desktop and Claude.ai delegate
MCP tool calls out to their cloud backend, which in turn connects back to
your server.  That round-trip means:

- A **publicly-routable HTTPS endpoint** with a valid certificate from a
  recognised CA (Let's Encrypt, DigiCert, etc.) — self-signed will not work.
- A **registered OAuth 2.1 client** in your Identity Provider so the
  browser-based PKCE login flow works for any user, anywhere.
- Firewall rules, DNS, and potentially a reverse proxy or tunnel to bridge
  on-prem MDM into the cloud.
- Ongoing operational cost to keep that endpoint monitored, patched, and
  available.

The payoff is that the end user does **zero setup**.

### How It Works

Recent versions of Claude Desktop (and Claude.ai on the web) support adding
MCP servers through the **Settings → Integrations** UI by simply providing a
URL.  No local EXE download, no `claude_desktop_config.json` editing, no
command-line flags.

The user enters the URL of a cloud-hosted Enterworks web server that is
running the PKCE + reverse-proxy configuration described in Mode 1.  Claude's
cloud infrastructure connects to that URL on behalf of the user, the PKCE
flow opens a browser window for login, and after authentication the MCP
tools become available — all without touching any files on disk.

### Prerequisites

| Requirement | Why |
|-------------|-----|
| **Publicly-accessible HTTPS endpoint** | Claude's cloud backend must reach the URL — not just the user's machine. |
| **Properly-signed TLS certificate** | Self-signed certs will not work — there is no way to set `NODE_TLS_REJECT_UNAUTHORIZED` in this mode. A certificate from a public CA is required. |
| **OAuth 2.1 PKCE configured** | The web server must run with `-enablePKCE=1` and a registered OAuth2 client so the browser-based login flow works. |
| **MCP reverse proxy active** | `-mcpProxy="/mcp;http://internal-mcp:8082"` on the web server, pointing at the MCP server in `proxy-token` mode. |
| **Network security / firewall** | Only port 443 needs to be exposed.  The MCP server itself stays on an internal port and is never directly reachable from the internet. |

### User Experience

1. Open **Claude Desktop → Settings → Integrations** (or visit
   [claude.ai/settings/integrations](https://claude.ai/settings/integrations)).
2. Click **Add Custom Integration** (or **Add MCP Server**).
3. Enter the URL:
   ```
   https://enterworks.yourcompany.com/mcp
   ```
4. Claude opens a browser window for OAuth login (Azure AD / Okta / etc.).
5. After authentication, the Enterworks MCP tools appear in the Claude
   interface — the user can immediately start querying MDM data in natural
   language.

### Why This Is Rare

Most Enterworks MDM deployments are on-premises or behind a VPN, making the
server unreachable from Claude's cloud infrastructure or from a user's home
network.  This mode is only viable when:

- The MDM instance is hosted in a cloud environment (AWS, Azure, etc.) with
  a public DNS entry and valid TLS.
- Or a secure tunnel (e.g. Cloudflare Tunnel, ngrok with a fixed domain) is
  set up to bridge the gap.

When the infrastructure is in place, this is by far the simplest end-user
experience — zero installation, zero configuration.

---

## Command-Line Reference

```
enable2020-mcp-server-service.exe [flags]

  --enterworks-url URL          MDM API base URL (default "http://localhost")
  --login USER                  MDM login username (default "system")
  --password PASS               MDM login password (default "system")
  --mode MODE                   Security mode: standalone | proxy-token
  --port PORT                   HTTP listen port (default 8088)
  --mcp                         Force MCP stdio mode
  --generate-sdl                Generate schema file and exit
  --exclude-directives          Omit directives from generated SDL
  --output FILE                 Schema output path (default "schema.graphql")
  --repository-group-ids IDS    Comma-separated group IDs (default "10013,2")
  --fuzzy-search                Enable fuzzy search (default true)
  --no-broker                   Use direct HTTP instead of RabbitMQ for metadata
  --mdm-insecure-skip-verify    Skip TLS verification for MDM connections
  --service-name NAME           Windows service name (default "EWGraphQL")
  --working-dir DIR             Working directory override
  --no-log-file                 Disable logging to file (console only)
  --max-item-batch-size N       Max child item IDs per batch call (default 500)
  --ollama-endpoint URL         Ollama endpoint for fuzzy search embeddings
  --ollama-model MODEL          Ollama embedding model (default nomic-embed-text)
  --weaviate-endpoint URL       Weaviate endpoint for fuzzy search
  --debug-log                   Enable verbose JSON request logging
```

---

## Experimental Extensions

> ⚗️ **This section describes experimental, pre-release capabilities.**
> Access is granted on request — contact **Precisely Product Management** to
> be onboarded into the early-access programme.

---

### Vector / Fuzzy Search via Ollama + Weaviate

When this extension is enabled, [Ollama](https://ollama.com/) generates
**vector embeddings** of every MDM record, and
[Weaviate](https://weaviate.io/) indexes those embeddings so the MCP server
can perform **semantic nearest-neighbour searches** — finding records that
*mean* the same thing as the query, not just records that share the same
characters.  Both run as Docker containers alongside the MCP server.

---

### Why Fuzzy Search Matters for AI

Standard MDM search is exact and lexical.  That works fine when a human is
typing into a search box and can try again with different words.  For an AI
assistant it is a critical failure mode, because the LLM has no way to know
which vocabulary your MDM team used when they entered the data.

**A concrete example:**

> 🧑 *"Can you find me any weatherproof connectors rated for outdoor
> installation?"*

Without vector search, the AI queries MDM for records matching
`"weatherproof"` and `"outdoor"`.  Your catalogue uses the terms
`"IP67-rated"`, `"ingress-protected"`, and `"exterior-grade"` instead.
Nothing comes back.  The AI tells the user the catalogue has no matching
products.  It does — the words just didn't line up.

> 🤖 *"I couldn't find any products matching that description in the
> catalogue."*

With vector search, the query is converted to an embedding that sits in the
same region of semantic space as `"IP67"`, `"ingress protection"`, and
`"exterior use"`.  The nearest-neighbour search finds those records
regardless of the exact words used, and the AI can give a useful answer:

> 🤖 *"I found 14 connectors in the catalogue that look relevant — the
> closest matches are the IP67-rated M12 series and the exterior-grade
> junction boxes.  Want me to pull the full specs?"*

The same dynamic plays out across misspellings, abbreviations, brand-name
variants (`"ACME Corp"` vs. `"Acme Corporation"`), and conceptual synonyms
(`"fastener"` vs. `"bolt"`).  The AI succeeds on the first attempt instead
of silently returning nothing.

---

### Availability

This feature is **not included** in the standard MCP server distribution.
To request access to the experimental Docker package and setup guide, contact:

> **Precisely Product Management**
> [https://www.precisely.com/contact](https://www.precisely.com/contact)

Include your Enterworks version, deployment mode (standalone / proxy-token),
and a brief description of your use case.
