"""
Verification Tools Module
Contains 5 tools for email verification, phone validation, and name parsing
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of verification tool definitions"""
    return [
        Tool(
            name="verify_email",
            description=(
                "Verify a single email address for deliverability, validity, and format correctness. "
                "Checks syntax, domain existence, and MX record reachability to determine "
                "whether the address is likely deliverable. "
                "Use this tool when you need to validate one email address before sending or storing it. "
                "Do NOT use for bulk validation of multiple emails — use verify_batch_emails instead "
                "(more efficient for 2 or more addresses). "
                "Does not send any email; this is a read-only verification call.\n\n"
                "Output: Object with verification result including validity status "
                "(e.g., valid, invalid, risky, unknown), confidence score, reason code, "
                "corrected email (if applicable), and domain details."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email address to verify (e.g., 'john.doe@company.com').",
                        "format": "email"
                    }
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="verify_batch_emails",
            description=(
                "Verify multiple email addresses for deliverability and validity in a single batch call. "
                "Checks syntax, domain existence, and MX record reachability for each address. "
                "Use this tool when you have two or more email addresses to validate "
                "(more efficient than repeated verify_email calls). "
                "Do NOT use for a single email — use verify_email instead. "
                "Maximum batch size: 10 addresses per call. "
                "Does not send any email; this is a read-only verification call.\n\n"
                "Output: Array of verification result objects (one per input), each containing validity status, "
                "confidence score, reason code, and corrected email if applicable. "
                "Each result includes the 'id' from the corresponding input for correlation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "emails": {
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
                            "required": ["id", "email"]
                        },
                        "minItems": 1,
                        "maxItems": 10
                    }
                },
                "required": ["emails"]
            }
        ),
        Tool(
            name="parse_name",
            description=(
                "Parse a full personal name string into its individual components: "
                "title/salutation, first name, middle name, last name, and suffix. "
                "Use this tool when you need to decompose a combined name string for data processing, "
                "personalization, or storage in structured fields. "
                "Do NOT use if you need address parsing — use parse_address or parse_address_batch instead. "
                "Works best with Western-style name formats; accuracy may vary for non-Western names.\n\n"
                "Output: Object with extracted name components: "
                "title (e.g., 'Dr.'), firstName, middleName, lastName, and suffix (e.g., 'Jr.')."
            ),
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
            name="validate_phone",
            description=(
                "Validate a single phone number for format correctness, country assignment, "
                "and line type (mobile, landline, VoIP, toll-free, etc.). "
                "Use this tool when you need to validate one phone number before storing or dialing it. "
                "Do NOT use for bulk validation of multiple numbers — use validate_batch_phones instead "
                "(more efficient for 2 or more numbers). "
                "Provide the country code to improve accuracy; without it, the service will attempt to infer the country.\n\n"
                "Output: Object with validation result including validity status, formatted phone number "
                "(E.164 or local format), country code, line type (mobile/landline/VoIP/toll-free), "
                "and carrier information where available."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Phone number validation request.",
                        "properties": {
                            "phoneNumber": {
                                "type": "string",
                                "description": "Phone number to validate. Can include digits only or common formatting characters (e.g., '4144654885' or '(414) 465-4885')."
                            },
                            "country": {
                                "type": "string",
                                "description": "ISO 2-letter country code to scope the validation (e.g., 'US', 'GB', 'DE'). Strongly recommended for accurate validation."
                            }
                        },
                        "required": ["phoneNumber"]
                    }
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="validate_batch_phones",
            description=(
                "Validate multiple phone numbers for format correctness, country assignment, "
                "and line type in a single batch call. "
                "Use this tool when you have two or more phone numbers to validate "
                "(more efficient than repeated validate_phone calls). "
                "Do NOT use for a single number — use validate_phone instead. "
                "Maximum batch size: 10 phone numbers per call.\n\n"
                "Output: Array of validation result objects (one per input), each containing validity status, "
                "formatted phone number, country code, line type, and carrier information. "
                "Each result includes the 'id' from the corresponding input for correlation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Batch phone validation request.",
                        "properties": {
                            "phoneNumbers": {
                                "type": "array",
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
                                            "description": "ISO 2-letter country code (e.g., 'US'). Strongly recommended for accurate validation."
                                        }
                                    },
                                    "required": ["id", "phoneNumber"]
                                },
                                "minItems": 1,
                                "maxItems": 10
                            }
                        },
                        "required": ["phoneNumbers"]
                    }
                },
                "required": ["data"]
            }
        ),
    ]

