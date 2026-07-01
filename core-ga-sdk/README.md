# ga-sdk_mcp

> 📦 **Download:** [ga-sdk-mcp-server.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/ga-sdk-mcp-server.v1.0)


Standalone MCP server for the **GA SDK (geo-gga) V1 Java API**.

Lets you run the `Addressing.geocode()` / `verify()` / `lookup()` / `predict()` V1 APIs and then ask GitHub Copilot
questions about the results — all in a repo that is completely separate from `geo-gga`.

---

## What's inside

| Path | Purpose |
|------|---------|
| `src/main/java/.../mcp/McpServer.java` | MCP stdio server (JSON-RPC 2.0) — exposes the three tools below |
| `src/main/java/.../mcp/handler/suggest/` | `suggestAPI` tool — response annotation, diagnostics, NO_MATCH analysis |
| `src/main/java/.../mcp/handler/tester/` | `generateTester` tool — injects `@Test` methods and runs Maven internally |
| `src/main/java/.../mcp/handler/preferences/` | `managePreferences` tool — validates and applies custom SDK preferences |
| `src/main/java/.../mcp/handler/annotator/` | `AnnotationDictionary` — YAML-driven code descriptions (loaded once per session) |
| `src/main/java/.../mcp/ResponseStore.java` | In-memory store for the last response pushed by the tester |
| `src/main/java/.../mcp/ResponseIpcReceiver.java` | TCP loopback listener (`127.0.0.1:19877`) that receives responses from the tester |
| `src/main/java/.../mcp/PreferenceStateStore.java` | In-memory store for active custom preferences, last API type, and last country |
| `src/test/java/.../mcp/runner/GeocodeTester.java` | V1 API runner (geocode, verify, lookup, predict) |
| `config.properties` | Your local data/resources paths (**git-ignored**) |
| `config.properties.template` | Template — copy and fill in |
| `code-annotations.yaml` | **Human-editable** domain-code descriptions |

---

## Prerequisites

### 1. Java 11+

