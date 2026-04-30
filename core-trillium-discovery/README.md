# Beta Test VM Deployment

> 📦 **Download:** [trillium-discovery-mcp.beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/trillium-discovery-mcp.beta.v1.0)

## Purpose

This file gives the exact minimum deployment bundle for running the packaged MCP server on a separate Windows test VM.

This is the intended beta deployment path:

- build the jar on the development VM
- copy the packaged runtime bundle to the test VM
- run the MCP server on the test VM against the installed Trillium Discovery REST API

## Minimal Files To Copy

Copy only these files and folders to the test VM:

```text
tss-mcp-server-deploy\
  .env
  scripts\
    run-server-with-env.cmd
  target\
    tss-mcp-server-0.1.0-SNAPSHOT.jar
```

Notes:

- You do not need to copy source code.
- You do not need to copy Maven or the Maven wrapper for this beta deployment path.
- You do not need to copy `run-mvnw-java17.cmd` unless you plan to build on the test VM.

## Test VM Prerequisites

The test VM must also have:

- Java 17 installed, preferably at `C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot`, or `JAVA_HOME` set to a valid Java 17 install
- network reachability from the MCP server process to the Trillium Discovery REST API
- permission to bind the selected MCP server port
- trust for the Trillium HTTPS certificate chain if Trillium is using a non-public or self-signed certificate

## Important Note: Discovery SSL Certificate Update

Before starting the MCP server, update the Discovery SSL certificate file on the test VM.

Target file:

```text
C:\Program Files\Trillium Software\MBSW\18\svr\server\ssl\server.cert
```

Replace the file contents with this certificate value:

```text
-----BEGIN CERTIFICATE-----
MIIDHzCCAgegAwIBAgIUTVBW+Bqq9slpBuZt+rUgzu0psXEwDQYJKoZIhvcNAQEL
BQAwFDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTI2MDQyMjE2NTE1NloXDTI4MDcy
NTE2NTE1NlowFDESMBAGA1UEAwwJbG9jYWxob3N0MIIBIjANBgkqhkiG9w0BAQEF
AAOCAQ8AMIIBCgKCAQEAwku7Ll7rhMToCRfTGeUBTTIaJwHz1miMVp3oX9/fbXL+
E+BkO+7c1QV+Qmlmy1IDvBtHNN3KjXhgYyDGQINvYYZPixyjgaVxwC3hfIUZTSi8
10ObI3HoVXsKGrTQVewlmtOhdRaFFwlx+PsgIuWugS/NKXmLSVcGns/6hUxZeykq
uLZ+lZug05diNDwtxQx+MX6kQ68dsqoT7h9nxrOoGW6A/O2mbzh33V3cZh0zh7xC
D9uNFaoH7r8xtYdBPl1Y83luRW7EvgFFXoKHb4HvxtoCfqZJTdb5WDkuRRlFcfiN
MPE/iWx6TNmJipztFzzkg0SE+yGP6CO4g7/R7xm+bwIDAQABo2kwZzAdBgNVHQ4E
FgQUPvmLw6oF3vopP36iRJI3pmr/M8wwHwYDVR0jBBgwFoAUPvmLw6oF3vopP36i
RJI3pmr/M8wwDwYDVR0TAQH/BAUwAwEB/zAUBgNVHREEDTALgglsb2NhbGhvc3Qw
DQYJKoZIhvcNAQELBQADggEBADidN/vLKEmMOSmzrJRHa5mhY7gqPDzhmHysxDaH
2zFrKbNUvW4WUXPLKuqh5UUu6Dpdg+H7YxOqZoKqCE8pfaukp5fAVef1YJQOoiyI
HVad/oLFBIsbLH5NKw3U2g1csG5X0+BZx5Ii4SQ2AKiHrbc3EYmvJTrM5/lYY4At
C/9lXKZwGZ9Dc5pQSYUwMhUFVjJutp72/riWxK88FHJ0cvai3+6FbBLklWCg60qe
9+XEaRcNDIVFqr8INGvAggOYEcOf3Jiu7TQuOUOGvk4CqrvIsgP639c6G3S9mS94
YU7Aa9f5XDZ3uZDnNHO81GgdMd3Hy7f3ovOTFZLqOhBcrbw=
-----END CERTIFICATE-----
```

