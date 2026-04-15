"""
Backward-compatibility shim.

All logic has been moved to the mcp_servers package.
Existing launch commands continue to work unchanged:

    python mcp_servers/precisely_wrapper_server.py
    python mcp_servers/precisely_wrapper_server.py --transport http
"""

import sys
from pathlib import Path

# Ensure the repo root (dis-locate-apis-v2/) is on sys.path so that
# `mcp_servers` is importable when this shim is invoked directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.__main__ import main

if __name__ == "__main__":
    main()
