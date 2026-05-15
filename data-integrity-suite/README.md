# How to Access DIS MCP Tools

This document covers two ways to connect to the DIS MCP server remotely using the DIS API Gateway:

- **[Part 1: VS Code / GitHub Copilot](#part-1-vs-code--github-copilot)** — configure via `mcp.json`
- **[Part 2: Microsoft Copilot Studio](#part-2-microsoft-copilot-studio)** — create a custom agent
- **[Part 3: Claude Desktop & Claude.ai](#part-3-claude-desktop--claudeai)** — create a custom connector

The **DIS MCP API Gateway URL**:

```
https://api.cloud.precisely.com/dis-mcp/mcp
```

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
      "url": "https://api.cloud.precisely.com/dis-mcp/mcp",
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
| **Server URL** | `https://api.cloud.precisely.com/dis-mcp/mcp` |

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
3. Enter the name `Precisely DIS MCP` and the Remote MCP server URL:
   ```
   https://api.cloud.precisely.com/dis-mcp/mcp
   ```
4. Click **Advanced settings** and enter:

   | Field | Value |
   |-------|-------|
   | **OAuth Client ID** | `0oawtlk3vhx09KMUJ4x7` |
   | **OAuth Client Secret** | *(leave blank — public client)* |

5. Click **Add**.
6. Click **Connect** and complete the Precisely SSO login.

> **Team and Enterprise:** Only an Owner can add a custom connector for the org (steps 1–5 above). Members skip straight to step 6 — navigate to [Customize > Connectors](https://claude.ai/customize/connectors), find **Precisely DIS MCP** (marked **Custom**), and click **Connect**.

> **Note:** This method authenticates via SSO and can only connect to your **default DIS workspace**. If you need to target a specific non-default workspace, use Option 2 with credentials from that workspace instead.


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
        "https://api.cloud.precisely.com/dis-mcp/mcp",
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
        "https://api.cloud.precisely.com/dis-mcp/mcp",
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
