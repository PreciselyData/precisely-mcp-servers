# How to Access DIS MCP Tools

This document covers several ways to connect to the DIS MCP server remotely using the DIS API Gateway:

- **[Part 1: VS Code / GitHub Copilot](#part-1-vs-code--github-copilot)** — configure via `mcp.json`
- **[Part 2: Microsoft Copilot Studio](#part-2-microsoft-copilot-studio)** — create a custom agent
- **[Part 3: Claude Desktop & Claude.ai](#part-3-claude-desktop--claudeai)** — create a custom connector
- **[Part 4: Databricks](#part-4-databricks)** — create a Unity Catalog connection
- **[Part 5: Snowflake](#part-5-snowflake)** — create a Cortex agent with an external MCP server

The **DIS MCP API Gateway URLs** by region:

| Region | Host |
|--------|-----|
| `us-east-1` | `https://api.cloud.precisely.com` |
| `eu-west-1` | `https://api.eu1.cloud.precisely.com` |
| `eu-west-2` | `https://api.gb1.cloud.precisely.com` |
| `ap-southeast-2` | `https://api.au1.cloud.precisely.com` |

Throughout this guide, `<MCP_SERVER_URL>` refers to the DIS MCP API Gateway URL: `<MCP_SERVER_HOST>/mcp`.

---

## Create an API Key

1. Log into your Data Integrity Suite workspace at [https://cloud.precisely.com](https://cloud.precisely.com).
2. Click **Account**.
3. Click the **API Keys** tab.
4. Click **Generate API Key** or select an existing API key.
5. The `api_key:api_secret` pair is encoded as a Base64 string and used in an `Authorization` header:

   ```
   Apikey base64(api_key:api_secret)
   ```

6. Save the `Apikey` value — you will use it to connect to the DIS MCP server.

---

## Part 1: VS Code / GitHub Copilot

### Set Up Your MCP Server Definition

Once you have an `Apikey`, edit your `mcp.json` file and add the following entry. Use the  Apikey value created above.

```json
{
  "servers": {
    "dis-mcp": {
      "type": "http",
      "url": "<MCP_SERVER_URL>",
      "headers": {
        "Authorization": "Apikey base64(api_key:api_secret)"
      }
    }
  }
}
```

Put your Copilot chat instance into **Agent** mode, then follow
[Validating Connectivity via Chat](#validating-connectivity-via-chat) and try the
[Example Queries](#example-queries) below.

---

## Part 2: Microsoft Copilot Studio

### Prerequisites

- Access to Microsoft Copilot Studio with permission to create agents and tools
- Generative orchestration enabled in your agent (required for MCP)

> Copilot Studio supports MCP tools and resources. Tools are invoked automatically by the orchestrator.

### Step 1: Create a New Agent

1. Open **Microsoft Copilot Studio**
2. Select **Agents** from the left navigation
3. Choose **Create blank agent**
4. Provide:
   - **Name** (e.g., "DIS MCP Assistant")
   - **Description** (e.g., "An agent that searches, describes, and executes Precisely DIS actions via MCP")
   - **Instructions** — for example:
     > "You help users discover and execute Precisely data intelligence actions. Use the DIS MCP tools to search for available actions, describe their inputs and outputs, and execute them on behalf of the user."
5. Select your agent's model (e.g., GPT-4o or the default model available in your environment)
6. Save the agent

### Step 2: Enable Generative Orchestration

1. Open your agent
2. Go to **Settings**
3. Ensure **Generative orchestration** is turned **ON**

### Step 3: Add the DIS MCP Server as a Tool

1. Open your agent
2. Go to the **Tools** page
3. Select **Add a tool** → **Create New** → **Model Context Protocol**
4. This launches the MCP onboarding wizard

### Step 4: Configure the MCP Server Connection

Provide the following details in the wizard:

| Field | Value |
|---|---|
| **Server name** | `Precisely DIS MCP` |
| **Description** | `Precisely DIS MCP server — search, describe, and execute data intelligence actions` |
| **Server URL** | `<MCP_SERVER_URL>` |

**Authentication** — select **API Key**:

- **Type**: `Header`
- **Header name**: `Authorization`

Click **Create** to create the MCP connection.

### Step 4a: Connect to the DIS MCP Server

After the MCP tool is created, you must explicitly connect it before the agent can call its tools.

1. On the **Add Tools** page, **Connection** shows **Not connected**
2. Click the dropdown menu next to it and select **Create new connection**
3. When prompted, enter your Apikey value created above:
   - **Value**: `Apikey base64(api_key:api_secret)`
4. Click **Create**
5. **Connection** should now show the created connection

Click **Add and Configure** — the tool will appear on the **Tools** page.

### Step 5: Verify DIS MCP Tools Are Available

After adding the MCP server, three core tools become automatically available to the agent:

| Tool | Purpose |
|---|---|
| `precisely_actions_search` | Discover actions by natural language goal |
| `precisely_actions_describe` | Get full schema and examples for a specific action |
| `precisely_actions_execute` | Run an action with provided arguments |

Tool changes on the MCP server are dynamically reflected in Copilot Studio.

### Step 6: Test the Agent via Chat

Open **Test your agent** in Copilot Studio and follow
[Validating Connectivity via Chat](#validating-connectivity-via-chat).
Try the [Example Queries](#example-queries) below — the agent will automatically select and call the
appropriate DIS MCP tool based on what you ask.

### Step 7: Publish and Share (Optional)

1. Select **Publish**
2. Choose a channel (e.g., Microsoft Teams, Microsoft 365)
3. Configure visibility and submit for approval if required

After publishing, users can chat with the DIS MCP agent in supported channels.

---

## Part 3: Claude Desktop & Claude.ai

[Option 1 (`Custom Connectors`)](#option-1--connect-via-custom-connectors-claude-desktop--claudeai) is the recommended approach and works for both Claude Desktop and Claude.ai. [Option 2 (`mcp-remote`)](#option-2--configure-via-mcp-remote-claude-desktop-only) is Claude Desktop-only and is intended for API key auth or non-default workspace access.

### Option 1 — Connect via `Custom Connectors` (Claude Desktop & Claude.ai)

Custom connectors are configured through your Claude account and shared across all Claude clients. Even though Claude Desktop runs on your computer, the connection to the MCP server is brokered through Anthropic's infrastructure. When adding a custom connector, you go through an OAuth flow to sign in to your Precisely account. Make sure Claude Desktop and Claude.ai are signed in with the same account.

1. Navigate to [Customize > Connectors](https://claude.ai/customize/connectors).
2. Click **+** then **Add custom connector**.
3. Enter the name `Precisely DIS MCP` and the Remote MCP server URL `<MCP_SERVER_URL>` and click Continue
4. Select **Sign In Now** in Authentication and **Use your own OAuth client** in OAuth Client then enter:

   | Field | Value |
   |-------|-------|
   | **OAuth Client ID** | `0oawtlk3vhx09KMUJ4x7` |
   | **OAuth Client Secret** | *(leave blank — public client)* |

5. Click **Add**.
6. Click **Connect** and complete the Precisely SSO login.

> **Team and Enterprise:** Only an Owner can add a custom connector for the org (steps 1–5 above). Members skip straight to step 6 — navigate to [Customize > Connectors](https://claude.ai/customize/connectors), find **Precisely DIS MCP** (marked **Custom**), and click **Connect**.

> **Note:** This method authenticates via SSO and can only connect to your **default DIS workspace**. If you need to target a specific non-default workspace, use Option 2 with credentials from that workspace instead.

> **Regional limitation:** This method only works for the `us-east-1` region (`https://api.cloud.precisely.com/mcp`). For all other regions (`eu-west-1`, `eu-west-2`, `ap-southeast-2`), use [Option 2](#option-2--configure-via-mcp-remote-claude-desktop-only) instead.


### Option 2 — Configure via `mcp-remote` (Claude Desktop only)

Use this approach for service accounts or to connect to a non-default DIS workspace using an API key.

**Prerequisites:** Node.js 18+ with `npx` (bundled with Node.js). `mcp-remote` downloads automatically on first use and is cached for subsequent launches.

**Step 1:** Open the config file for your OS:

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Step 2:** Merge the following into the `mcpServers` object. Replace `Apikey base64(api_key:api_secret)` with your encoded API key from the [Create an API Key](#create-an-api-key) section above.

**Windows:**

```json
{
  "mcpServers": {
    "Precisely DIS MCP": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "mcp-remote",
        "<MCP_SERVER_URL>",
        "--header", "Authorization: Apikey base64(api_key:api_secret)"]
    }
  }
}
```

**macOS / Linux:**

```json
{
  "mcpServers": {
    "Precisely DIS MCP": {
      "command": "npx",
      "args": ["-y", "mcp-remote",
        "<MCP_SERVER_URL>",
        "--header", "Authorization: Apikey base64(api_key:api_secret)"]
    }
  }
}
```

> Header format is strict: `Authorization:Apikey <value>` (no extra space after the colon).

**Step 3:** Quit and relaunch Claude Desktop. **Precisely DIS MCP** will appear in **Customize > Connectors**.

Once connected, enable the connector per conversation via the **+** button → **Connectors** → toggle **Precisely DIS MCP** on.

Follow [Validating Connectivity via Chat](#validating-connectivity-via-chat) below.

---

## Part 4: Databricks

Databricks can register the Precisely Data Integrity Suite (DIS) external MCP server as a **Unity Catalog MCP Service**. The MCP Service uses a Unity Catalog HTTP connection to communicate with Precisely and can be used in Databricks AI workflows.

### Requirements

| Requirement | Detail |
| --- | --- |
| **Unity Catalog** | Enabled on the workspace |
| **Databricks Runtime** | 15.0 or later |
| **Region** | Workspace must be in a region where Model Serving is supported |
| **Permissions** | Permission to create connections and services in the target Unity Catalog schema (`CREATE CONNECTION` and `CREATE SERVICE`) |
| **Credentials** | Precisely DIS `api_key` and `api_secret` |

> The examples below use `main.default`, but you can use any Unity Catalog catalog and schema where you have the required permissions.

### Step 1: Open the MCP Service page

1. In Databricks, open **Catalog** from the left navigation.
2. Click **+** in the Catalog pane or **Create** in the upper-right.
3. Select **Create a service**.
4. Select **MCP service**.

The **Create MCP Service** page opens.

### Step 2: Configure the MCP Connection

Complete each section of the form as follows.

1. Under **Name**, select the catalog and schema where you want to create the service.

      For example:

      | Field | Value |
      | --- | --- |
      | **Catalog** | `main` |
      | **Schema** | `default` |
      | **Name** | `precisely_dis_mcp` |

2. Under **Connection**, select **Create new connection**.

3. For **Server URL**, enter the Precisely MCP endpoint for your region. See the regional URL table at the beginning of this document.

      `"<MCP_SERVER_URL>"`

4. Under **Authentication**, select **OAuth M2M**.

      Configure the following fields.

      | Field | Value |
      | --- | --- |
      | **Token endpoint** | `https://api.cloud.precisely.com/auth/v2/token` |
      | **Client ID** | Precisely `api_key` |
      | **Client secret** | Precisely `api_secret` |
      | **OAuth scope** | `default` |
      | **Credential exchange method** | `Header only` |

5. Click **Create & load tools**.

      Databricks connects to the Precisely MCP server and discovers the tools exposed by the server.

6. Select **tools**

      Select the MCP tools `precisely_actions_search`, `precisely_actions_describe`, `precisely_actions_execute`. Then click **Create MCP Service** to finish creating the service.
      
After the MCP Service is created, click Try in Playground to test the service. 
Follow [Validating Connectivity via Chat](#validating-connectivity-via-chat) below.

---

## Part 5: Snowflake

Snowflake supports external MCP servers through **Cortex Agents**. Once you register the DIS MCP server as an `EXTERNAL MCP SERVER`, its tools become available to Cortex Agents and can be invoked directly from Snowflake Intelligence.

### Requirements

| Requirement | Detail |
|-------------|--------|
| **Role** | `ACCOUNTADMIN` — required to create the API integration and external MCP server |
| **Cortex Agents** | Enabled on your account |
| **Cross-region inference** | Cortex must be allowed to run cross-region (see Prerequisites below) |

### Prerequisites: Enable Cortex Cross-Region Inference

Run as `ACCOUNTADMIN`:

```sql
-- Enable Cortex cross-region inference
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';

-- Verify CORTEX_ENABLED_CROSS_REGION via CLIENT_PARAMS_INFO
SELECT SYSTEM$BOOTSTRAP_DATA_REQUEST('CLIENT_PARAMS_INFO');

-- Most reliable way to confirm the parameter
SHOW PARAMETERS LIKE 'CORTEX%' IN ACCOUNT;
```

### Step 1: Create the API Integration

Replace `<OAUTH_CLIENT_SECRET>` with the OAuth client secret Precisely provides for your environment.

```sql
-- Production (us-east-1)
CREATE API INTEGRATION precisely_dis_mcp_api_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('<MCP_SERVER_URL>')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_CLIENT_ID = '0oaxc9efzsqT0oQDF4x7'
    OAUTH_CLIENT_SECRET = '<OAUTH_CLIENT_SECRET>'
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://sso.precisely.com/oauth2/ausofsdv2wu3Qs1tw4x7/v1/authorize'
    OAUTH_TOKEN_ENDPOINT = 'https://sso.precisely.com/oauth2/ausofsdv2wu3Qs1tw4x7/v1/token'
    OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
    OAUTH_REFRESH_TOKEN_VALIDITY = 86400  -- 24 hours; minimum 3600
    OAUTH_ALLOWED_SCOPES = ('openid', 'email', 'offline_access')
  )
  ENABLED = TRUE;
```

### Step 2: Create the External MCP Server

```sql
-- Production (us-east-1)
CREATE EXTERNAL MCP SERVER precisely_dis_mcp_server
  WITH DISPLAY_NAME = 'Precisely DIS MCP'
  URL = '<MCP_SERVER_URL>'
  API_INTEGRATION = precisely_dis_mcp_api_integration;
```

### Step 3: Add to a Cortex Agent

1. In the navigation menu, select **AI & ML → Agents**.
2. Select **Create agent**.
3. Select **Database and schema**, enter an **Agent object name**, then click **Create agent**.
4. Select the **Configuration** tab, then click **MCP**.
5. From the available MCP servers, find **Precisely DIS MCP** and click **Add to agent**.
6. Click **+ Add to Snowflake CoWork**, then click **Add agent**

### Step 4: Authenticate (per user)

1. In the navigation menu, select **AI & ML → Snowflake CoWork**.
2. In **Snowflake CoWork**, open the **New chat** panel and click the agent box to the right of **+** and select the agent created in **Step 3**.
3. Click **+ → Connectors → Connect** next to **PRECISELY_DIS_MCP_SERVER**, the MCP server created in **Step 2**. This redirects to the Precisely SSO login.
4. After authenticating, the connector shows as connected and the agent can invoke DIS tools automatically.

### Step 5: Test the Agent

Follow
[Validating Connectivity via Chat](#validating-connectivity-via-chat).
Try the [Example Queries](#example-queries) below — the agent will automatically select and call the
appropriate DIS MCP tool based on what you ask.

---

## Validating Connectivity via Chat

Run these queries in order to confirm the MCP server is connected and working correctly.

**1. Discovery**

`Search for actions related to geocoding an address`

You should see it invoke the `precisely_actions_search` tool and return a list of matching actions.

**2. Detail**

`Describe the geocode.address action`

You should see it invoke the `precisely_actions_describe` tool and return the action's schema and examples.

**3. Execution**

`What's the flood risk for 1600 Pennsylvania Ave NW, Washington, DC?`

You should see it invoke `precisely_actions_execute` and return a result. An authentication error
means your API key is invalid or lacks permission to execute actions — re-generate and re-encode it,
then update your configuration.

---

## Example Queries

These queries work with both VS Code Copilot and Microsoft Copilot Studio.

### Discovery

```
Search for actions related to geocoding an address
```
```
What actions are available for data quality?
```
```
Find actions for validating email addresses
```

### Describe an Action

```
Describe the geocode.address action
```
```
What inputs does validate.email require?
```

### Execute an Action

```
Geocode 123 Main St, Kansas City, MO
```
```
What's the flood risk for 1600 Pennsylvania Ave NW, Washington, DC?
```
```
Find banks near Times Square, New York
```
```
Reverse geocode coordinates 40.7484, -73.9857
```

---
