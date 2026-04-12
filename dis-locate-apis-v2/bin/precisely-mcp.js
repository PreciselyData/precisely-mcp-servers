#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const { execSync } = require('child_process');

// Find Python 3.11 specifically
function findPython() {
  for (const cmd of ['python3.11', 'python3', 'python']) {
    try {
      const version = execSync(`${cmd} --version 2>&1`, { stdio: 'pipe' }).toString().trim();
      if (/Python 3\.11\.\d+/.test(version)) return cmd;
    } catch (_) {}
  }
  return null;
}

const python = findPython();

if (!python) {
  console.error('[precisely-mcp] Error: Python 3.11 is required but not found.');
  console.error('  Install Python 3.11 from https://www.python.org/downloads/release/python-3110/');
  console.error('  macOS: brew install python@3.11');
  process.exit(1);
}

const serverScript = path.join(__dirname, '..', 'mcp_servers', 'precisely_wrapper_server.py');
const args = [serverScript, ...process.argv.slice(2)];

const server = spawn(python, args, {
  stdio: 'inherit',
  env: process.env
});

server.on('error', (err) => {
  if (err.code === 'ENOENT') {
    console.error(`[precisely-mcp] Could not find Python executable: ${python}`);
  } else {
    console.error(`[precisely-mcp] Failed to start server: ${err.message}`);
  }
  process.exit(1);
});

server.on('exit', (code) => {
  process.exit(code ?? 0);
});

process.on('SIGINT', () => server.kill('SIGINT'));
process.on('SIGTERM', () => server.kill('SIGTERM'));