Do this certificate replacement before launching the MCP server.

> ***After replacing the Discovery SSL certificate, you will need to restart the Trillium Scheduler service.***

## Exact .env Contents

Create `.env` in the deployment root with these contents and replace the placeholder values.

Important:

- `TRILLIUM_BASE_URL` should be the host root, not the `/api` path
- because the MCP server already appends `/api/repositories/...`, use `https://localhost:49713`, not `https://localhost:49713/api`

```text
TRILLIUM_USERNAME=replace-with-beta-service-username
TRILLIUM_PASSWORD=replace-with-beta-service-password
TRILLIUM_BASE_URL=https://localhost:49713
SERVER_PORT=8080
TRILLIUM_TRANSPORT=sse

MCP_IDENTITY_MODE=api-key-map
MCP_BETA_API_KEY=replace-with-a-long-random-beta-api-key
MCP_BETA_PRINCIPAL=support-beta
MCP_BETA_DISPLAY_NAME=Support Beta
MCP_BETA_GROUPS=support
```

Guidance for the inbound beta auth values:

- `MCP_IDENTITY_MODE` must be `api-key-map` for the supported beta path
- `MCP_BETA_API_KEY` should be a strong shared secret, not a guessable label
- `MCP_BETA_PRINCIPAL` should be a stable machine-readable identity name
- `MCP_BETA_DISPLAY_NAME` should be a human-readable label
- `MCP_BETA_GROUPS` should be one or more comma-separated logical groups

Example stronger API key shape:

```text
MCP_BETA_API_KEY=2fe8f8a3b9014a7f8f4c9c5e0a2d6b11supportbeta
```

## Copy-Paste Startup Checklist

Use this checklist when standing up the latest packaged MCP server on a Windows test VM with the full currently available tool surface.

### 1. Put the deployment bundle in place

Expected layout:

```text
C:\tss-mcp-server-deploy\
  .env
  scripts\
    run-server-with-env.cmd
  target\
    tss-mcp-server-0.1.0-SNAPSHOT.jar
```

### 2. Fill in `.env`

Copy this template and replace the placeholder values:

```text
TRILLIUM_USERNAME=replace-with-beta-service-username
TRILLIUM_PASSWORD=replace-with-beta-service-password
TRILLIUM_BASE_URL=https://replace-with-real-trillium-host
SERVER_PORT=8080
TRILLIUM_TRANSPORT=sse

MCP_IDENTITY_MODE=api-key-map
MCP_BETA_API_KEY=replace-with-a-long-random-beta-api-key
MCP_BETA_PRINCIPAL=support-demo
MCP_BETA_DISPLAY_NAME=Support Demo
MCP_BETA_GROUPS=support
```

Notes:

- `TRILLIUM_BASE_URL` must be the host root, not an `/api` URL.
- `MCP_BETA_API_KEY` should be a strong random shared secret.
- `TRILLIUM_TRANSPORT=sse` is the expected setting for HTTP validation from the test VM.

### 3. Update the Discovery SSL certificate

Before starting the MCP server, replace the contents of this file:

```text
C:\Program Files\Trillium Software\MBSW\18\svr\server\ssl\server.cert
```

