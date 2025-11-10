# Precisely SDK MCP Server

> **⚠️ DEPRECATED:** This project is deprecated and will no longer receive updates. Please migrate to [`dis-locate-apis-v2`](../dis-locate-apis-v2/) for the latest features and improvements.

A Model Context Protocol (MCP) server that provides access to Precisely's comprehensive Data Integrity Suite's API assistants to answer complex questions about addresses, properties, demographics, risk assessments, and spatial analysis.

## Features

- **Address Intelligence**: Geocoding, reverse geocoding, address verification and parsing
- **Property Data**: Building information, parcel details, property attributes, replacement costs
- **Risk Assessment**: Flood, wildfire, earthquake, coastal, and weather risk analysis
- **Demographics**: Crime indices, lifestyle segments, neighborhood statistics
- **Spatial Analysis**: Query data within geographic boundaries
- **Verification Services**: Email and phone number validation
- **Location Services**: IP geolocation, timezone lookup, tax jurisdiction data


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
python main.py
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


## Function Reference Guide
### Geo Addressing API

**`autocomplete`** - *Suggest addresses as you type*
- "Complete this address: 123 Main"
- "What addresses start with Empire State?"
- "Autocomplete: 1600 Penn"

**`autocomplete_postal_city`** - *Find cities by postal code*
- "What cities are in ZIP 90210?"
- "Cities for postal code 10001"
- "Find cities in 02101 area"

**`autocomplete_v2`** - *Enhanced address suggestions with details*
- "Smart complete: Apple Park Way"
- "Enhanced suggestions for Times Square"
- "V2 autocomplete for Golden Gate"

**`geocode`** - *Convert addresses to coordinates*
- "What are coordinates for White House?"
- "Get lat/lon for 123 Main St"
- "Geocode this address: Central Park"

**`lookup`** - *Find address details by ID*
- "Lookup address ID: ABC123"
- "Get details for precisely ID 456"
- "Address info for reference XYZ"

**`reverse_geocode`** - *Convert coordinates to addresses*
- "What address is at 40.7589, -73.9851?"
- "Address for GPS location 34.0522, -118.2437"
- "Reverse geocode: 41.8781, -87.6298"

**`verify_address`** - *Validate and standardize addresses*
- "Verify: 123 Main Street Boston MA"
- "Is this address valid: 456 Oak Ave?"
- "Standardize this address format"

### Address Parser API

**`parse_address`** - *Break address into components*
- "Parse: John Doe 123 Main St Boston"
- "Split this address into parts"
- "Extract components from full address"

**`parse_address_batch`** - *Parse multiple addresses together*
- "Parse my address list into components"
- "Batch parse 100 customer addresses"
- "Split multiple addresses into fields"

### Email Verification API

**`verify_email`** - *Check if email is valid*
- "Verify email: user@example.com"
- "Is this email real: test@domain.com?"
- "Check email deliverability"

**`verify_batch_emails`** - *Validate multiple emails together*
- "Verify my email list"
- "Check 500 customer emails"
- "Bulk validate email addresses"

### Emergency Info API

**`psap_address`** - *Find 911 center by address*
- "911 center for 123 Main St?"
- "Emergency dispatch for this address"
- "PSAP serving my location"

**`psap_location`** - *Find 911 center by coordinates*
- "911 center at 40.7589, -73.9851"
- "Emergency services for GPS location"
- "PSAP for coordinates 34.05, -118.24"

**`psap_ahj_address`** - *Find authority by address*
- "Emergency authority for this address"
- "AHJ serving 456 Oak Street"
- "Jurisdiction for my location"

**`psap_ahj_location`** - *Find authority by coordinates*
- "Emergency authority at coordinates"
- "AHJ for GPS 41.88, -87.63"
- "Jurisdiction for this location"

**`psap_ahj_fccid`** - *Find authority by FCC ID*
- "AHJ for FCC ID: ABC123"
- "Emergency authority for FCC XYZ"
- "Jurisdiction by FCC identifier"

