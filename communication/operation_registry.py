"""
Communication operation registry for AURA.

Provides read-only metadata describing supported communication
operations. This module does not execute communication actions.
"""

from typing import Dict


_OPERATIONS = {
    "whatsapp": {
        "send_message": {
            "service": "whatsapp",
            "operation": "send_message",
            "parameters": {
                "recipient": {
                    "type": "string",
                    "required": True,
                },
                "message": {
                    "type": "string",
                    "required": True,
                },
            },
            "external_communication": True,
            "requires_confirmation": True,
            "executable": True,
        },
    },
}


def list_operations(service: str):
    """Return supported operations for a communication service."""

    service_value = str(service).strip().lower()

    operations = _OPERATIONS.get(service_value)

    if operations is None:
        return [] 

    return list(operations.keys())


def get_operation(
    service: str,
    operation: str,
) -> Dict:
    """Return metadata for a specific operation."""

    service_value = str(service).strip().lower()
    operation_value = str(operation).strip().lower()

    service_operations = _OPERATIONS.get(service_value)

    if service_operations is None:
        return {
            "service": service_value,
            "operation": operation_value,
            "supported": False,
            "error": "unsupported_service",
        }

    metadata = service_operations.get(operation_value)

    if metadata is None:
        return {
            "service": service_value,
            "operation": operation_value,
            "supported": False,
            "error": "unsupported_operation",
        }

    return dict(metadata)


def get_all_operations() -> Dict:
    """Return metadata for all registered communication operations."""

    return {
        service: {
            operation: dict(metadata)
            for operation, metadata in operations.items()
        }
        for service, operations in _OPERATIONS.items()
    }