with the certificate value shown in [Important Note: Discovery SSL Certificate Update](#important-note-discovery-ssl-certificate-update).

After updating `server.cert`, also import the same certificate into the Java 17 truststore used by the MCP server. This is required so the Java HTTP client trusts the Discovery HTTPS endpoint.

Important:

- Import the certificate into the same Java 17 installation that `run-server-with-env.cmd` will use.
- If `JAVA_HOME` is set before launch, use that JDK's truststore instead of the default path below.

Save the certificate to a file, for example:

```text
C:\tss-mcp-server-deploy\discovery-localhost.crt
```

Default Java 17 truststore path:

```text
C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot\lib\security\cacerts
```

Import command:

```text
"C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot\bin\keytool.exe" -importcert -alias discovery-localhost-20260422 -file "C:\tss-mcp-server-deploy\discovery-localhost.crt" -keystore "C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot\lib\security\cacerts" -storepass changeit -noprompt
```

Verification command:

```text
"C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot\bin\keytool.exe" -list -alias discovery-localhost-20260422 -keystore "C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot\lib\security\cacerts" -storepass changeit
```

If `JAVA_HOME` points to a different Java 17 install, replace both the `keytool.exe` path and the `cacerts` path with the ones under that JDK.

### 4. Start the server in `cmd.exe`

If Java 17 is installed at the default script location, run:

```text
cd /d C:\tss-mcp-server-deploy
scripts\run-server-with-env.cmd .env
```

If Java 17 is installed somewhere else, run:

```text
cd /d C:\tss-mcp-server-deploy
set JAVA_HOME=C:\Path\To\Your\Java17
scripts\run-server-with-env.cmd .env
```

### 5. Confirm the expected startup result

With `SERVER_PORT=8080`, the MCP server should listen on:

```text
http://localhost:8080
```

Beta callers authenticate with:

```text
Authorization: Bearer <MCP_BETA_API_KEY>
```

The server should log the registered tool list at startup. The current tool set is:

```text
get_business_rule
get_business_rule_job_status
get_entity
get_entity_row_details
get_entity_rows
get_repository
list_business_rules
list_entities
list_entity_rows
list_repositories
run_business_rule
```

### 6. If using VS Code stdio, add repository startup args

If you want VS Code to start the MCP server directly, add a server entry like this to `mcp.json` and adjust the paths and repository names for the test VM:

```json
{
  "servers": {
    "trillium-mcp": {
      "type": "stdio",
      "command": "cmd.exe",
      "args": [
        "/c",
        "C:\\tss-mcp-server-deploy\\scripts\\run-server-with-env.cmd",
        "C:\\tss-mcp-server-deploy\\.env",
        "--server.port=0",
        "--trillium.transport=stdio",

        "--trillium.repositories.germany.principal=system",
        "--trillium.repositories.germany.permissions[0]=repositories:read",
        "--trillium.repositories.germany.permissions[1]=entities:read",
        "--trillium.repositories.germany.permissions[2]=business-rules:read",
        "--trillium.repositories.germany.permissions[3]=business-rules:execute",

        "--trillium.repositories.france.principal=system",
        "--trillium.repositories.france.permissions[0]=repositories:read",
        "--trillium.repositories.france.permissions[1]=entities:read",
        "--trillium.repositories.france.permissions[2]=business-rules:read",
        "--trillium.repositories.france.permissions[3]=business-rules:execute"
      ]
    }
  }
}
```

VS Code notes:

- Use `--trillium.transport=stdio` in the `args` list because VS Code MCP launches the server over stdio, not SSE.
- Keep the `.env` path absolute so VS Code can start the server reliably from any workspace.
- Replace `germany` and `france` with the exact repository names returned by Trillium.
- Add one repository block per repository you want to use through VS Code.
- The `.env` file can still keep `TRILLIUM_TRANSPORT=sse` for HTTP validation; the command-line `--trillium.transport=stdio` override takes precedence for the VS Code launch.

Use one block like this for each allowed repository name:

```json
"--trillium.repositories.REPOSITORY_NAME.principal=system",
"--trillium.repositories.REPOSITORY_NAME.permissions[0]=repositories:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[1]=entities:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[2]=business-rules:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[3]=business-rules:execute",
```

That single block covers:

- `list_repositories`
- `get_repository`
- `list_entities`
- `get_entity`
- `list_entity_rows`
- `get_entity_rows`
- `get_entity_row_details`
- `list_business_rules`
- `get_business_rule`
- `run_business_rule`
- `get_business_rule_job_status`

Notes:

- `list_repositories` can be called first to discover names.
- Any protected repository-scoped follow-on tool still requires the repository to be configured at startup.
- `get_entity_rows` is a compatibility alias for `list_entity_rows`.

### 7. Working with Claude Desktop

The Beta MCP Server for Trillium Discovery will **NOT** work with Claude Desktop at this time. We are working to enable this integration as soon as possible.

### 8. Run a minimal validation sequence

After startup, validate in this order:

1. `list_repositories`
2. `get_repository`
3. `list_entities`
4. `list_entities` again with `options.where`, using a concrete filter such as `Rows > 0`, and confirm only matching entities are returned
5. `get_entity`
6. `list_entity_rows` or `get_entity_rows`
7. `list_entity_rows` or `get_entity_rows` again with `options.where`, using a real humanized column name from the selected entity, and confirm only matching rows are returned
8. `get_entity_row_details`
9. `list_business_rules`
10. `get_business_rule`
11. `run_business_rule`
12. `get_business_rule_job_status`

Use the request examples in [beta-request-examples.md](./beta-request-examples.md) for direct HTTP validation.

Filtered validation notes:

- For entity filtering, `Rows > 0` is a safe first real-environment example because `Rows` is a documented entity-list humanized field.
- For row filtering, replace the sample `Score >= 90` expression with a real humanized column name from the chosen entity if that column is not present.

## Exact Startup Command

Assuming you copied the bundle into:

```text
C:\tss-mcp-server-deploy
```

Run these commands in `cmd.exe` on the test VM:

```text
cd /d C:\tss-mcp-server-deploy
scripts\run-server-with-env.cmd .env
```

That command will:

- load variables from `.env`
- find `target\tss-mcp-server-0.1.0-SNAPSHOT.jar`
- start the Spring Boot MCP server

If Java 17 is not installed at the default path used by the script, set `JAVA_HOME` first in the same `cmd.exe` session:

```text
set JAVA_HOME=C:\Path\To\Your\Java17
scripts\run-server-with-env.cmd .env
```

## What To Expect After Startup

With `SERVER_PORT=8080`, the MCP server should listen on:

```text
http://localhost:8080
```

For the beta path:

- callers authenticate to the MCP server with `Authorization: Bearer <MCP_BETA_API_KEY>`
- the MCP server maps that key to the configured beta identity
- the first protected business-rules request causes the MCP server to log into Trillium with `TRILLIUM_USERNAME` and `TRILLIUM_PASSWORD`

## VS Code mcp.json Repository Entries

If the test VM is being used through a VS Code MCP stdio client, add one repository block per repository in the `args` array of the `mcp.json` server entry.

Business-rules-only repository block:

```json
"--trillium.repositories.REPOSITORY_NAME.principal=system",
"--trillium.repositories.REPOSITORY_NAME.permissions[0]=business-rules:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[1]=business-rules:execute",
```

Combined repository, entity, and business-rule block:

```json
"--trillium.repositories.REPOSITORY_NAME.principal=system",
"--trillium.repositories.REPOSITORY_NAME.permissions[0]=repositories:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[1]=entities:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[2]=business-rules:read",
"--trillium.repositories.REPOSITORY_NAME.permissions[3]=business-rules:execute",
```

Notes:

- Replace `REPOSITORY_NAME` with the exact repository name returned by Trillium.
- `list_repositories` can be used first to discover names.
- The same combined block also covers the repository/entity row tools added later, including `list_entity_rows`, `get_entity_rows`, and `get_entity_row_details`.
- Any protected repository-scoped follow-on request still requires that repository to already be present in `mcp.json` when the server starts.

## First Operator Validation Step

After startup, use the examples in [beta-request-examples.md](./beta-request-examples.md) to validate the server.

When the repository/entity slice is in scope, do not stop at paging-only checks. Explicitly run:

- the filtered `list_entities` example using `options.where`
- the filtered `list_entity_rows` or `get_entity_rows` example using `options.where`

and confirm the returned item sets are narrower than the unfiltered calls while preserving authoritative Trillium metadata.

Normal beta users should still use the AI agent rather than calling the MCP server directly.