"""
Mock WhatsApp runtime for AURA testing.

This module never contacts WhatsApp or sends real messages.
"""

from typing import Dict


def send_message(
    recipient: str,
    message: str,
) -> Dict:
    """
    Simulate successful WhatsApp message delivery.
    """

    recipient_value = str(recipient).strip()
    message_value = str(message).strip()

    if not recipient_value:
        return {
            "success": False,
            "message": "WhatsApp recipient cannot be empty.",
            "error": "invalid_recipient",
        }

    if not message_value:
        return {
            "success": False,
            "message": "WhatsApp message cannot be empty.",
            "error": "invalid_message",
        }

    return {
        "success": True,
        "message": "WhatsApp message sent successfully.",
        "error": None,
        "recipient": recipient_value,
        "message_text": message_value,
        "runtime": "mock",
        "delivered": True,
    }
