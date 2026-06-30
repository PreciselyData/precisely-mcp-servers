
# Matching SDK MCP Server

> 📦 **Download:** [core-data-quality-matching-sdk.v1.0](https://github.com/PreciselyData/precisely-mcp-servers/releases/tag/core-data-quality-matching-sdk.v1.3.0)

## Summary

The Matching SDK MCP Server exposes data matching capabilities as tools for AI models and development environments. It provides programmatic access to the Precisely Matching SDK through a stdio-based interface, enabling configuration management, data inspection, and distributed matching job execution across local or remote Spark clusters.

## Table of Contents

- [Summary](#summary)
- [Available Tools](#available-tools)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [MCP Client Integration](#mcp-client-integration)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)


### Prerequisites

Before running the MCP server, ensure you have:

- **Java 17 or higher** installed ([Download](https://www.oracle.com/java/technologies/downloads/#java17))
    - Verify: `java -version`

- **Apache Spark 3.3+** (required only for job execution)
    - Required for the `embedded` or `submit` backends
    - Not required for the `remote` backend (jobs run on a remote cluster)
    - Verify: `spark-submit --version`
    - On Windows, local Spark execution may also require Hadoop Windows helper binaries (`winutils.exe`) and `HADOOP_HOME`

- **Writable staging directory** (required for `remote` backend)
    - Used to stage job inputs, specs, and results
    - Must be visible to both the MCP host and the Spark cluster (local path or mount)

- **Matching SDK runtime data** (required for `name_tools` only)
    - Set `MATCHING_SDK_DATA_DIR` to a directory containing the bootstrapped Precisely runtime data packs
    - For `remote` (`spark-rest`) backend, this path must be accessible from the MCP server **and** from all Spark nodes via matching volume mounts
    - Example: `export MATCHING_SDK_DATA_DIR=/data/precisely/datapacks`


## Available Tools

The MCP server exposes the following tools:

| Tool | Action | Description | Notes |
| --- | --- | --- | --- |
| `inspect` | `spark_status` | Reports Spark availability and runtime health. | Uses the configured environment variables. |
|  | `preview_data` | Inspects CSV, JSON, or Parquet files without executing matching. | Returns schema, bounded row samples, truncation flag, and diagnostics. |
|  | `workflow_guide` | Retrieves the deterministic orchestration workflow as markdown. | Intended as authoritative workflow guidance for agents. |
| `manage_config` | `discover_config_types` | Lists available configuration families. | Families: `match_key`, `match_rule`, `name_parser`, `name_variant`. |
|  | `list_algorithms` | Lists configurable dimensions for a config type with pagination support. |  |
|  | `list_samples` | Lists bundled sample configurations grounded in real authoring scenarios. |  |
|  | `validate` | Validates a configuration draft and returns structured issues with path, severity, and suggested fix. |  |
|  | `get` | Retrieves a stored configuration by file or `configId`. |  |
|  | `create_match_key` | Creates a new `match_key` configuration from raw JSON, samples, or structured intent. |  |
|  | `create_match_rule` | Creates a new `match_rule` configuration from raw JSON, samples, or structured intent. |  |
|  | `create_parser_config` | Creates a new `name_parser` configuration from raw JSON, samples, or structured intent. |  |
|  | `create_variant_config` | Creates a new `name_variant` configuration from raw JSON, samples, or structured intent. |  |
| `run_match` | `intra` | Runs intra matching with a single dataset with `match_key` and `match_rule` configurations. |  For example identifying duplicates or related entries. |
|  | `inter` | Runs inter matching and link related records across two datasets to track entity relationships. |  |
| `name_tools` | `parse_names` | Parses raw name strings into structured components. | Components include prefix, given, middle, family, and suffix. |
|  | `generate_variants` | Expands input names into candidate variant forms for matching. |  |
| `run_task` | `status` | Polls the current status of a submitted job. |  |
|  | `result` | Retrieves the result manifest once a job completes. |  |
|  | `cancel` | Requests cancellation of a running job. |  |


## Installation

### Step 1: Download the JAR

The MCP server is distributed as a single executable JAR file: `matching-sdk-mcp-1.3.0.jar`

If you plan to use the `submit` or `remote` backend, distribute the Spark runner JAR alongside it:

- `matching-sdk-mcp-1.3.0.jar` - MCP server process
- `lib/matching-sdk-mcp-spark-runner-1.3.0.jar` - Spark application JAR used by `spark-submit`

Distribution output layout is:

```text
matching-sdk-mcp.zip
  matching-sdk-mcp-1.3.0.jar
  lib/
    matching-sdk-mcp-spark-runner-1.3.0.jar
```

Choose a location to store the MCP server (examples below):

If you use the `submit` backend, copy the runner JAR too:

**Linux/macOS:**
```bash
mkdir -p ~/.local/share/mcp-servers/matching-sdk/lib
cp matching-sdk-mcp-1.3.0.jar ~/.local/share/mcp-servers/matching-sdk/
cp lib/matching-sdk-mcp-spark-runner-1.3.0.jar ~/.local/share/mcp-servers/matching-sdk/lib/
```

**Windows (PowerShell):**
```powershell
$MCPPath = "$env:APPDATA\mcp-servers"
New-Item -ItemType Directory -Force -Path "$MCPPath\lib"
Copy-Item matching-sdk-mcp-1.3.0.jar -Destination $MCPPath
Copy-Item lib\matching-sdk-mcp-spark-runner-1.3.0.jar -Destination "$MCPPath\lib"
```

## Configuration

### Backend modes

The MCP server can run matching jobs through three Spark execution paths:

- `embedded` - uses the local JVM Spark runtime
- `submit` - launches `spark-submit` from the MCP host
- `remote` - submits jobs to a Spark master through the Spark REST API on port `6066`

When `MCP_SPARK_MASTER_URL` is set, the remote backend takes precedence over embedded and submit backends.

#### Remote backend

The remote backend uses Spark master REST submissions instead of launching `spark-submit` locally.

Deployment guidance:

- The Spark master REST API port `6066` must be exposed and reachable from the MCP server
- Deploy the remote backend only within a trusted network boundary such as a VPN or DMZ
- Because Spark REST submissions on port 6066 are not authenticated by the MCP server, do not expose this endpoint to the public Internet.

The server stages inputs and submits `matching-sdk-mcp-spark-runner-1.3.0.jar` through the Spark REST API, then polls for completion and reads results from the shared staging location.

### Environment variables

- MATCHING_SDK_DATA_DIR - Path to bootstrapped Precisely runtime data packs required by `name_tools`
    - For `remote` (`spark-rest`) backend, this path must be accessible from the MCP server and all Spark nodes via matching mounts
    - Example: `/data/precisely/datapacks` on Linux/macOS or `C:\precisely\datapacks` on Windows

- SPARK_HOME - Path to Apache Spark installation
    - If set, enables Docker Spark detection

- MCP_SPARK_MASTER_URL - Enables the remote backend and identifies the Spark master
    - Format: `spark://hostname:7077`
    - The MCP server derives the REST submission endpoint as `http://hostname:6066`

- MCP_SPARK_DRIVER_MASTER_URL - Optional driver-facing Spark master URL for the remote backend
    - Use this when the REST submission endpoint and the driver runtime see the cluster under different hostnames
    - Example: host submits to `spark://localhost:7077`, but the driver inside Docker must use `spark://spark-master:7077`

- MCP_SHARED_ROOT - Host-local writable staging directory for remote execution artifacts
    - Stores staged inputs, job specs, and outputs that the MCP server can read back after completion

- MCP_SHARED_ROOT_EXECUTOR - Executor-visible path for the same shared root
    - Example: host path `C:\matching-sdk\mcp-output` mapped as `/mcp-shared` inside containers

- MCP_SPARK_RUNNER_JAR - Host-local path to `matching-sdk-mcp-spark-runner-1.3.0.jar` for the `submit` backend
    - Example: `C:\Users\you\AppData\Roaming\mcp-servers\lib\matching-sdk-mcp-spark-runner-1.3.0.jar`

- MCP_RUNNER_JAR_EXECUTOR - Executor-visible runner JAR path for remote REST execution
    - The `submit` backend will also accept this value only when the same path exists on the local host

- MCP_SPARK_DRIVER_EXTRA_JAVA_OPTIONS - Optional value passed as `--conf spark.driver.extraJavaOptions=...` for the `submit` backend

- MCP_SPARK_EXECUTOR_EXTRA_JAVA_OPTIONS - Optional value passed as `--conf spark.executor.extraJavaOptions=...` for the `submit` backend

- SPARK_DRIVER_JAVA_OPTIONS and SPARK_EXECUTOR_JAVA_OPTIONS
    - Used as fallback sources for the same submit-time Spark conf if the `MCP_` prefix variants are not set

- QUARKUS_LOG_LEVEL - Logging level (default: INFO)
    - Possible values: OFF, ERROR, WARN, INFO, DEBUG, TRACE


## Running the Server

The JAR file is a complete, self-contained executable with all dependencies embedded.

### With environment variables
```bash
export SPARK_HOME=/opt/spark
export MCP_SPARK_RUNNER_JAR="$HOME/.local/share/mcp-servers/lib/matching-sdk-mcp-spark-runner-1.3.0.jar"
export MATCHING_SDK_DATA_DIR=/data/precisely/datapacks
java -jar matching-sdk-mcp-1.3.0.jar
```

**Windows (PowerShell):**
```powershell
$env:SPARK_HOME = "C:\path\to\spark"
$env:MCP_SPARK_RUNNER_JAR = "$env:APPDATA\mcp-servers\lib\matching-sdk-mcp-spark-runner-1.3.0.jar"
$env:MATCHING_SDK_DATA_DIR = "C:\path\to\precisely\datapacks"
java -jar matching-sdk-mcp-1.3.0.jar
```

## MCP Client Integration

### Cursor or Claude/VS Code with MCP Extension

The MCP configuration file location depends on your client:

**Claude Desktop:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

**VS Code with MCP Extension:** Typically in a `.mcp` or `.mcp-servers` config directory

### Configuration Examples

**Linux/macOS Configuration (mcp.json or claude_desktop_config.json):**
```json
{
  "matching-mcp": {
    "type": "stdio",
    "command": "java",
    "args": ["-jar", "~/.local/share/mcp-servers/matching-sdk/matching-sdk-mcp-1.3.0.jar"],
    "env": {
      "SPARK_HOME": "/opt/spark",
      "MCP_SPARK_RUNNER_JAR": "~/.local/share/mcp-servers/matching-sdk/lib/matching-sdk-mcp-spark-runner-1.3.0.jar",
      "MATCHING_SDK_DATA_DIR": "/data/precisely/datapacks"
    }
  }
}
```

**Windows JSON Sample (Spark-Submit Mode):**
```json
{
  "matching-mcp": {
    "type": "stdio",
    "command": "java",
    "args": ["-jar", "%APPDATA%\\mcp-servers\\matching-sdk-mcp-1.3.0.jar"],
    "env": {
      "SPARK_HOME": "C:\\spark",
      "MCP_SPARK_RUNNER_JAR": "%APPDATA%\\mcp-servers\\lib\\matching-sdk-mcp-spark-runner-1.3.0.jar",
      "MATCHING_SDK_DATA_DIR": "C:\\path\\to\\precisely\\datapacks"
    }
  }
}
```

**Linux/macOS Configuration for remote backend:**
```json
{
  "matching-mcp": {
    "type": "stdio",
    "command": "java",
    "args": ["-jar", "~/.local/share/mcp-servers/matching-sdk/matching-sdk-mcp-1.3.0.jar"],
    "env": {
      "MCP_SPARK_MASTER_URL": "spark://localhost:7077",
      "MCP_SPARK_DRIVER_MASTER_URL": "spark://spark-master:7077",
      "MCP_SHARED_ROOT": "/absolute/path/to/mcp-output",
      "MCP_SHARED_ROOT_EXECUTOR": "/mcp-shared",
      "MCP_RUNNER_JAR_EXECUTOR": "/mcp-dist/lib/matching-sdk-mcp-spark-runner-1.3.0.jar",
      "MATCHING_SDK_DATA_DIR": "/data/precisely/datapacks"
    }
  }
}
```


**Windows Configuration for remote backend:**
```json
{
  "matching-mcp": {
    "type": "stdio",
    "command": "java",
    "args": ["-jar", "%APPDATA%\\mcp-servers\\matching-sdk-mcp-1.3.0.jar"],
    "env": {
      "MCP_SPARK_MASTER_URL": "spark://localhost:7077",
      "MCP_SPARK_DRIVER_MASTER_URL": "spark://spark-master:7077",
      "MCP_SHARED_ROOT": "C:\\Temp\\mcp-output",
      "MCP_SHARED_ROOT_EXECUTOR": "/mcp-shared",
      "MCP_RUNNER_JAR_EXECUTOR": "/mcp-dist/lib/matching-sdk-mcp-spark-runner-1.3.0.jar",
      "MATCHING_SDK_DATA_DIR": "C:\\path\\to\\precisely\\datapacks",
      "QUARKUS_LOG_LEVEL": "INFO"
    }
  }
}
```

### Example Windows Local PySpark Setup (`pip`)

If you want to run the `submit` backend on Windows without a full standalone Spark installation, you can point the MCP server at a local `pyspark` environment.

Use a Spark line that matches the SDK runtime. The current MCP modules build against Spark `3.5.x` on Scala `2.12`, so prefer `pyspark==3.5.6` or another `3.5.x` release that reports Scala `2.12`.

Example setup:

```powershell
python -m venv .venv-pyspark
.\.venv-pyspark\Scripts\python.exe -m pip install pyspark==3.5.6
```

Verify the local runtime:

```powershell
.\.venv-pyspark\Lib\site-packages\pyspark\bin\spark-submit.cmd --version
```

Expected shape:

```text
version 3.5.x
Using Scala version 2.12.x
```

Windows local Spark also requires Hadoop helper binaries. Place a compatible Hadoop `bin` directory on disk so that the following file exists:

```text
C:\tools\hadoop-3.3.6\bin\winutils.exe
```

Then configure the MCP server with explicit paths. On Windows, if you override `PATH` in the MCP server env, prefer an absolute `java.exe` path so process startup does not depend on PATH resolution.

**Windows JSON Sample (local `pyspark` submit mode):**

```json
{
  "matching-mcp": {
    "type": "stdio",
    "command": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.19.10-hotspot\\bin\\java.exe",
    "args": ["-jar", "C:\\path\\to\\matching-sdk-mcp-1.3.0.jar"],
    "env": {
      "SPARK_HOME": "C:\\path\\to\\.venv-pyspark\\Lib\\site-packages\\pyspark",
      "PYSPARK_PYTHON": "C:\\path\\to\\.venv-pyspark\\Scripts\\python.exe",
      "PYSPARK_DRIVER_PYTHON": "C:\\path\\to\\.venv-pyspark\\Scripts\\python.exe",
      "HADOOP_HOME": "C:\\tools\\hadoop-3.3.6",
      "PATH": "C:\\tools\\hadoop-3.3.6\\bin;${PATH}",
      "MATCHING_SDK_DATA_DIR": "C:\\path\\to\\precisely\\datapacks"
    }
  }
}
```

Notes:

- `SPARK_HOME` is the environment variable used by the local submit backend. `MCP_SPARK_HOME` is not sufficient on its own.
- `HADOOP_HOME` and `hadoop.home.dir` are both important on Windows. Without them, Spark may fail with `HADOOP_HOME and hadoop.home.dir are unset`.
- If `winutils.exe` is present but native access still fails, ensure the Hadoop helper binaries are compatible with the Hadoop line bundled in your `pyspark` install.


### After Configuration

1. Save the configuration file
2. Restart Claude Desktop or VS Code
3. The MCP server should appear in the available tools list
4. Test it by asking Claude to analyze data or inspect runtime status


## Docker Deployment

For containerized environments, the MCP server can be deployed alongside a local Spark cluster using Docker Compose.

### Docker Prerequisites

- Docker and Docker Compose installed

### Quick Start with Docker Compose

A pre-configured `docker-compose.yaml` is available in the source repository. It orchestrates:

- **MCP Server** - Matching SDK MCP container
- **Spark Master** - Cluster master node on port 7077 and REST API on port 6066
- **Spark Worker** - Optionally worker node for job execution
- **Shared Volume** - `mcp-output` directory for staging and results

### Configuration for Docker

The `docker-compose.yaml` automatically configures:

- `MCP_SPARK_MASTER_URL=spark://spark-master:7077` - Remote backend targeting the cluster
- `MCP_SHARED_ROOT=/mcp-shared` - Container-mounted staging directory
- `MCP_RUNNER_JAR_EXECUTOR=/mcp-dist/lib/matching-sdk-mcp-spark-runner-1.3.0.jar` - Runner JAR path inside container
- `MATCHING_SDK_DATA_DIR=/matching-sdk-data` - Container-visible Precisely runtime data packs shared with the MCP server and Spark nodes

#### docker-compose.yaml Sample

A minimal `docker-compose.yaml` for local development:

```yaml
services:
  spark-master:
    image: spark:3.5.7-scala2.12-java17-ubuntu
    container_name: spark-master
    hostname: spark-master
    ports:
      - "6066:6066"
      - "7077:7077"
      - "8081:8081"
    volumes:
      - ~/.local/share/mcp-servers/matching-sdk:/mcp-dist:ro
      - ./mcp-output:/mcp-shared
      - ./matching-sdk-data:/matching-sdk-data:ro
    environment:
      SPARK_HOME: "/opt/spark"
      SPARK_MASTER_HOST: "spark-master"
      SPARK_MASTER_PORT: "7077"
      SPARK_MASTER_WEBUI_PORT: "8081"
      SPARK_MASTER_OPTS: "-Dspark.master.rest.enabled=true -Dspark.master.rest.host=0.0.0.0 -Dspark.master.rest.port=6066"
      MATCHING_SDK_DATA_DIR: "/matching-sdk-data"
    command: /opt/spark/sbin/start-master.sh

  spark-worker:
    image: spark:3.5.7-scala2.12-java17-ubuntu
    hostname: spark-worker
    depends_on:
      - spark-master
    volumes:
      - ~/.local/share/mcp-servers/matching-sdk:/mcp-dist:ro
      - ./mcp-output:/mcp-shared
      - ./matching-sdk-data:/matching-sdk-data:ro
    environment:
      SPARK_MASTER_URL: "spark://spark-master:7077"
      MATCHING_SDK_DATA_DIR: "/matching-sdk-data"
    command: /opt/spark/sbin/start-worker.sh spark://spark-master:7077

  matching-sdk-mcp:
    image: eclipse-temurin:17-jre
    container_name: matching-sdk-mcp
    volumes:
      - ~/.local/share/mcp-servers/matching-sdk:/mcp-dist:ro
      - ./mcp-output:/mcp-shared
      - ./matching-sdk-data:/matching-sdk-data:ro
    environment:
      MCP_SPARK_MASTER_URL: "spark://spark-master:7077"
      MCP_SHARED_ROOT: "/mcp-shared"
      MCP_RUNNER_JAR_EXECUTOR: "/mcp-dist/lib/matching-sdk-mcp-spark-runner-1.3.0.jar"
      MATCHING_SDK_DATA_DIR: "/matching-sdk-data"
    command: java -jar /mcp-dist/matching-sdk-mcp-1.3.0.jar
    depends_on:
      - spark-master
      - spark-worker
```

**Setup instructions:**

1. Complete the Installation section above to extract and install the MCP server files to `~/.local/share/mcp-servers/matching-sdk/`

2. Create a `docker-compose.yaml` in your working directory (use the sample above)

3. Start services:
```bash
mkdir -p ./mcp-output  # Shared staging directory
docker-compose up -d
```

4. Verify services are running:
```bash
docker-compose ps
docker-compose logs -f matching-sdk-mcp
```

5. Access the Spark cluster:
    - **Spark Master UI:** http://localhost:8081

### Integration with MCP Clients

To connect your MCP client (Claude Desktop, VS Code) to the Docker-deployed server:

**VS Code MCP Configuration (mcp.json):**
```json
{
  "matching-sdk-mcp-docker": {
    "type": "stdio",
    "command": "docker",
    "args": [
      "compose",
      "-f",
      "/path/to/docker-compose.yaml",
      "run",
      "--rm",
      "-T",
      "matching-sdk-mcp"
    ],
    "env": {
      "MCP_SPARK_MASTER_URL": "spark://spark-master:7077",
      "MCP_SHARED_ROOT": "/mcp-shared",
      "MATCHING_SDK_DATA_DIR": "/matching-sdk-data"
    },
    "alwaysAllow": ["inspect", "manage_config"]
  }
}
```

This configuration runs the MCP server inside the Docker Compose environment on-demand, with automatic networking and volume access to the Spark cluster.



## Troubleshooting

### Server fails to start
1. Verify Java 17+ is installed: `java -version`
2. Check SPARK_HOME is correct (if using Spark features)
4. Run with verbose output: `java -jar matching-sdk-mcp-1.3.0.jar`

### Remote backend submission fails
1. Verify `MCP_SPARK_MASTER_URL` points to a reachable Spark master
2. Verify the Spark master REST API is reachable on port `6066`
3. Verify `MCP_SHARED_ROOT` is writable on the host
4. Verify `MCP_SHARED_ROOT_EXECUTOR` and `MCP_RUNNER_JAR_EXECUTOR` match the paths visible inside the Spark cluster
5. If the driver runs in a different network context, set `MCP_SPARK_DRIVER_MASTER_URL` to the hostname the driver should use to find the master

### ClassNotFoundException or missing classes
All dependencies are embedded in the JAR. If you encounter missing classes:
1. Verify you're running the complete `matching-sdk-mcp-1.3.0.jar` (check file size, ~60-100MB)
2. Check JAR integrity: `jar -tf matching-sdk-mcp-1.3.0.jar | head`
3. Ensure no partial downloads

If you use the `submit` backend:
1. Verify `matching-sdk-mcp-spark-runner-1.3.0.jar` is present and readable
2. Set `MCP_SPARK_RUNNER_JAR` to the host-local runner JAR path
3. Only use `MCP_RUNNER_JAR_EXECUTOR` for submit when that exact path also exists on the host machine

### Windows local Spark issues

If you run the `submit` backend against a local Windows `pyspark` installation:

1. **`HADOOP_HOME and hadoop.home.dir are unset`:** Configure `HADOOP_HOME`, add `%HADOOP_HOME%\\bin` to `PATH`, and pass `-Dhadoop.home.dir=...` through `MCP_SPARK_DRIVER_EXTRA_JAVA_OPTIONS` and `MCP_SPARK_EXECUTOR_EXTRA_JAVA_OPTIONS`.
2. **`UnsatisfiedLinkError: NativeIO$Windows.access0(...)`:** The loaded Hadoop helper binaries do not match the Hadoop line bundled with your `pyspark` install. Check the `hadoop-client-*` jars under `pyspark\\jars` and use a compatible `winutils.exe`/`hadoop.dll` set.
3. **`spawn java ENOENT` after editing `PATH`:** Use an absolute `command` path for `java.exe` in your MCP JSON instead of relying on PATH lookup.

### Java 17 serialization or module-access failures
If Spark jobs fail with Java 17 reflective-access or serialization issues, pass module-open flags to both driver and executor.

For the `submit` backend, the MCP server maps these environment variables to Spark submit conf:

- `MCP_SPARK_DRIVER_EXTRA_JAVA_OPTIONS` -> `spark.driver.extraJavaOptions`
- `MCP_SPARK_EXECUTOR_EXTRA_JAVA_OPTIONS` -> `spark.executor.extraJavaOptions`
- `SPARK_DRIVER_JAVA_OPTIONS` -> fallback for driver when `MCP_SPARK_DRIVER_EXTRA_JAVA_OPTIONS` is unset
- `SPARK_EXECUTOR_JAVA_OPTIONS` -> fallback for executor when `MCP_SPARK_EXECUTOR_EXTRA_JAVA_OPTIONS` is unset

Example:

```bash
export MCP_SPARK_DRIVER_EXTRA_JAVA_OPTIONS="--add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.invoke=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED"
export MCP_SPARK_EXECUTOR_EXTRA_JAVA_OPTIONS="--add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.invoke=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED"
```

These become:

```text
--conf spark.driver.extraJavaOptions=...
--conf spark.executor.extraJavaOptions=...
```

For embedded or externally managed Spark runtimes, set the equivalent Spark conf or container JVM options in the runtime that actually launches the driver and executors.

### Backend selection issues

If the wrong backend is selected or rejected:

1. **`remote` backend rejected when `SPARK_MASTER_URL` is set:** The server forbids explicit `embedded` or `submit` when `SPARK_MASTER_URL` is active. Remove `SPARK_MASTER_URL` to allow embedded/submit, or remove conflicting backend override.
2. **`embedded`/`submit` rejected with no SPARK_HOME:** Set `SPARK_HOME` to enable embedded/submit, or set `MCP_SPARK_MASTER_URL` for remote backend.
3. **Verify active backend:** Check the `inspect.spark_status` response; `sparkSource` indicates the resolved source (HOST_LOCAL, DOCKER_LOCAL, NONE for degraded).

### Configuration validation errors (`manage_config`)

If validation fails with structured issues:

1. **Missing `availableColumns`:** If column mapping fails, provide `availableColumns` in the validate request to enable per-column checks.
2. **Schema structure errors:** Ensure JSON matches expected shape (e.g., `matchKeys` array for match_key, `rules` array for match_rule). Use `list_samples` to see valid structures.
3. **Idempotency conflicts:** Reusing an `idempotencyToken` with different `draftJson` returns a conflict error. Use a unique token or omit idempotency for non-retryable operations.

### Input file issues (`preview_data`, `run_match` and `name_tools`)

1. **File not found (MCP-002):** Verify the `host_path` exists and is readable; use `preview_data` first to confirm accessibility.
2. **Permission denied:** Ensure the MCP process has read access to the dataset file.
3. **Attachment materialization failed (MCP-007):** If using `attachment` source type, verify the attachment ID is correct and material.

### Preview issues (`inspect.preview_data`)

1. **Unsupported format (MCP-003):** Only CSV, JSON, and Parquet are supported. Check `formatHint` parameter.
2. **Parquet preview requires Spark (MCP-004):** Parquet preview is Spark-gated. Ensure Spark is available or use CSV/JSON formats.
3. **Preview truncated:** If `truncated: true`, increase `maxRows` (up to 10000) or `maxBytes` (default 1MB) to capture more data.

### Common error codes

| Code | Name | Typical Cause | Retryable |
| --- | --- | --- | --- |
| MCP-001 | VALIDATION_ERROR | Invalid input schema or conflicting params | No |
| MCP-002 | FILE_NOT_FOUND | Dataset or config file not accessible | No |
| MCP-003 | UNSUPPORTED_FORMAT | CSV/JSON/Parquet expected | No |
| MCP-004 | SPARK_UNAVAILABLE | Spark required but not configured | No |
| MCP-005 | RUNTIME_DEPENDENCY_UNAVAILABLE | Transient service outage | Yes |
| MCP-006 | INPUT_TOO_LARGE | Dataset exceeds size limits | No |
| MCP-007 | ATTACHMENT_MATERIALIZATION_FAILED | Attachment upload or staging failed | No |
| MCP-999 | INTERNAL_ERROR | Unexpected server error | Yes |

### Trace IDs and diagnostics

All error responses include a `traceId` for support correlation. Logs are written to stderr; enable `QUARKUS_LOG_LEVEL=DEBUG` to capture per-action diagnostics. Include the `traceId` when reporting issues.