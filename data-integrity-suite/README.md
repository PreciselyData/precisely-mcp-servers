# How to Access DIS MCP Tools

This document covers two ways to connect to the DIS MCP server remotely using the DIS API Gateway:

- **[Part 1: VS Code / GitHub Copilot](#part-1-vs-code--github-copilot)** — configure via `mcp.json`
- **[Part 2: Microsoft Copilot Studio](#part-2-microsoft-copilot-studio)** — create a custom agent

The **DIS MCP API Gateway URL**:

```
https://dis-developer.api.cloud.precisely.com/dis-mcp/mcp
```

---

## Create an API Key

1. Log into your Data Integrity Suite workspace at [https://cloud.precisely.com](https://cloud.precisely.com).
2. Click **Account**.
3. Click the **API Keys** tab.
4. Click **Generate API Key** or select an existing API key.
5. The `api_key:api_secret` pair is encoded as a Base64 string and used in an `Authorization` header:

   ```
   Apikey OWMxZGFmODA4ZTI1ZDQ5ZjpCdDAyZ2NpQjNYTjlac3U3eEZNVGJHU3NZZE5OQnBrZA==
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
      "url": "https://dis-developer.api.cloud.precisely.com/dis-mcp/mcp",
      "headers": {
        "Authorization": "Apikey OWMxZGFmODA4ZTI1ZDQ5ZjpCdDAyZ2NpQjNYTjlac3U3eEZNVGJHU3NZZE5OQnBrZA=="
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
| **Server URL** | `https://dis-developer.api.cloud.precisely.com/dis-mcp/mcp` |

**Authentication** — select **API Key**:

- **Type**: `Header`
- **Header name**: `Authorization`

Click **Create** to create the MCP connection.

### Step 4a: Connect to the DIS MCP Server

After the MCP tool is created, you must explicitly connect it before the agent can call its tools.

1. On the **Add Tools** page, **Connection** shows **Not connected**
2. Click the dropdown menu next to it and select **Create new connection**
3. When prompted, enter your Apikey value created above:
   - **Value**: `Apikey OWMxZGFmODA4ZTI1ZDQ5ZjpCdDAyZ2NpQjNYTjlac3U3eEZNVGJHU3NZZE5OQnBrZA==`
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
