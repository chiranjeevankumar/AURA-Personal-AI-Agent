"""
WhatsApp communication operations for AURA.
"""

import os
from typing import Dict

from communication.whatsapp_runtime import send_message


def send(
    recipient: str,
    message: str,
) -> Dict:
    """
    Send a WhatsApp message.

    The actual runtime is selected through AURA_WHATSAPP_RUNTIME.

    Supported values:

    - unset / "unavailable": no runtime
    - "mock": simulated delivery for testing
    """

    recipient_value = str(recipient).strip()
    message_value = str(message).strip()

    if not recipient_value:
        return {
            "success": False,
            "message": "WhatsApp recipient cannot be empty.",
            "error": "invalid_recipient",
            "recipient": recipient_value,
            "message_text": message_value,
        }

    if not message_value:
        return {
            "success": False,
            "message": "WhatsApp message cannot be empty.",
            "error": "invalid_message",
            "recipient": recipient_value,
            "message_text": message_value,
        }

    runtime = os.environ.get(
        "AURA_WHATSAPP_RUNTIME",
        "unavailable",
    ).strip().lower()

    if runtime == "mock":
        return send_message(
            recipient_value,
            message_value,
        )

    return {
        "success": False,
        "message": (
            "WhatsApp runtime is not available "
            "in the current environment."
        ),
        "error": "whatsapp_runtime_unavailable",
        "recipient": recipient_value,
        "message_text": message_value,
    }
