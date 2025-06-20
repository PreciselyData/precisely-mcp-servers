# Precisely Python SDK

This SDK provides Python client wrappers for Precisely APIs, fully production ready. This will work for https://developer.cloud.precisely.com/

---

## ✅ Supported APIs

- Geo Addressing
- Address Parser
- Email Verification
- Emergency Info (PSAP / AHJ)
- Geolocation (IP, WiFi)
- GeoTAX
- Name Parsing
- Phone Verification
- TimeZone

---

## ✅ Installation

Clone or extract this SDK package locally and run:

```bash
pip install -r requirements.txt .
```

### requirements.txt
```
fastmcp
requests
python-dotenv
```

---

## ✅ Authentication

You will need your Precisely `api_key` and `api_secret`.

Example initialization:

```python
from precisely_sdk import ApiClient

client = ApiClient(
    base_url="https://api.cloud.precisely.com",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)
```

---

## ✅ Running the Main Server

To start the MCP server (for Claude or other LLMs):

```bash
python precisely_sdk/main.py
```

This will launch the MCP server using FastMCP. Make sure your `.env` file is set up with your API credentials.

---

## ✅ Claude Desktop Integration (MCP Config Example)

To use this SDK as a Claude tool, add the following to your Claude Desktop config:

```json
{
  "name": "Precisely API MCP Server",
  "command": "python",
  "args": ["main.py"],

  "transport": "stdio"
}
```

- Make sure the path to `main.py` is correct relative to your Claude Desktop config.
- The server will expose all supported Precisely API tools to Claude.

---

## ✅ Environment Variables

Create a `.env` file in the root directory with:

```
API_KEY=your_api_key
API_SECRET=your_api_secret
BASE_URL=https://api.cloud.precisely.com
```

---
