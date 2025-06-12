# Precisely API MCP Server

An experimental Model Context Protocol (MCP) server that provides AI-first access to Precisely APIs for location intelligence, address verification, geocoding, demographics, and other location-based services.

## Overview

This MCP server integrates with applications that support MCP, such as Claude Desktop to provide seamless access to Precisely's comprehensive suite of location APIs. It enables natural language interactions with location data, address verification, demographic information, and much more.

This MCP server is designed to be an extension of precisely's public SDK - https://github.com/PreciselyData/PreciselyAPIsSDK-Python. Currently, this MCP tool is only available using python. For usage, it is highly recommended to use UV to manage the python environment and dependencies.

## Features

### Core Services

- **Address Services**: Autocomplete, verification, and validation
- **Geocoding**: Convert addresses to coordinates and vice versa
- **Demographics**: Population, income, and demographic data
- **Geolocation**: Location-based services and proximity searches
- **Places**: Points of interest and business location data
- **Property Information**: Real estate and property details
- **Risk Assessment**: Natural disaster and environmental risk data
- **Routing**: Turn-by-turn directions and route optimization
- **Streets**: Intersection lookup and speed limit information
- **Time Zones**: Time zone information for locations
- **Zones**: Boundary and zoning information

### Additional Services

- **Email Verification**: Validate email addresses
- **Phone Verification**: Validate phone numbers
- **Local Tax**: Tax jurisdiction information
- **Schools**: Educational institution data
- **Neighborhoods**: Community and neighborhood information
- **PSAP 911**: Emergency services data
- **Telecomm Info**: Telecommunications coverage data

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Precisely API credentials

### Setup

1. **Clone or download the project**:
   ```bash
   cd /path/to/your/workspace
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure API credentials**:
   Edit [`credentials.py`](credentials.py) with your Precisely API credentials:
   ```python
   PRECISELY_API_KEY="your_api_key_here"
   PRECISELY_API_SECRET="your_api_secret_here"
   ```

4. **Configure Claude Desktop**:
   Add the following to your Claude Desktop configuration file:
   
   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "Precisely API MCP Server": {
         "command": "/path/to/uv",
         "args": [
           "--directory",
           "/path/to/mcp_api_server/",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

5. **Restart Claude Desktop** to load the MCP server.

## Usage Examples

Once configured with Claude Desktop, you can interact with the Precisely APIs using natural language:

### Address and Geocoding
- "Verify this address: 123 Main St, Anytown, CA"
- "Find the coordinates for the Empire State Building"
- "What's the complete address for coordinates 40.7128, -74.0060?"

### Demographics
- "What are the demographics for zip code 90210?"
- "Show me population data for Boulder, Colorado"

### Places and Points of Interest
- "Find coffee shops near Times Square"
- "What restaurants are within 2 miles of Central Park?"

### Streets and Transportation
- "Find the nearest intersection to 1600 Pennsylvania Avenue"
- "What's the speed limit on Highway 101 in California?"

### Risk Assessment
- "What natural disaster risks exist for Miami, Florida?"
- "Show me flood risk data for Houston, Texas"


### Dependencies

Defined in [`pyproject.toml`](pyproject.toml):

- **com-precisely-apis** (>=18.1.1) - Official Precisely APIs SDK
- **mcp[cli]** (>=1.9.2) - Model Context Protocol framework


## Getting Precisely API Credentials

1. Visit the [Precisely Developer Portal](https://developer.precisely.com/)
2. Sign up for an account
3. Create a new application
4. Generate API credentials
5. Add them to your [`credentials.py`](credentials.py) file