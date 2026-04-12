#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');

function findPython311() {
  const candidates = process.platform === 'win32'
    ? ['py -3.11', 'python3.11', 'python']
    : ['python3.11', 'python3', 'python'];

  for (const cmd of candidates) {
    try {
      const version = execSync(`${cmd} --version 2>&1`, { stdio: 'pipe' }).toString().trim();
      if (/Python 3\.11\.\d+/.test(version)) return cmd;
    } catch (_) {}
  }
  return null;
}

const python = findPython311();

if (!python) {
  console.error('\n[precisely-mcp] Error: Python 3.11 is required to install dependencies.');
  console.error('  macOS:   brew install python@3.11');
  console.error('  Linux:   sudo apt install python3.11');
  console.error('  Windows: https://www.python.org/downloads/release/python-3110/\n');
  process.exit(1);
}

const requirements = path.join(__dirname, '..', 'requirements.txt');

try {
  console.log(`[precisely-mcp] Installing Python dependencies with ${python}...`);
  execSync(`${python} -m pip install -r "${requirements}" --quiet`, { stdio: 'inherit' });
  console.log('[precisely-mcp] Python dependencies installed successfully.');
} catch (err) {
  console.error('[precisely-mcp] Failed to install Python dependencies.');
  console.error(`  Run manually: ${python} -m pip install -r requirements.txt`);
  process.exit(1);
}
