"""
Communication service capability metadata for AURA.

This module is read-only metadata.
It does not create connections or execute communication actions.
"""

from typing import Dict


_SERVICE_CAPABILITIES = {
    "whatsapp": {
        "service": "whatsapp",
        "operations": [
            "send_message",
        ],
        "supported_runtimes": [
            "mock",
        ],
        "real_connection": False,
        "external_communication": True,
        "requires_confirmation": True,
    },
}


def get_service_capabilities(service: str) -> Dict:
    """
    Return capability metadata for a communication service.
    """

    service_name = str(service).strip().lower()

    if service_name not in _SERVICE_CAPABILITIES:
        return {
            "service": service_name,
            "supported": False,
            "error": "unsupported_service",
        }

    return dict(_SERVICE_CAPABILITIES[service_name])


def get_all_service_capabilities() -> Dict:
    """
    Return capability metadata for all supported services.
    """

    return {
        name: dict(capabilities)
        for name, capabilities in _SERVICE_CAPABILITIES.items()
    }
