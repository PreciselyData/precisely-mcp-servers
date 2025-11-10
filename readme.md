# Precisely MCP Servers

This repository contains Model Context Protocol (MCP) servers for accessing Precisely's comprehensive suite of location intelligence APIs. Choose the appropriate MCP server based on which Precisely API endpoint you're working with.

## 📁 Repository Structure

```
precisely-mcp-servers/
├── developer-hub-apis/     # For https://developer.precisely.com/apis
├── dis-locate-apis-v2/     # For https://developer.cloud.precisely.com/apis
└── dis-locate-apis/        # ⚠️ DEPRECATED - Use dis-locate-apis-v2 instead
```

## 🚀 Quick Start Guide

### For developer.precisely.com APIs

If you're using APIs from **https://developer.precisely.com/apis**, use the **`developer-hub-apis`** MCP server:

```bash
cd developer-hub-apis/
```

This server provides access to:
- Address verification and autocomplete
- Geocoding and reverse geocoding  
- Demographics and lifestyle data
- Risk assessment (flood, wildfire, earthquake)
- Property information and valuations
- Tax jurisdiction data
- And many more location intelligence services

📖 **[View developer-hub-apis documentation](./developer-hub-apis/README.md)**

### For developer.cloud.precisely.com APIs

If you're using APIs from **https://developer.cloud.precisely.com/apis**, use the **`dis-locate-apis-v2`** MCP server:

```bash
cd dis-locate-apis-v2/
```

This is the latest version for cloud-based Precisely APIs with improved functionality and performance.

📖 **[View dis-locate-apis-v2 documentation](./dis-locate-apis-v2/readme.md)**

## ⚠️ Deprecation Notice

The `dis-locate-apis` folder contains a deprecated MCP server. Please migrate to `dis-locate-apis-v2` for the latest features and improvements.

## 🔑 Authentication

Both MCP servers require Precisely API credentials. You'll need:
- API Key
- API Secret

Refer to the individual README files in each folder for specific setup instructions.

## 🆘 Support

- **API Documentation**: Visit the respective Precisely developer portals
  - [developer.precisely.com](https://developer.precisely.com/apis)
  - [developer.cloud.precisely.com](https://developer.cloud.precisely.com/apis)
- **Issues**: Report issues in this repository's GitHub Issues
- **Questions**: Check the documentation in each subfolder

## 📝 License

See individual LICENSE files in each subfolder for specific licensing information.
