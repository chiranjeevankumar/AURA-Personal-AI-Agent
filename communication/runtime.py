"""
Communication runtime abstraction for AURA.

Provides a small common interface for communication backends.
"""

from typing import Dict, Protocol


class CommunicationRuntime(Protocol):
    """
    Protocol implemented by communication runtimes.
    """

    def send_message(
        self,
        recipient: str,
        message: str,
    ) -> Dict:
        ...


def runtime_unavailable(
    service: str,
    recipient: str,
    message: str,
) -> Dict:
    """
    Return a safe result when a runtime is unavailable.
    """

    return {
        "success": False,
        "message": (
            f"{service} runtime is not available "
            "in the current environment."
        ),
        "error": f"{service.lower()}_runtime_unavailable",
        "recipient": str(recipient).strip(),
        "message_text": str(message).strip(),
    }
