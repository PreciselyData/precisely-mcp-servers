"""
Verification Tools Module
Contains 6 tools for email verification, phone validation, and name parsing
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of verification tool definitions"""
    return [
        Tool(
            name="verify_email",
            description="Verify single email. Example: {'email': 'john.doe@company.com'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string"}
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="verify_batch_emails",
            description="Verify multiple emails (max 10). Example: {'emails': [{'id': '1', 'email': 'john@company.com'}, {'id': '2', 'email': 'jane@company.com'}]}",
            inputSchema={
                "type": "object",
                "properties": {
                    "emails": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "email": {"type": "string"}}}}
                },
                "required": ["emails"]
            }
        ),
        Tool(
            name="parse_name",
            description="Parse name into components. Example: {'data': {'name': 'John Robert Smith'}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Object with 'name' field containing full name to parse"}
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="validate_phone",
            description="Validate phone number. Example: {'data': {'phoneNumber': '4144654885', 'country': 'US'}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object"}
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="validate_batch_phones",
            description="Validate multiple phones (max 10). Example: {'data': {'phoneNumbers': [{'id': '1', 'phoneNumber': '3035551234', 'country': 'US'}, {'id': '2', 'phoneNumber': '7205559999', 'country': 'US'}]}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "Object with 'phoneNumbers' array containing phone objects with id, phoneNumber, and country fields"}
                },
                "required": ["data"]
            }
        ),
    ]

