"""Email, name, and phone verification API methods."""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class VerificationMixin:
    def verify_emails(self, emails, **kwargs) -> Dict[str, Any]:
        """Verify one or more email addresses for deliverability, validity, and format.

        Accepts a single email string or a list of emails (strings or objects).
        Always uses the batch endpoint; a single string is auto-wrapped.

        Args:
            emails: A single email string (e.g., "john@company.com"),
                a list of email strings, or a list of dicts with 'email'
                (and optional 'id') keys.  Maximum 10 emails per call.
        """
        try:
            url = f"{self.base_url}/v1/emails/verify/batch"

            # Normalize input → list of {"email": ...} dicts
            if isinstance(emails, str):
                processed_emails = [{"email": emails}]
            elif isinstance(emails, list):
                processed_emails = []
                for entry in emails:
                    if isinstance(entry, str):
                        processed_emails.append({"email": entry})
                    elif isinstance(entry, dict):
                        if "email" in entry:
                            processed_emails.append(entry)
                        else:
                            email_value = None
                            for key, value in entry.items():
                                if "email" in key.lower() or "@" in str(value):
                                    email_value = value
                                    break
                            if email_value:
                                processed_emails.append({"email": email_value})
                            else:
                                logger.warning(f"Could not extract email from object: {entry}")
                    else:
                        logger.warning(f"Skipping unsupported email entry type: {type(entry)}")
            else:
                return self._build_error(
                    "Email verification",
                    ValueError("'emails' must be a string or a list of email strings/objects."),
                )

            if not processed_emails:
                return self._build_error(
                    "Email verification",
                    ValueError("No valid email addresses provided."),
                )

            json_data = {"emails": processed_emails}
            logger.debug(f"[verify_emails] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_emails] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Email verification error: {e}")
            return self._build_error("Email verification", e)

    def parse_name(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Parse a name"""
        try:
            url = f"{self.base_url}/v1/names/parse"
            json_data = data
            logger.debug(f"[parse_name] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[parse_name] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Name parsing error: {e}")
            return self._build_error("Name parsing", e)

    def validate_phones(self, phones, **kwargs) -> Dict[str, Any]:
        """Validate one or more phone numbers for format, country, and line type.

        Accepts a single phone object or a list of phone objects.
        Always uses the batch endpoint; a single object is auto-wrapped.

        Args:
            phones: A dict with 'phoneNumber' (and optional 'country', 'id') for
                a single phone, or a list of such dicts. Maximum 10 per call.
        """
        try:
            url = f"{self.base_url}/v1/phone-numbers/validate/batch"

            # Normalize input → list of phone dicts
            if isinstance(phones, dict) and "phoneNumber" in phones:
                # Single phone object
                processed_phones = [phones]
            elif isinstance(phones, list):
                processed_phones = phones
            else:
                return self._build_error(
                    "Phone validation",
                    ValueError(
                        "'phones' must be a dict with 'phoneNumber' key "
                        "or a list of such dicts."
                    ),
                )

            if not processed_phones:
                return self._build_error(
                    "Phone validation",
                    ValueError("No phone numbers provided."),
                )

            json_data = {"phoneNumbers": processed_phones}
            logger.debug(f"[validate_phones] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[validate_phones] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Phone validation error: {e}")
            return self._build_error("Phone validation", e)
