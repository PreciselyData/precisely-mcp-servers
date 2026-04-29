# DQ+ MCP Server Setup Guide

> **Last Updated:** April 2026

This guide provides instructions for connecting to the DQ+ MCP (Model Context Protocol) server, enabling AI assistants like Claude to interact with DQ+ GraphQL APIs.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Available Tools](#available-tools)
- [GraphQL APIs](#graphql-apis)
- [Configuration](#configuration)
  - [Option 1: Claude Desktop Custom Connector](#option-1-claude-desktop-custom-connector)
  - [Option 2: Using mcp-remote](#option-2-using-mcp-remote)
- [Configuration Parameters](#configuration-parameters)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## Prerequisites

### User Requirements

- Active DQ+ account with API access
- Valid tenant ID and OAuth client ID (provided by your DQ+ administrator)
- **For mcp-remote option:** Node.js v20.x or later installed

### Server Requirements

- MCP server is enabled and configured for your tenant in DQ+ API Settings
- The configured OAuth 2 authorization server (e.g., Okta, Entra ID) must have the following redirect URI registered:
  ```
  https://claude.ai/api/mcp/auth_callback
  ```
---

## Available Tools

Once connected, the following MCP tools are available:

| Tool | Description |
|------|-------------|
| `dqplus_graphql_schema_introspect` | Returns GraphQL schema metadata visible to the current user via introspection |
| `dqplus_graphql_execute` | Executes a GraphQL query or mutation with optional variables and operationName |

---

## GraphQL APIs

DQ+ exposes a single GraphQL endpoint with **Query** and **Mutation** root types covering the following domains.

### Queries

| Domain | Description                                                                                                                                                                                                           |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Environments** | List, read, and export environment definitions, settings, settings history, and calendars                                                                                                                             |
| **Pipelines & Stages** | Read pipelines (by ID, name, or env), paths, stages (by ID, UUID, or alternate ID), and stage type metadata. List dependents/dependencies for stages and field paths; list version history and retrieve version text. |
| **Data Store** | Read definitions, query data (paginated), generate fields/schema, test DB connections, upload status, file delimiter detection, and currency listing                                                                  |
| **Data View** | Read definitions and query data (paginated)                                                                                                                                                                           |
| **Case Store** | Read definitions and query case data (paginated)                                                                                                                                                                      |
| **Dashboards** | Read dashboard/dashbook definitions                                                                                                                                                                                   |
| **Execution & Scheduling** | Check execution status/completion, query execution history, future schedules, and cluster information                                                                                                                 |
| **Audit Trail & Activity Log** | Query audit trail events and activity logs for data/case stores                                                                                                                                                       |
| **Import/Export** | Start definition exports, check export/import status                                                                                                                                                                  |
| **Users & Groups** | List/read users (with filtering, sorting, pagination), read user by email/ID, list/read groups, get logged-in user info                                                                                               |
| **Server Logs** | Export server logs and check export status                                                                                                                                                                            |
| **Govern Integration** | Test connection, list configurations, list business asset types, check technical asset configuration, read sync schedules                                                                                             |
| **Spectrum Integration** | Test Spectrum connection                                                                                                                                                                                              |
| **Security** | Encrypt text                                                                                                                                                                                                          |
| **System Info** | Retrieve system information                                                                                                                                                                                           |
| **Tenant** | Read tenant info, settings, and settings history                                                                                                                                                                      |

### Mutations

| Domain | Description |
|--------|-------------|
| **Client Logging** | Submit client log events |
| **Environments** | Create, update, delete environments; manage environment groups; replace environment calendars |
| **Pipelines** | CRUD for pipelines, paths, and pipeline items; manage pipeline item watchers |
| **Data Store** | Create, update data store definitions; upload, delete (single/all) data store data (by stage ID or alternate ID) |
| **Data View** | Create and update data view definitions |
| **Case Store** | Transition, take, and merge cases |
| **Execution** | Execute, rerun, rollback, and terminate stage executions |
| **Import** | Prepare (upload) and execute item definition imports |
| **Users** | Create, update, enable, disable users; add/remove users from groups; populate users; manage user preferences |
| **Groups** | Create, update, delete groups |
| **Govern** | Configure technical assets, create Govern configuration, push metadata, manage sync schedules |
| **Tenant** | Update tenant info |

---

## Configuration

### Option 1: Claude Desktop Custom Connector

Use the built-in custom connector feature for a simplified setup.

1. Open Claude Desktop
2. Navigate to **Customize** → **Connectors** → **Add custom connector**
3. Configure the following settings:

| Field | Value |
|-------|-------|
| Remote MCP Server URL | `https://{{dqplus-server-url}}/mcp/{{tenantId}}` |
| Client ID | `{{clientId}}` |

4. Save and restart Claude Desktop if prompted

### Option 2: Using mcp-remote

For environments requiring manual configuration, use the `mcp-remote` package.

1. Locate your Claude Desktop configuration file:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add or update the configuration with the following:

```json
{
  "mcpServers": {
    "dqplus-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://{{dqplus-server-url}}/mcp/{{tenantId}}",
        "--static-oauth-client-info",
        "{\"client_id\":\"{{clientId}}\"}"
      ]
    }
  }
}
```

> **Note (Windows):** If `npx` is not in your system PATH, use the full path to `npx.cmd`:
> ```json
> "command": "C:\\Program Files\\nodejs\\npx.cmd"
> ```

3. Save the file and restart Claude Desktop

---

## Configuration Parameters

Replace the following placeholders with your environment-specific values:

| Parameter | Description                          | Example |
|-----------|--------------------------------------|---------|
| `{{dqplus-server-url}}` | Base URL of your DQ+ server instance | `dqplus.example.com` |
| `{{tenantId}}` | Your organization's tenant ID in DQ+ | `acme-corp` |
| `{{clientId}}` | OAuth client ID for authentication   | `dqplus-mcp-client` |

---

## Troubleshooting

### Connection Issues

- **Verify network connectivity** to the DQ+ server URL
- **Check firewall rules** to ensure outbound HTTPS connections are allowed on port 443
- **Validate credentials** — confirm your client ID is correct and has appropriate permissions

### Tools Not Appearing

- Restart Claude Desktop after configuration changes, and kill any lingering `claude` processes
- Verify the MCP server URL includes the correct tenant ID
- Check Claude Desktop logs for connection errors

### Authentication Errors

- Ensure your client ID is registered and active in DQ+
- Verify your account has the necessary permissions for MCP access
- Contact your DQ+ administrator if issues persist

---

## Support

For additional assistance, contact your DQ+ administrator or refer to the official DQ+ documentation.
