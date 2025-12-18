# Setup Precisely MCP Server for Claude Desktop
Write-Host "Setting up Precisely MCP Server for Claude Desktop..." -ForegroundColor Green

# Get credentials from .env file
$envPath = Join-Path $PSScriptRoot "..\.env"
$API_KEY = ""
$API_SECRET = ""

if (Test-Path $envPath) {
    Write-Host "Found .env file" -ForegroundColor Green
    Get-Content $envPath | ForEach-Object {
        if ($_ -match '^\s*PRECISELY_API_KEY\s*=\s*(.*)$') {
            $API_KEY = $matches[1].Trim().Trim('"')
        }
        if ($_ -match '^\s*PRECISELY_API_SECRET\s*=\s*(.*)$') {
            $API_SECRET = $matches[1].Trim().Trim('"')
        }
    }
}

if (-not $API_KEY -or -not $API_SECRET) {
    Write-Host "ERROR: Could not find API credentials in .env file" -ForegroundColor Red
    exit 1
}

# Set paths
$serverPath = Join-Path $PSScriptRoot "precisely_wrapper_server.py"
$serverPath = $serverPath.Replace('\', '/')

# Claude Desktop config location
$claudeConfigDir = "$env:APPDATA\Claude"
$claudeConfigFile = Join-Path $claudeConfigDir "claude_desktop_config.json"

Write-Host "Server path: $serverPath" -ForegroundColor Cyan
Write-Host "Claude config: $claudeConfigFile" -ForegroundColor Cyan
Write-Host ""

# Create directory if it doesn't exist
if (-not (Test-Path $claudeConfigDir)) {
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
    Write-Host "Created Claude config directory" -ForegroundColor Yellow
}

# Create properly formatted JSON (Claude Desktop prefers readable format)
$configJson = @"
{
  "mcpServers": {
    "precisely": {
      "command": "python",
      "args": [
        "$($serverPath.Replace('\', '/'))"
      ],
      "env": {
        "PRECISELY_API_KEY": "$API_KEY",
        "PRECISELY_API_SECRET": "$API_SECRET"
      }
    }
  }
}
"@

# Write configuration without BOM (Claude Desktop requires clean UTF-8)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($claudeConfigFile, $configJson, $utf8NoBom)

Write-Host ""
Write-Host "Configuration written successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Download Claude Desktop from https://claude.ai/download (if not installed)" -ForegroundColor White
Write-Host "2. Restart Claude Desktop (if already running)" -ForegroundColor White
Write-Host "3. Click the menu icon (☰) in the bottom-left corner" -ForegroundColor White
Write-Host "4. Look for 'precisely' in the connectors list - it should be enabled (toggle on)" -ForegroundColor White
Write-Host "5. Ask Claude: Use precisely to geocode 1600 Pennsylvania Ave" -ForegroundColor White
Write-Host ""
Write-Host "Setup Complete for Claude Desktop!" -ForegroundColor Green
Write-Host "You now have 48 Precisely API tools available in Claude!" -ForegroundColor Cyan
