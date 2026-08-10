"""
Read-only execution preflight for AURA communication operations.

This module does not execute communication.
It only determines whether a validated operation is
currently eligible for execution.
"""

from communication.operation_validator import validate_operation
from communication.runtime_status import get_runtime_status


def preflight_operation(
    service,
    operation,
    parameters=None,
    confirmed=False,
):
    """
    Determine whether a communication operation is ready
    for execution.

    No communication is executed by this function.
    """

    parameters = parameters or {}

    validation = validate_operation(
        service,
        operation,
        parameters,
    )

    if not validation.get("valid", False):
        return {
            "ready": False,
            "service": service,
            "operation": operation,
            "error": validation.get(
                "error",
                "validation_failed",
            ),
            "validation": validation,
        }

    requires_confirmation = validation.get(
        "requires_confirmation",
        False,
    )

    external_communication = validation.get(
        "external_communication",
        False,
    )

    if requires_confirmation and not confirmed:
        return {
            "ready": False,
            "service": service,
            "operation": operation,
            "error": "confirmation_required",
            "requires_confirmation": True,
            "external_communication": external_communication,
            "validation": validation,
        }

    runtime = get_runtime_status(service)

    runtime_available = runtime.get(
        "available",
        False,
    )

    executable = validation.get(
        "executable",
        False,
    )

    real_connection = runtime.get(
        "real_connection",
        False,
    )

    if not executable:
        return {
            "ready": False,
            "service": service,
            "operation": operation,
            "error": "operation_not_executable",
            "requires_confirmation": requires_confirmation,
            "external_communication": external_communication,
            "runtime": runtime,
        }

    if not runtime_available:
        return {
            "ready": False,
            "service": service,
            "operation": operation,
            "error": "runtime_unavailable",
            "requires_confirmation": requires_confirmation,
            "external_communication": external_communication,
            "runtime": runtime,
        }

    return {
        "ready": True,
        "service": service,
        "operation": operation,
        "parameters": parameters,
        "requires_confirmation": requires_confirmation,
        "confirmed": confirmed,
        "external_communication": external_communication,
        "runtime_available": runtime_available,
        "runtime": runtime.get("runtime"),
        "real_connection": real_connection,
    }


def preflight_whatsapp_send(
    recipient,
    message,
    confirmed=False,
):
    """
    Convenience preflight for WhatsApp send_message.
    """

    return preflight_operation(
        "whatsapp",
        "send_message",
        {
            "recipient": recipient,
            "message": message,
        },
        confirmed=confirmed,
    )