Verify with:
```powershell
java -version
```
Install from [Adoptium](https://adoptium.net/) if not present.

### 2. Apache Maven 3.8+

Verify with:
```powershell
mvn -version
```
Install from [maven.apache.org](https://maven.apache.org/download.cgi) if not present.
Make sure `mvn` is on your `PATH`.

### 3. IntelliJ IDEA (recommended)

Any edition works (Community or Ultimate).
Download from [jetbrains.com/idea](https://www.jetbrains.com/idea/download/).

### 4. GA SDK Distribution

Download and extract the GA SDK distribution to a local folder (e.g., `D:\geo_addressing_sdk\latest`).

The SDK distribution contains everything needed:

```
geo_addressing_sdk/latest/
├── resources/              ← Point resources.path here
│   ├── bin/                # Native libraries (DLLs for Windows)
│   ├── config/             # Configuration files (addressing.yaml, etc.)
│   ├── lib/                # Runtime support JARs
│   ├── addressing-api-11.2.690-jdk11.jar
│   ├── addressing-ggs-11.2.690-jdk11.jar
│   ├── geocoding-api-11.2.690-jdk11.jar
│   └── ... (other JARs)
├── sdk/
│   └── repository/         ← Maven repository for compile-time dependencies
│       └── com/precisely/addressing/
│           ├── addressing-api/11.2.690-jdk11/
│           ├── geocoding-api/11.2.690-jdk11/
│           └── ...
└── ...
```

> **Note:** If you don't have the SDK distribution, contact your team lead or
> download it from the internal distribution server.

### 5. Reference data & resources

You need two directories on disk:

| Config key | What it points to | Example path |
|---|---|---|
| `data.path` | Country dataset folder (EGM format) | `D:\SPD\USA-EGM-TOMTOM-STREET-EN-KGD` |
| `resources.path` | GA SDK resources from the distribution | `D:\geo_addressing_sdk\latest\resources` |

---

## Local setup (step-by-step)

### Step 1 — Clone this repository

```powershell
git clone <repo-url> D:\Git\gasdk-mcp
cd D:\Git\gasdk-mcp
```

### Step 2 — Create `config.properties`

Copy the template and fill in your local paths:

```powershell
Copy-Item config.properties.template config.properties
```

Edit `config.properties`:

```properties
# Path to the GA SDK reference data directory (country dataset)
data.path=D:\\SPD\\USA-EGM-TOMTOM-STREET-EN-KGD

# Path to the GA SDK resources directory (from SDK distribution)
resources.path=D:\\geo_addressing_sdk\\latest\\resources
```

> `config.properties` is git-ignored — your paths are never committed.

### Step 3 — Configure SDK repository path (if needed)

The `pom.xml` is pre-configured to use the SDK at `D:\geo_addressing_sdk\latest`.

**If your SDK is in a different location**, update the repository URL in `pom.xml`:

```xml
<repository>
  <id>local-sdk</id>
  <name>Local GA SDK Repository</name>
  <url>file:///YOUR/SDK/PATH/sdk/repository</url>
  <releases><enabled>true</enabled></releases>
  <snapshots><enabled>false</enabled></snapshots>
</repository>
```

**If using a different SDK version**, also update the version property:

```xml
<ggs.version>11.2.690-jdk11</ggs.version>  <!-- Change to match your SDK version -->
```

### Step 4 — Open the project in IntelliJ IDEA

1. **File → Open** → select `D:\Git\gasdk-mcp` → **Trust Project**
2. IntelliJ auto-imports the Maven project. Wait for indexing to complete.
3. Set the Project SDK to **Java 11** if prompted
   (**File → Project Structure → Project → SDK**).

### Step 5 — Build the MCP server fat JAR

From a terminal (or the IntelliJ Maven panel):

```powershell
cd D:\Git\gasdk-mcp
mvn clean package -DskipTests
```

Output: `target/gasdk-mcp.jar`

### Step 6 — Register the MCP server in IntelliJ

Edit (or create) `%LOCALAPPDATA%\github-copilot\intellij\mcp.json`:

```json
{
  "servers": {
    "ga-sdk-mcp": {
      "type": "stdio",
      "command": "java",
      "args": ["-jar", "D:\\Git\\gasdk-mcp\\target\\gasdk-mcp.jar"]
    }
  }
}
```

**Restart IntelliJ** after saving.

---

## Running the geocoder tester

### From IntelliJ

Right-click `GeocodeTester.java` → **Run 'GeocodeTester.integration'**
or **Run 'GeocodeTester.verifyIntegration'**

### From Maven (terminal)

```powershell
# Run the geocode test
mvn test -Dtest=GeocodeTester#integration

# Run the verify test
mvn test -Dtest=GeocodeTester#verifyIntegration

# Run both
mvn test -Dtest=GeocodeTester
```

Both tests push the full API response directly to the running MCP server over a TCP
loopback socket (`127.0.0.1:19877`) and store it in memory — no file is written to disk.

> **Note:** The MCP server must be running before you run the tester for the response
> to be stored. If MCP is not running, a warning is logged and the test still passes.
> Simply start the MCP server and re-run the tester.

### Changing the test address

Open `GeocodeTester.java` and edit the address fields and country near the top of
`integration()` / `verifyIntegration()`. No other files need changing.

---

## MCP tools available in Copilot Chat

The MCP server exposes **three tools**. Each tool is invoked automatically by Copilot
Chat when you phrase your request naturally — you never call them by name.

---

### `suggestAPI` — Unified response analysis

Accepts the most recent response (or an explicit response + request pair) and returns:

- **Plain-English interpretation** of every field — match type, precision code, score tier,
  delivery indicator, location code, status, etc.
- **Root-cause analysis** for `ZERO_RESULTS` / `NO_MATCH` results.
- **Actionable improvement suggestions** — alternative match modes, preferences to try,
  input-format tips — without automatically applying any change.

All arguments are optional. When called with no arguments the tool reads the last response
stored in MCP memory by the tester — no copy-paste required.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `response` | object | No | A `Response` / `PredictionResponse` JSON object from any V1 API call. Omit to use the last stored response. |
| `request` | object | No | The original `RequestAddress` JSON sent to the API. Providing it enables deeper diagnostics and more targeted suggestions. |

**Example prompts**

```
"Explain the last response."
"Why did this address return ZERO_RESULTS?"
"What does precision code S4 mean?"
"How can I improve the match quality for this result?"
"Diagnose this request and response: request={...} response={...}"
```

> This is the **read-only** tool — it never modifies `GeocodeTester.java`, never re-runs
> Maven, and never applies any preference. Use it for all questions about an existing result.

---

### `generateTester` — Inject and run a V1 API test

Injects a new `@Test` method into `GeocodeTester.java` for the requested API type, then
immediately runs it via Maven internally. No terminal command is needed — the test executes
inside the tool call and the annotated response JSON is returned directly to Copilot Chat.

**Behaviour**

- If the target method **already exists**, its body is preserved (your custom address is kept)
  and only the active-preferences block is refreshed before the run.
- If the target method **does not exist**, a default scaffold is injected with a sample address.
- After the test passes, the response is pushed to MCP memory over the IPC socket and
  the annotated JSON is embedded in the tool result — no further steps required.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `apiType` | string | **Yes** | API to test. One of: `verify` \| `geocode` \| `predict` \| `autocomplete` \| `lookup` |
| `lookupType` | string | No | Key type for `lookup` only. One of: `PB_KEY` \| `GNAF_PID` \| `EIR_CODE` \| `UPRN` \| `UDPRN` \| `GERS_ID`. Defaults to `PB_KEY`. |

**Supported API types**

| `apiType` | Method injected | SDK call |
|-----------|-----------------|----------|
| `verify` | `verifyIntegration()` | `addressing.verify()` |
| `geocode` | `integration()` | `addressing.geocode()` |
| `predict` / `autocomplete` | `predictIntegration()` | `addressing.predict()` *(stub)* |
| `lookup` | `lookup<KeyType>()` e.g. `lookupPbKey()` | `addressing.lookup()` |

**Example prompts**

```
"Run a verify test."
"Run a geocode test."
"Generate a lookup tester using a GNAF PID."
"Re-run the last test."
"Test the verify API for this address."
```

> **Important:** Only call this tool when you explicitly want to run or re-run a test.
> Never use it just to analyse an existing response — use `suggestAPI` instead.

---

### `managePreferences` — Manage custom SDK preferences

Validates and applies custom preferences to `GeocodeTester.java`'s `buildPreferences()`
method. After any change the last-used API is automatically re-run so you can see the effect
immediately.

**Behaviour by action**

| Action | What it does |
|--------|-------------|
| `list` | Shows the full preference catalog (keys, allowed values, applicable APIs and countries) plus all currently active preferences. |
| `add` | Validates the key and value against the catalog and GA SDK JARs, checks that the preference applies to the current API and country, then injects it into `GeocodeTester.java` and re-runs the test. |
| `remove` | Removes all active preferences whose key or description contains the given phrase (case-insensitive substring match), then re-runs the test. If no match is active, reports the mismatch without re-running. |

**Validation rules (for `add`)**

1. A test must have been run first via `generateTester` so the API type and country are known.
2. The value must be in the preference's `allowedValues` list (where applicable).
3. The preference must be applicable for the current API type.
4. Country-specific preferences are blocked if the active country does not match.
5. Keys not found in the catalog are cross-checked against the GA SDK JARs on the classpath.
   If not found there either, the key is rejected.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | **Yes** | `list` \| `add` \| `remove` |
| `preferenceKey` | string | `add`/`remove` | Exact key for `add` (e.g. `ADDRESS_CASING`). Exact key or natural-language phrase for `remove` (e.g. `"address casing"`). |
| `preferenceValue` | string | `add` only | Value to apply (e.g. `LOWER`, `true`, `false`). |

**Example prompts**

```
"List all available preferences."
"What preferences are currently active?"
"Add preference ADDRESS_CASING = LOWER."
"Set FIND_DPV to true."
"Remove the address casing preference."
"Remove ADDRESS_CASING."
```

> Active preferences persist for the lifetime of the MCP server session. They are cleared
> automatically when the server shuts down.

---

## Annotation dictionary (`code-annotations.yaml`)

All plain-English explanations added to geocode/verify responses (match types,
precision codes, score tiers, delivery indicators, etc.) live in a single YAML file —
**no Java recompile needed** to change wording or add new codes.

### Where to edit

Edit **`code-annotations.yaml`** in the working directory — the same folder from
which `java -jar gasdk-mcp.jar` is launched (same place as `config.properties`).

### When do changes take effect?

The dictionary is loaded **once when the MCP server starts**. Edit the file, then
restart the server — changes are picked up immediately, no rebuild required.

### What happens if a key is missing?

If a code value is not listed in the YAML the raw code is forwarded to the LLM
unchanged. The LLM handles it exactly as it did before the dictionary existed —
so adding new codes is purely additive and never breaks anything.

### YAML structure at a glance

```yaml
matchCode:
  simpleFields:   { P: "placeName", S: "street", … }
  extendedFields: { D: "house-number directional", … }
  qualityLabels:  { "4": "EXACT", "0": "NOT MATCHED", … }

matchType:
  topLevel:        { ADDRESS: "…", STREET: "…", … }
  fieldDescriptors: { EXACT: "…", PARTIAL: "…", … }

precisionCode:
  classes:  { S8: "Point Address — rooftop …", … }
  suffixes: { H: "House number interpolated …", … }

scoreTier:
  tiers:
    - { label: "HIGH", min: 95, max: 100, description: "…" }
    - …

deliveryIndicator: { "1": "DELIVERABLE …", "3": "NON-DELIVERABLE …", … }
locationCodeBits:  { 1: "point-level geocode …", 256: "rooftop coordinate …", … }
status:            { OK: "…", ZERO_RESULTS: "…", ERROR: "…" }
locationType:      { ADDRESS_POINT: "…", STREET_CENTROID: "…", … }
```

---

## SDK Version Compatibility

This project is configured for GA SDK version `11.2.690-jdk11`. If you're using a different SDK version:

1. Update `<ggs.version>` in `pom.xml`
2. Ensure the `local-sdk` repository URL in `pom.xml` points to your SDK's `sdk/repository` folder
3. Verify `resources.path` in `config.properties` points to your SDK's `resources` folder

The SDK version can be found in the JAR filenames (e.g., `addressing-api-11.2.690-jdk11.jar`).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `config.properties not found` | Copy `config.properties.template` → `config.properties` and fill in both paths |
| `data.path` or `resources.path` blank | Open `config.properties` and set the correct absolute paths |
| GA SDK JAR not found | Verify the `local-sdk` repository URL in `pom.xml` points to your SDK's `sdk/repository` folder |
| `serialVersionUID` mismatch | Ensure `<ggs.version>` in `pom.xml` matches your SDK version (e.g., `11.2.690-jdk11`) |
| `No address factories available` | Verify `resources.path` points to the SDK's `resources` folder (must contain factory JARs) |
| MCP server not showing in Copilot | Check `mcp.json` path (`gasdk-mcp.jar`), rebuild the JAR, and restart IntelliJ |
| Test compiles but throws at runtime | Verify that `data.path` points to a valid, readable dataset directory |
| `generateTester` returns "no IPC response" | Ensure the MCP server is running before the test is triggered |
| Preferences not applying | Run a test via `generateTester` first so the API type and country are known |