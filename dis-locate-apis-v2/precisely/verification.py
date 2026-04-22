"""Email, name, and phone verification API methods."""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class VerificationMixin:
    def verify_email(self, email: str, **kwargs) -> Dict[str, Any]:
        """Verify a single email address"""
        try:
            url = f"{self.base_url}/v1/emails/verify"
            json_data = {"email": email}
            logger.debug(f"[verify_email] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_email] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Email verification error: {e}")
            return self._build_error("Email verification", e)

    def verify_batch_emails(self, emails: List, **kwargs) -> Dict[str, Any]:
        """Verify a batch of email addresses - accepts either strings or objects"""
        try:
            url = f"{self.base_url}/v1/emails/verify/batch"
            processed_emails = []
            for email in emails:
                if isinstance(email, str):
                    processed_emails.append({"email": email})
                elif isinstance(email, dict):
                    if "email" in email:
                        processed_emails.append(email)
                    else:
                        email_value = None
                        for key, value in email.items():
                            if "email" in key.lower() or "@" in str(value):
                                email_value = value
                                break
                        if email_value:
                            processed_emails.append({"email": email_value})
                        else:
                            logger.warning(f"Could not extract email from object: {email}")
            json_data = {"emails": processed_emails}
            logger.debug(f"[verify_batch_emails] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[verify_batch_emails] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Batch email verification error: {e}")
            return self._build_error("Batch email verification", e)

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

    def validate_phone(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Validate a phone number"""
        try:
            url = f"{self.base_url}/v1/phone-numbers/validate"
            json_data = data
            logger.debug(f"[validate_phone] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[validate_phone] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Phone validation error: {e}")
            return self._build_error("Phone validation", e)

    def validate_batch_phones(self, data: Dict, **kwargs) -> Dict[str, Any]:
        """Validate a batch of phone numbers"""
        try:
            url = f"{self.base_url}/v1/phone-numbers/validate/batch"
            json_data = data
            logger.debug(f"[validate_batch_phones] Request payload: {json.dumps(json_data, indent=2)}")
            response = self.session.post(url, json=json_data)
            logger.debug(f"[validate_batch_phones] Raw response: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Batch phone validation error: {e}")
            return self._build_error("Batch phone validation", e)
