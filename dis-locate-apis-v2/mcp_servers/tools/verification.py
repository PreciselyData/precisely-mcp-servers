"""
Verification Tools Module
Contains 3 tools for email verification, phone validation, and name parsing
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of verification tool definitions"""
    return [
        Tool(
            name="verify_emails",
            description="""Verify one or more email addresses for deliverability, validity, and format correctness. Checks syntax, domain existence, and MX record reachability to determine whether each address is likely deliverable. Accepts a single email string or an array of email objects (max 10). A single string is automatically handled as a one-item batch. Does not send any email; this is a read-only verification call.

Output: Array of verification result objects (one per input), each containing validity status (e.g., valid, invalid, risky, unknown), domain and other details. Each result includes the 'id' from the corresponding input for correlation when provided.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "emails": {
                        "description": "Email address(es) to verify. Provide a single email string or an array of email objects (max 10).",
                        "oneOf": [
                            {
                                "type": "string",
                                "description": "A single email address to verify (e.g., 'john.doe@company.com').",
                                "format": "email"
                            },
                            {
                                "type": "array",
                                "description": "List of email addresses to verify. Maximum 10 per call.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                        },
                                        "email": {
                                            "type": "string",
                                            "description": "Email address to verify (e.g., 'john@company.com').",
                                            "format": "email"
                                        }
                                    },
                                    "required": ["email"]
                                },
                                "minItems": 1,
                                "maxItems": 10
                            }
                        ]
                    }
                },
                "required": ["emails"]
            }
        ),
        Tool(
            name="parse_name",
            description="""Parse a full personal name, or business name. Personal names parsed  into: title/salutation, first name, middle name, last name, and suffix.Use this tool when you need to decompose a combined name string for data processing, personalization, or storage in structured fields. Do NOT use if you need address parsing — use parse_address or parse_address_batch instead. Works best with Western-style name formats; accuracy may vary for non-Western names.

Output: Object with extracted name components: title (e.g., 'Dr.'), firstName, middleName, lastName, and suffix (e.g., 'Jr.').""",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Wrapper object containing the name to parse.",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Full name string to parse (e.g., 'Dr. John Robert Smith Jr.')."
                            }
                        },
                        "required": ["name"]
                    }
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="validate_phones",
            description="""Validate one or more phone numbers for format correctness, country assignment, and line type (mobile, landline, VoIP, toll-free, etc.). Accepts a single phone object or an array of phone objects (max 10). A single object is automatically handled as a one-item batch. Provide the country code to improve accuracy; without it, the service will attempt to infer the country.

Output: Array of validation result objects (one per input), each containing validity status, formatted phone number (E.164 or local format), country code, line type, and carrier information where available. Each result includes the 'id' from the corresponding input for correlation when provided.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "phones": {
                        "description": "Phone number(s) to validate. Provide a single phone object or an array of phone objects (max 10).",
                        "oneOf": [
                            {
                                "type": "object",
                                "title": "Single phone number",
                                "description": "A single phone number to validate.",
                                "properties": {
                                    "phoneNumber": {
                                        "type": "string",
                                        "description": "Phone number to validate. Can include digits only or common formatting characters (e.g., '4144654885' or '(414) 465-4885')."
                                    },
                                    "country": {
                                        "type": "string",
                                        "description": "Country code in ISO2 or ISO3 format (e.g., 'US', 'GB', 'DE'). Strongly recommended for accurate validation."
                                    }
                                },
                                "required": ["phoneNumber"]
                            },
                            {
                                "type": "array",
                                "title": "Batch phone numbers",
                                "description": "List of phone numbers to validate. Maximum 10 per call.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                        },
                                        "phoneNumber": {
                                            "type": "string",
                                            "description": "Phone number to validate (e.g., '3035551234')."
                                        },
                                        "country": {
                                            "type": "string",
                                            "description": "Country code in ISO2 or ISO3 format (e.g., 'US'). Strongly recommended for accurate validation."
                                        }
                                    },
                                    "required": ["phoneNumber"]
                                },
                                "minItems": 1,
                                "maxItems": 10
                            }
                        ]
                    }
                },
                "required": ["phones"]
            }
        ),
    ]

