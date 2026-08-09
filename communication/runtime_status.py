"""
Communication runtime status utilities for AURA.

Provides read-only information about configured communication
runtimes. This module does not execute or connect to any service.
"""

import os
from typing import Dict


def get_whatsapp_status() -> Dict:
    """
    Return the current WhatsApp runtime status.

    Supported runtime:
    - mock

    Any other value is considered unavailable.
    """

    configured = os.environ.get(
        "AURA_WHATSAPP_RUNTIME",
        "unavailable",
    ).strip().lower()

    if configured == "mock":
        return {
            "service": "whatsapp",
            "runtime": "mock",
            "available": True,
            "executable": True,
            "real_connection": False,
        }

    return {
        "service": "whatsapp",
        "runtime": "unavailable",
        "available": False,
        "executable": False,
        "real_connection": False,
    }


def get_runtime_status(service: str) -> Dict:
    """
    Return runtime status for a supported communication service.
    """

    service_value = str(service).strip().lower()

    if service_value == "whatsapp":
        return get_whatsapp_status()

    return {
        "service": service_value,
        "runtime": "unavailable",
        "available": False,
        "executable": False,
        "real_connection": False,
        "error": "unsupported_service",
    }
