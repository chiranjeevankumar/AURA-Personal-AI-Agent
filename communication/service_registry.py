"""
Communication service registry for AURA.

Provides a central, read-only registry of supported communication
services and their runtime status.

This module does not connect to external services.
"""

from typing import Dict, List

from communication.runtime_status import get_runtime_status


SUPPORTED_SERVICES = (
    "whatsapp",
)


def list_services() -> List[str]:
    """
    Return the communication services currently supported by AURA.
    """
    return list(SUPPORTED_SERVICES)


def get_service_status(service: str) -> Dict:
    """
    Return runtime status for a supported communication service.
    """
    service_name = str(service).strip().lower()

    if service_name not in SUPPORTED_SERVICES:
        return {
            "service": service_name,
            "supported": False,
            "status": "unsupported",
            "error": "unsupported_service",
        }

    status = get_runtime_status(service_name)

    return {
        "service": service_name,
        "supported": True,
        "status": (
            "available"
            if status.get("available")
            else "unavailable"
        ),
        "runtime": status.get("runtime"),
        "available": status.get("available", False),
        "executable": status.get("executable", False),
        "real_connection": status.get("real_connection", False),
    }


def get_all_service_status() -> Dict[str, Dict]:
    """
    Return status for every supported communication service.
    """
    return {
        service: get_service_status(service)
        for service in SUPPORTED_SERVICES
    }