### Geolocation API

**`geo_locate_ip_address`** - *Find location of IP*
- "Where is IP 192.168.1.1?"
- "Geolocate this IP address"
- "Location for IP 8.8.8.8"

**`geo_locate_wifi_access_point`** - *Find WiFi location*
- "Locate WiFi: MAC AA:BB:CC"
- "Where is this access point?"
- "WiFi geolocation by MAC address"

### Geo Tax API

**`lookup_by_address`** - *Find tax rates by address*
- "Tax rates for 123 Main St"
- "Sales tax at this address"
- "Tax jurisdiction for my business"

**`lookup_by_addresses`** - *Get tax rates for multiple addresses*
- "Tax rates for my store locations"
- "Bulk tax lookup for addresses"
- "Sales tax for address list"

**`lookup_by_location`** - *Find tax rates by coordinates*
- "Tax rates at 40.7589, -73.9851"
- "Sales tax for GPS location"
- "Tax jurisdiction for coordinates"

**`lookup_by_locations`** - *Get tax rates for multiple coordinates*
- "Tax rates for coordinate list"
- "Bulk tax lookup by GPS points"
- "Sales tax for multiple locations"

### Name Parsing API

**`parse_name`** - *Split names into components*
- "Parse: Dr. John Michael Smith Jr."
- "Split name into first/middle/last"
- "Extract title and suffix from name"

### Phone Verification API

**`validate_phone`** - *Check if phone number valid*
- "Verify phone: (555) 123-4567"
- "Is this phone number real?"
- "Validate mobile number format"

**`validate_batch_phones`** - *Validate multiple phones together*
- "Verify my phone number list"
- "Check 200 customer phone numbers"
- "Bulk validate phone database"

### Timezone API

**`timezone_addresses`** - *Find timezone by address*
- "Timezone for 123 Main St Seattle"
- "What timezone is this address in?"
- "Time zone for business location"

**`timezone_locations`** - *Find timezone by coordinates*
- "Timezone at 40.7589, -73.9851"
- "Time zone for GPS location"
- "Timezone for coordinates 34.05, -118.24"

### GraphQL API - Core Property Data

**`get_addresses_detailed`** - *Complete address information with IDs*
- "Detailed info for 123 Main St"
- "Full address data including IDs"
- "Complete address profile and metadata"

**`get_buildings_by_address`** - *Building data including type and area*
- "Building info for Empire State Building"
- "Structure details at this address"
- "Building type and square footage"

**`get_parcels_by_address`** - *Land parcel information and boundaries*
- "Parcel data for 123 Oak Street"
- "Land boundaries for this property"
- "Lot information and parcel ID"

**`get_places_nearby`** - *Local businesses and points of interest*
- "Restaurants near 123 Main St"
- "Businesses within 1 mile radius"
- "Coffee shops close to this address"

**`get_property_attributes_by_address`** - *Detailed property characteristics*
- "Property details for 456 Oak Ave"
- "Bedrooms, bathrooms, year built info"
- "Square footage and property value"

**`get_replacement_cost_by_address`** - *Insurance replacement cost estimates*
- "Replacement cost for my house"
- "Insurance rebuild estimate"
- "Property replacement value calculation"

### GraphQL API - Risk Assessment

**`get_coastal_risk`** - *Hurricane and storm surge vulnerability*
- "Hurricane risk for Miami Beach address"
- "Coastal storm threat assessment"
- "Storm surge risk for beachfront property"

**`get_property_fire_risk`** - *Fire station distances and response*
- "Fire risk for 123 Forest Lane"
- "Fire station response time"
- "Nearest fire department distance"

**`get_earth_risk`** - *Earthquake fault proximity and risk*
- "Earthquake risk for San Francisco address"
- "Fault line distance and seismic risk"
- "Earthquake hazard assessment"

**`get_wildfire_risk_by_address`** - *Wildfire probability and severity ratings*
- "Wildfire risk for Malibu property"
- "Fire danger assessment"
- "Wildfire threat level analysis"

