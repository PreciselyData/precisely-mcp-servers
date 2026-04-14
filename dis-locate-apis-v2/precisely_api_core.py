"""
Backward-compatibility shim.

All logic has been moved to the `precisely/` package.
Importing PreciselyAPI from this module continues to work unchanged.
"""

from precisely import PreciselyAPI  # noqa: F401

__all__ = ["PreciselyAPI"]
