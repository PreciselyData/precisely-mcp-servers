# Deploying Trillium Realtime MCP

This guide covers deploying the Trillium Realtime MCP server across supported MCP clients using a pre-built artifact. For the Claude Desktop quick-start, see the [Claude Desktop](README.dist.md#claude-desktop) section in the distribution README.

In all configuration snippets below, `TRILLIUM_API_KEY` can be omitted if no web access key has been configured for the Trillium service.

Supported clients with dedicated instructions:
- [VS Code / GitHub Copilot](#vs-code--github-copilot)
- [JetBrains AI Assistant](#jetbrains-ai-assistant-intellij-idea-and-other-jetbrains-ides) (all platforms; IDE 2025.2+)
- [IntelliJ / GitHub Copilot](#intellij--github-copilot)
- [Microsoft Visual Studio](#microsoft-visual-studio) (Visual Studio 2022 17.14+ / 2026 with GitHub Copilot)

---

## Prerequisites

Before configuring any MCP client, ensure the following are in place:

1. **`uv` is installed** — MCP clients invoke `uvx --from <wheel>` to launch the server on demand. `uvx` creates a temporary isolated environment, installs the wheel, and runs the server automatically; no separate installation step is required. Install `uv` from [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/) if not already present.

2. **The wheel file is available** at a known absolute path on the machine where the MCP client runs. Each client config section below uses this path in the `--from` argument.

3. **A running Trillium Realtime instance** is required for full operation.

---

## VS Code / GitHub Copilot

GitHub Copilot in VS Code reads MCP server configurations from a `.vscode/mcp.json` file in your workspace root.

### Configuration

Create or open `.vscode/mcp.json` in your workspace root and add:

```json
{
    "servers": {
        "trillium-realtime-mcp": {
            "type": "stdio",
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

> **Windows path**: Replace the `--from` value with `C:\\absolute\\path\\to\\trillium_realtime_mcp-{version}-py3-none-any.whl` (double backslashes in JSON).

> **Credentials in the `env` block are for experimentation only.** The `.vscode/mcp.json` file is typically committed to version control; do not store real credentials in it. For production use, omit the `env` block and supply the variables via OS-level environment variables or a wrapper script. See [Keeping Credentials Out of MCP Config Files](#keeping-credentials-out-of-mcp-config-files).

### Reloading the config

After editing `.vscode/mcp.json`, reload the VS Code window to pick up changes: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → **Developer: Reload Window**.

### Starting the server

After saving `.vscode/mcp.json`:

1. Reload the VS Code window: `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → **Developer: Reload Window**.
2. VS Code will show a **trust dialog** on first use — review the server configuration and confirm trust. The server will not start until you do.
3. Once trusted, VS Code starts the server automatically when Copilot needs its tools. To manually start, stop, or restart at any time, run **MCP: List Servers** from the Command Palette, select `trillium-realtime-mcp`, and choose **Start** or **Restart**.

> **If the server does not appear or start**: run **MCP: List Servers**, select `trillium-realtime-mcp`, and choose **Start**. If trust was previously declined, run **MCP: Reset Trust** from the Command Palette and reload the window to be prompted again.

> **Agent mode required**: MCP tools are only available in **Agent mode**. In the Copilot Chat panel, switch the mode selector to **Agent** before invoking any Trillium tools; **Ask** is generally the default mode.

For full MCP documentation in VS Code see [Use MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers).

### Log location

Open the Output panel (`Ctrl+Shift+U`) and select **GitHub Copilot** or **MCP** from the dropdown to see server startup and tool-execution logs.

---

## IntelliJ / GitHub Copilot

GitHub Copilot in IntelliJ IDEA and other JetBrains IDEs reads MCP server configurations from a `mcp.json` file on disk.

### Configuration

**Config file location:**

| Platform | Path |
|----------|------|
| **Windows** | `%LOCALAPPDATA%\github-copilot\intellij\mcp.json` |
| **macOS** | `~/Library/Application Support/github-copilot/intellij/mcp.json` |
| **Linux** | `~/.config/github-copilot/intellij/mcp.json` |

If the file does not exist, create it. Add a `servers` block (merging with any existing entries):

```json
{
  "servers": {
    "trillium-realtime-mcp": {
      "type": "stdio",
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

> **Windows path**: Replace the `--from` value with `C:\\absolute\\path\\to\\trillium_realtime_mcp-{version}-py3-none-any.whl`.

> **Prefer to keep credentials out of the config file?** Omit the `env` block and instead supply `TRILLIUM_BASE_URL` and `TRILLIUM_API_KEY` via OS-level environment variables before launching the IDE. See [Keeping Credentials Out of MCP Config Files](#keeping-credentials-out-of-mcp-config-files).

### Starting the server

After saving the config file, restart the IDE. The most reliable way to start the MCP server and confirm its tools are available is:

1. Open the GitHub Copilot Chat panel.
2. Switch to **Agent mode** using the mode selector at the bottom of the chat input (the server is only accessible in Agent mode).
3. Click the **Configure tools** button that appears in the chat input toolbar once Agent mode is active. This triggers GitHub Copilot to connect to the MCP server and load its tools.
4. Confirm `trillium-realtime-mcp` and its tools are listed. If the server is not connected, check the Copilot output log for startup errors.

> **Agent mode required**: MCP tools are not available in Ask or Edit mode. Always switch to Agent mode before invoking Trillium tools.

### Log location

Check the GitHub Copilot output panel: **Help → Show Log in Explorer** (Windows) / **Show Log in Finder** (macOS) to open the IDE log directory. Open `idea.log` from that directory and search for lines containing `copilot` or `MCP` to find startup errors and tool-invocation activity.

---

## JetBrains AI Assistant (IntelliJ IDEA and other JetBrains IDEs)

> **Minimum IDE version**: JetBrains AI Assistant MCP client support requires **IntelliJ IDEA 2025.2** or later (and the equivalent 2025.2 release of other JetBrains IDEs). Verify your IDE version under Help → About before following these steps.

### Configuration

#### Step 1 — Open the MCP settings

Navigate to:

> **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

Alternatively, type `/` in the AI chat panel and click **Add Command**, which opens the same settings page.

#### Step 2 — Add the server

1. Click the **+** button to add a new server entry.
2. Paste the following JSON into the input dialog:

```json
{
  "mcpServers": {
    "trillium-realtime-mcp": {
      "command": "uvx",
      "args": ["trillium-realtime-mcp"],
      "env": {
          "TRILLIUM_BASE_URL": "http://your-trillium-host:8080",
          "TRILLIUM_API_KEY": "your_trillium_web_key"
      }
    }
  }
}
```

3. Set the **Server level** to **Global** (available in all projects) or **Project** (current project only).
4. Click **OK** → **Apply**. The IDE will attempt to connect to the server.

> **Credentials in the `env` block are for experimentation only.** For production use, omit the `env` block and supply the variables via OS-level environment variables or a wrapper script. See [Keeping Credentials Out of MCP Config Files](#keeping-credentials-out-of-mcp-config-files) for step-by-step instructions.

### Starting the server

JetBrains IDEs start the MCP server process automatically when AI Assistant first invokes a tool. To manually start or restart it:

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**.
2. Find the `trillium-realtime-mcp` entry. If it shows a stopped/disconnected state, click the **Start** (▶) button next to it.
3. A green status indicator confirms the server is connected and ready.
4. After any credential or config change, click **Restart** on the same settings page rather than restarting the entire IDE.

For full documentation see the [JetBrains AI Assistant — MCP Servers](https://www.jetbrains.com/help/idea/mcp-servers.html) help page.

### Log location

Help → **Show Log in Explorer** (Windows) / **Show Log in Finder** (macOS) → look for an `mcp/` subfolder.

---

## Microsoft Visual Studio

> **Minimum version**: Visual Studio 2022 version 17.14 or later (or Visual Studio 2026) with the **GitHub Copilot** extension installed. Visual Studio is Windows-only.

GitHub Copilot in Visual Studio reads MCP server configurations from `.mcp.json` files (note the leading dot).

### Config file locations

| Priority | Path | Scope |
|----------|------|-------|
| 1 | `%USERPROFILE%\.mcp.json` | User-global — applies to all solutions for the current user |
| 2 | `<SOLUTIONDIR>\.mcp.json` | Solution-level — suitable for source control |

For most setups, use `<SOLUTIONDIR>\.mcp.json` (source-controllable) or `%USERPROFILE%\.mcp.json` (user-global).

### Configuration

Create or open the config file and add:

```json
{
    "servers": {
        "trillium-realtime-mcp": {
            "type": "stdio",
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

> **macOS/Linux path**: Replace the `--from` value with `/absolute/path/to/trillium_realtime_mcp-{version}-py3-none-any.whl`.

> **Credentials in the `env` block are for experimentation only.** For production use, omit the `env` block and supply credentials via OS-level environment variables. See [Keeping Credentials Out of MCP Config Files](#keeping-credentials-out-of-mcp-config-files).

### Starting the server

After saving `.mcp.json`:

1. Restart Visual Studio (required for config changes to take effect).
2. Open the GitHub Copilot Chat panel (**View → GitHub Copilot Chat**) and switch to **Agent mode** using the mode selector in the chat input (MCP tools are only available in Agent mode).
3. Click the **Select tools and skills** button in the Copilot chat toolbar. A tools panel opens listing all registered MCP servers and their tools.
4. If `trillium-realtime-mcp` shows a stopped or disconnected state in that panel, click **Start** (or **Restart**) next to it directly from the panel to connect the server.
5. Once connected, the Trillium tools are available for use in the chat.

> **Agent mode required**: MCP tools are not available in Ask or Edit mode. Always switch to Agent mode before invoking Trillium tools.

For full documentation see [Use MCP servers in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/ide/mcp-servers).

### Log location

Check the GitHub Copilot output window: **View → Output** → select **GitHub Copilot** from the dropdown.

---

## Environment Variable Reference

The server reads these environment variables at startup. All clients must ensure the required variables are set before the MCP server process is launched.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRILLIUM_BASE_URL` | Yes | — | Base URL of the Trillium Realtime REST API. Example: `http://your-trillium-host:8080`. No trailing slash. |
| `TRILLIUM_PROJECT_DESCRIPTION` | No | `""` | Human-readable description of this server instance for multi-server disambiguation. |
| `TRILLIUM_API_KEY` | No | — | Trillium web key passed as `?webKey=` on every REST call. Required when a web access key has been configured for the Trillium Realtime service (set in the TSI Web Server Administration settings). |
| `TRILLIUM_REQUEST_TIMEOUT_SECONDS` | No | `60` | HTTP request timeout in seconds. Increase if the Trillium service is slow. |
| `TRILLIUM_CA_BUNDLE` | No | — | Path to a PEM CA certificate file (or hashed directory on Linux) used to verify TLS when `TRILLIUM_BASE_URL` is `https://`. Leave unset to use the system trust store or when using `http://`. |

### How to supply variables per client

> **Using the `env` block in a config file is convenient for experimentation, but not recommended for production.** Config files are often committed to version control or shared. For production deployments, supply credentials via OS-level environment variables or a wrapper script — see [Keeping Credentials Out of MCP Config Files](#keeping-credentials-out-of-mcp-config-files).

> **Security**: Never commit `TRILLIUM_API_KEY` (your Trillium web key) or other credentials to version control. If using a config file with an `env` block for experimentation, ensure the file is listed in `.gitignore`.

---

## Keeping Credentials Out of MCP Config Files

You may prefer to keep credentials out of config files to avoid storing sensitive values on disk or in version control. Both options below work with any MCP client in this guide.

### Option A — OS-level environment variables

Set the variables in your operating system's environment before launching the client. They are inherited by any subprocess, including the MCP server process.

**macOS/Linux** — add to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.profile`):

```bash
export TRILLIUM_BASE_URL="http://your-trillium-host:8080"
export TRILLIUM_PROJECT_DESCRIPTION="Your project description"
export TRILLIUM_API_KEY="your_trillium_web_key"
```

Reload the profile (`source ~/.zshrc`) or open a new terminal, then launch the client.

**Windows** — use either method:

*System Properties:*
1. Open **System Properties → Advanced → Environment Variables**
2. Under **User variables**, click **New** and add `TRILLIUM_BASE_URL`, `TRILLIUM_PROJECT_DESCRIPTION`, and `TRILLIUM_API_KEY`
3. Click **OK**, then restart the client application

*Command Prompt:*
```cmd
setx TRILLIUM_BASE_URL "http://your-trillium-host:8080"
setx TRILLIUM_PROJECT_DESCRIPTION "Your project description"
setx TRILLIUM_API_KEY "your_trillium_web_key"
```

> **Note**: `setx` changes apply to new processes only. Restart the client after running these commands.

> **Not suitable for multi-server deployments**: OS-level environment variables are process-wide and cannot differ between two MCP server instances running on the same machine. If you need to deploy multiple Trillium MCP servers that each link to a different Trillium project, use [Option B — Wrapper script](#option-b--wrapper-script) instead, which lets each server instance use its own values.

### Option B — Wrapper script

Create a small script that sets the environment variables and then starts the MCP server. Use the script path as the `command` in your client config (with `args: []`), instead of pointing directly to `uvx`.

> **Required for multi-server deployments**: If you need to run multiple Trillium MCP server instances on the same machine, each linking to a different Trillium project, use a separate wrapper script per instance. Each script sets its own `TRILLIUM_BASE_URL`, `TRILLIUM_API_KEY`, and `TRILLIUM_PROJECT_DESCRIPTION` values, so the client config can register them as distinct servers with independent settings.

**macOS/Linux** — create `trillium-mcp-wrapper.sh`:

```bash
#!/bin/bash
export TRILLIUM_BASE_URL="http://your-trillium-host:8080"
export TRILLIUM_PROJECT_DESCRIPTION="Your project description"
export TRILLIUM_API_KEY="your_trillium_web_key"
exec uvx --from /absolute/path/to/trillium_realtime_mcp-{version}-py3-none-any.whl trillium-realtime-mcp "$@"
```

Make it executable:
```bash
chmod +x /path/to/trillium-mcp-wrapper.sh
```

Set `command` to the absolute path of the script and `args` to `[]` in your client config:
```json
{
  "command": "/path/to/trillium-mcp-wrapper.sh",
  "args": []
}
```

**Windows** — create `trillium-mcp-wrapper.ps1`:

```powershell
$env:TRILLIUM_BASE_URL = "http://your-trillium-host:8080"
$env:TRILLIUM_PROJECT_DESCRIPTION = "Your project description"
$env:TRILLIUM_API_KEY = "your_trillium_web_key"
& uvx --from C:\absolute\path\to\trillium_realtime_mcp-{version}-py3-none-any.whl trillium-realtime-mcp @args
```

In the client config, set `command` to `powershell.exe` and `args` to `["-File", "C:\\path\\to\\trillium-mcp-wrapper.ps1"]`.

> **Security**: Do not commit wrapper scripts containing real credentials to version control. Add them to `.gitignore`.

---

## Verification

Use these steps to confirm the server is working after setup, regardless of which client you are using.

1. Open the AI chat panel in your client.
2. Switch to **Agent mode** if the client requires it (VS Code, IntelliJ / GitHub Copilot, and Visual Studio all require Agent mode to invoke MCP tools).
3. Ask the assistant to call the `ping` tool (e.g. type `ping the Trillium service`).
4. A successful response will indicate the service is healthy — the assistant may report this as plain text (e.g. "The Trillium service is healthy with a latency of 42 ms") or include the raw tool result:

   ```json
   {
     "status": "healthy",
     "service": "Trillium Realtime",
     "latency_ms": 42
   }
   ```

   Either form confirms the server is connected and working.
5. **If the call fails or returns an error**:
   - `Connection refused` or `Could not connect` → `TRILLIUM_BASE_URL` is wrong or unreachable.
   - `Timeout` → The Trillium service is reachable but slow. Increase `TRILLIUM_REQUEST_TIMEOUT_SECONDS`.
   - `Authentication failed` / `401` → `TRILLIUM_API_KEY` is missing, empty, or invalid.
   - Tools not listed at all → The server process did not start. Check client logs.

---

## Troubleshooting

### Wrong or unreachable `TRILLIUM_BASE_URL`

**Symptom**: `ping` returns "connection refused", "timeout", or "failed to connect". Other tools return service errors.

**Fix**:
- Verify the URL is reachable: `curl http://your-trillium-host:8080/TrilliumSOAP/REST/ping`
- Ensure the URL has **no trailing slash** and points to the Trillium Realtime REST base.

---

### Missing or empty web key (`TRILLIUM_API_KEY`)

**Symptom**: Tools return authentication errors, HTTP 401, or "invalid web key" messages.

**Fix**:
- Verify the variable is set and non-empty in your client config's `env` block or OS environment.
- In Claude Desktop: fully quit and relaunch after editing the config file.

---

### Server not appearing in the client's tool list

**Symptom**: The client connects but no Trillium tools appear in the available tools list.

**Fix**:
1. **Check config JSON syntax**: Paste your config block into `python -m json.tool` or an online JSON linter.
2. **Check client logs** for startup errors from the server process.
3. **Verify the server runs manually**: MCP clients suppress server stderr, so startup errors are invisible in the client. Run the server directly in a terminal to surface them. Quick smoke test:

   ```bash
   # macOS/Linux
   uvx --from /absolute/path/to/trillium_realtime_mcp-{version}-py3-none-any.whl trillium-realtime-mcp --help

   # Windows (PowerShell)
   uvx --from C:\absolute\path\to\trillium_realtime_mcp-{version}-py3-none-any.whl trillium-realtime-mcp --help
   ```

   If this fails, check that `uv` is installed and the wheel path is correct. For a full interactive debug session with environment variables set, see [Manual Installation (for Debugging)](README.dist.md#manual-installation-for-debugging) in the distribution README.
4. **Restart the client**: Some clients cache the tool list and require a full restart after adding a new server.

---

### Config change has no effect

**Cause**: Clients cache the server configuration at launch time. Saving the config file alone is not sufficient.

**Fix**:
- **VS Code**: Reload the window (`Ctrl+Shift+P` / `Cmd+Shift+P` → **Developer: Reload Window**).
- **IntelliJ / GitHub Copilot**: Restart the IDE after editing `mcp.json`.
- **JetBrains AI Assistant**: Click **Restart** on the server entry in **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**.
- **Visual Studio**: Restart Visual Studio after editing `.mcp.json`.
- **Claude Desktop**: Use File → Quit (macOS) or system tray → Quit (Windows) to fully exit, then relaunch.

---

### TLS certificate errors when using `https://`

**Symptom**: The `ping` tool fails with a certificate error such as "SSL certificate verify failed".

**Fix**:
1. Obtain your organization's CA certificate in PEM format.
2. Set `TRILLIUM_CA_BUNDLE` to the absolute path of the PEM file.
3. Verify the path is accessible to the MCP server process and the file contains a valid PEM certificate.

---

## See Also

- [README.dist.md](README.dist.md) — Installation and configuration overview
- [Model Context Protocol documentation](https://modelcontextprotocol.io/) — MCP specification and client guides
