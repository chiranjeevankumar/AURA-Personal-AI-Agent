"""
Communication runtime selector for AURA.

This module selects a safe communication runtime based on
the configured environment.
"""

import os

from communication.runtime import runtime_unavailable
from communication.whatsapp_runtime import send_message


def get_whatsapp_runtime():
    """
    Return the configured WhatsApp runtime.

    Supported runtime:

    - mock

    Any other value returns None, which means the runtime
    is safely unavailable.
    """

    runtime = os.environ.get(
        "AURA_WHATSAPP_RUNTIME",
        "unavailable",
    ).strip().lower()

    if runtime == "mock":
        return send_message

    return None


def send_whatsapp(
    recipient: str,
    message: str,
):
    """
    Send through the selected WhatsApp runtime.

    If no runtime is available, return a safe failure.
    """

    runtime = get_whatsapp_runtime()

    if runtime is None:
        return runtime_unavailable(
            "WhatsApp",
            recipient,
            message,
        )

    return runtime(
        recipient,
        message,
    )
