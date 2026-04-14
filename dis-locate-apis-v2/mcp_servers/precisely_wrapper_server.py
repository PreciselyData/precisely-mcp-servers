"""
Backward-compatibility shim.

All logic has been moved to the mcp_servers package.
Existing launch commands continue to work unchanged:

    python mcp_servers/precisely_wrapper_server.py
    python mcp_servers/precisely_wrapper_server.py --transport http
"""

from mcp_servers.__main__ import main  # noqa: F401

if __name__ == "__main__":
    main()
