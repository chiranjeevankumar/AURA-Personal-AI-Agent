"""
Communication operation validation for AURA.

Provides read-only validation of registered communication operations.
This module does not execute operations or create real communication
connections.
"""

from typing import Dict, Optional

from communication.operation_registry import get_operation
from communication.service_registry import get_service_status


def validate_operation(
    service: str,
    operation: str,
    parameters: Optional[Dict] = None,
) -> Dict:
    """
    Validate a communication operation without executing it.
    """

    service_value = str(service).strip().lower()
    operation_value = str(operation).strip().lower()

    if not service_value:
        return {
            "valid": False,
            "service": service_value,
            "operation": operation_value,
            "error": "invalid_service",
        }

    if not operation_value:
        return {
            "valid": False,
            "service": service_value,
            "operation": operation_value,
            "error": "invalid_operation",
        }

    metadata = get_operation(
        service_value,
        operation_value,
    )

    if not metadata.get("supported", True):
        return {
            "valid": False,
            "service": service_value,
            "operation": operation_value,
            "error": metadata.get(
                "error",
                "unsupported_operation",
            ),
        }

    parameters = parameters or {}

    required_parameters = [
        name
        for name, definition
        in metadata.get("parameters", {}).items()
        if definition.get("required", False)
    ]

    missing_parameters = []

    for name in required_parameters:
        value = parameters.get(name)

        if value is None:
            missing_parameters.append(name)
            continue

        if isinstance(value, str) and not value.strip():
            missing_parameters.append(name)

    if missing_parameters:
        return {
            "valid": False,
            "service": service_value,
            "operation": operation_value,
            "error": "missing_parameters",
            "missing_parameters": missing_parameters,
            "requires_confirmation": metadata.get(
                "requires_confirmation",
                False,
            ),
            "external_communication": metadata.get(
                "external_communication",
                False,
            ),
        }

    status = get_service_status(service_value)

    if not status.get("supported", False):
        return {
            "valid": False,
            "service": service_value,
            "operation": operation_value,
            "error": "unsupported_service",
        }

    runtime_available = status.get(
        "runtime",
        "unavailable",
    ) != "unavailable"

    return {
        "valid": True,
        "service": service_value,
        "operation": operation_value,
        "parameters": parameters,
        "requires_confirmation": metadata.get(
            "requires_confirmation",
            False,
        ),
        "external_communication": metadata.get(
            "external_communication",
            False,
        ),
        "executable": metadata.get(
            "executable",
            False,
        ),
        "runtime_available": runtime_available,
        "runtime": status.get(
            "runtime",
            "unavailable",
        ),
    }


def validate_whatsapp_send(
    recipient: str,
    message: str,
) -> Dict:
    """
    Validate a WhatsApp send_message operation.
    """

    return validate_operation(
        "whatsapp",
        "send_message",
        {
            "recipient": recipient,
            "message": message,
        },
    )