**`get_flood_risk_by_address`** - *FEMA flood zones and elevation*
- "Flood risk for New Orleans address"
- "FEMA flood zone designation"
- "Flood insurance requirements"

**`get_historical_weather_risk`** - *Tornado, hail, severe weather history*
- "Weather risk for Kansas address"
- "Tornado and hail history"
- "Severe weather threat assessment"

### GraphQL API - Demographics & Lifestyle

**`get_crime_index_by_address`** - *Crime statistics and safety indices*
- "Crime rates for 123 Downtown Ave"
- "Safety index compared to national average"
- "Violent vs property crime statistics"

**`get_psyte_geodemographics_by_address`** - *Lifestyle and consumer segments*
- "Demographics for this neighborhood"
- "Consumer lifestyle segments nearby"
- "Household income and lifestyle data"

**`get_ground_view_by_address`** - *Detailed demographic and economic data*
- "Population demographics for this area"
- "Income, education, employment statistics"
- "Age distribution and household composition"

### GraphQL API - Neighborhood & Area

**`get_neighborhoods_by_address`** - *Walkability, home prices, area statistics*
- "Neighborhood stats for 123 Elm St"
- "Walkability and transit scores"
- "Average home values and trends"

**`get_schools_by_address`** - *School districts, attendance zones, colleges*
- "Schools serving 456 Oak Avenue"
- "School district and ratings"
- "Colleges and universities nearby"

**`get_serviceability`** - *Delivery and service accessibility*
- "Is this address serviceable?"
- "Delivery accessibility information"
- "Service availability for location"

### GraphQL API - Spatial Queries

**`get_spatial_addresses`** - *Addresses within geographic boundaries*
- "Addresses in downtown Boston polygon"
- "All addresses within coordinate boundary"
- "Properties in this geographic area"

**`get_spatial_buildings`** - *Buildings in specified areas*
- "Buildings within Central Park boundary"
- "Structures in this geographic region"
- "Buildings intersecting polygon area"

**`get_spatial_parcels`** - *Land parcels within boundaries*
- "Parcels in this neighborhood boundary"
- "Land lots within coordinate area"
- "Property parcels in polygon region"

**`get_spatial_places`** - *Businesses and POIs in regions*
- "Restaurants in downtown boundary"
- "Businesses within geographic area"
- "POIs in this coordinate region"

### GraphQL API - Relationships

**`get_parcel_by_owner_detailed`** - *Properties by owner name/ID*
- "Properties owned by John Smith"
- "All parcels for owner ID 12345"
- "Real estate holdings by owner"

**`get_address_family`** - *Related addresses and units*
- "Related addresses for apartment building"
- "Address family for 123 Main St"
- "Connected units and addresses"


### API Response Format

All API functions return structured JSON responses with:
- **metadata**: Pagination and data vintage information
- **data**: The actual response data array
- **errors**: Any validation or processing errors

Example response structure:
```json
{
  "data": {
    "getByAddress": {
      "addresses": {
        "metadata": {
          "pageNumber": 1,
          "totalPages": 1,
          "count": 1,
          "vintage": "2024-Q1"
        },
        "data": [
          {
            "preciselyID": "12345",
            "addressNumber": "123",
            "streetName": "Main St",
            "city": "Boston",
            "admin1ShortName": "MA",
            "postalCode": "02101",
            "latitude": 42.3601,
            "longitude": -71.0589
          }
        ]
      }
    }
  }
}
```

## Error Handling

The server includes comprehensive error handling for:
- Invalid API credentials
- Malformed requests
- Rate limiting
- Network connectivity issues
- Invalid addresses or coordinates

## Rate Limits

Please be aware of Precisely's API rate limits and ensure your usage complies with your subscription plan.

## Support

For API documentation and support:
- [Precisely Developer Portal and API Documentation](https://developer.precisely.com/)
- [Precisely Help Center](https://help.precisely.com/)
- [Contact Precisely Support](https://www.precisely.com/support)