"""Shared request-scoped context variables."""

from contextvars import ContextVar
from typing import Optional

# Set by BearerTokenMiddleware for each HTTP request.
# call_tool reads this to forward caller-supplied tokens to the Precisely API.
_request_bearer_token: ContextVar[Optional[str]] = ContextVar(
    "_request_bearer_token", default=None
)
