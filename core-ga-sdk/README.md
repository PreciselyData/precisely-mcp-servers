# ga-sdk_mcp

> 📦 **Download:** [ga-sdk-mcp-server-beta.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/ga-sdk-mcp-server-beta.v1.0)

Standalone MCP server for the **GA SDK (geo-gga) V1 Java API**.

Lets you run the `Addressing.geocode()` / `verify()` V1 API and then ask GitHub Copilot
questions about the results — all in a repo that is completely separate from `geo-gga`.

---

## What's inside

| Path | Purpose |
|------|---------|
| `src/main/java/.../mcp/McpServer.java` | MCP stdio server (JSON-RPC 2.0) |
| `src/main/java/.../mcp/handler/` | MCP tools (explain, diagnose, suggest …) |
| `src/main/java/.../annotator/AnnotationDictionary.java` | Singleton YAML loader (loaded once per session) |
| `src/test/java/.../mcp/runner/GeocodeTester.java` | V1 API runner (geocode + verify) |
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

### 4. GA SDK JARs (`geo-gga` repo)

The GA SDK JARs (`geocoding-api`, `addressing-ggs`, `addressing-api`) are internal.
Install them into your local `~/.m2` **once** by running inside the `geo-gga` repo:

```powershell
cd D:\Git\geo-gga
mvn clean install -DskipTests
```

After that, this repo resolves them from local `~/.m2` — no Artifactory access required.

### 5. Reference data & resources

You need two directories on disk:

| Config key | What it points to | Example path |
|---|---|---|
| `data.path` | Country dataset folder (e.g. `ARG-EGM-TOMTOM-AR3`) | `D:\SPD\ARG-EGM-TOMTOM-AR3` |
| `resources.path` | GA SDK resources built by `geo-gga` | `D:\Git\geo-gga\ga-sdk\target\dist\resources` |

---

## Local setup (step-by-step)

### Step 1 — Clone this repository

```powershell
git clone <repo-url> D:\Git\ga-sdk_mcp
cd D:\Git\ga-sdk_mcp
```

### Step 2 — Create `config.properties`

Copy the template and fill in your local paths:

```powershell
Copy-Item config.properties.template config.properties
```

Edit `config.properties`:

```properties
# Path to the GA SDK reference data directory
data.path=D:\\SPD\\ARG-EGM-TOMTOM-AR3

# Path to the GA SDK resources directory
resources.path=D:\\Git\\geo-gga\\ga-sdk\\target\\dist\\resources
```

> `config.properties` is git-ignored — your paths are never committed.

### Step 3 — Install GA SDK JARs (if not already done)

```powershell
cd D:\Git\geo-gga
mvn clean install -DskipTests
cd D:\Git\ga-sdk_mcp
```

### Step 4 — Open the project in IntelliJ IDEA

1. **File → Open** → select `D:\Git\ga-sdk_mcp` → **Trust Project**
2. IntelliJ auto-imports the Maven project. Wait for indexing to complete.
3. Set the Project SDK to **Java 11** if prompted
   (**File → Project Structure → Project → SDK**).

### Step 5 — Build the MCP server fat JAR

From a terminal (or the IntelliJ Maven panel):

```powershell
cd D:\Git\ga-sdk_mcp
mvn clean package -DskipTests
```

Output: `target/ga-sdk-mcp.jar`

### Step 6 — Register the MCP server in IntelliJ

Edit (or create) `%LOCALAPPDATA%\github-copilot\intellij\mcp.json`:

```json
{
  "servers": {
    "ga-sdk-mcp": {
      "type": "stdio",
      "command": "java",
      "args": ["-jar", "D:\\Git\\ga-sdk_mcp\\target\\ga-sdk-mcp.jar"]
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

| Tool | Example prompt |
|------|---------------|
| `explain_geocode` | "Explain this geocode response: `{...}`" |
| `explain_verify` | "Explain this verify response: `{...}`" |
| `diagnose_request` | "Diagnose this request and response: request=`{...}` response=`{...}`" |
| `analyze_no_match` | "Why did this address return ZERO_RESULTS? `{...}`" |
| `suggest_improvements` | "How can I fix this no-match? request=`{...}` response=`{...}`" |

> After running `GeocodeTester`, you can simply ask *"Explain the last response"* —
> the response is already stored in memory, no copy-paste needed.

---

## Annotation dictionary (`code-annotations.yaml`)

All plain-English explanations added to geocode/verify responses (match types,
precision codes, score tiers, delivery indicators, etc.) live in a single YAML file —
**no Java recompile needed** to change wording or add new codes.

### Where to edit

Edit **`code-annotations.yaml`** in the working directory — the same folder from
which `java -jar ga-sdk-mcp.jar` is launched (same place as `config.properties`).

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

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `config.properties not found` | Copy `config.properties.template` → `config.properties` and fill in both paths |
| `data.path` or `resources.path` blank | Open `config.properties` and set the correct absolute paths |
| GA SDK JAR not found in `~/.m2` | Run `mvn clean install -DskipTests` inside the `geo-gga` repo |
| MCP server not showing in Copilot | Check `mcp.json` path, rebuild the JAR, and restart IntelliJ |
| Test compiles but throws at runtime | Verify that `data.path` points to a valid, readable dataset directory |
