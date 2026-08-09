"""
WhatsApp communication operations for AURA.
"""

from typing import Dict

from communication.runtime_selector import send_whatsapp


def send(
    recipient: str,
    message: str,
) -> Dict:
    """
    Send a WhatsApp message through the selected runtime.
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

    return send_whatsapp(
        recipient_value,
        message_value,
    )
