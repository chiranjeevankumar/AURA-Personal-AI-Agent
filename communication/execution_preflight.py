"""
Execution preflight checks for AURA communication operations.

This module is read-only.

It determines whether a validated communication operation
is currently eligible for execution.

No communication is performed here.
No real service connection is created here.
"""

from communication.operation_validator import validate_operation
from communication.runtime_status import get_runtime_status


def preflight_operation(
    service: str,
    operation: str,
    parameters: dict,
    confirmed: bool = False,
) -> dict:
    """
    Determine whether a communication operation is eligible
    for execution.

    No external action is performed.
    """

    validation = validate_operation(
        service,
        operation,
        parameters,
    )

    if not validation.get("valid", False):
        return {
            **validation,
            "preflight": False,
            "executable_now": False,
            "reason": validation.get("error", "validation_failed"),
        }

    requires_confirmation = validation.get(
        "requires_confirmation",
        False,
    )

    if requires_confirmation and not confirmed:
        return {
            **validation,
            "preflight": False,
            "executable_now": False,
            "reason": "confirmation_required",
        }

    runtime = get_runtime_status(service)

    if not runtime.get("available", False):
        return {
            **validation,
            "preflight": False,
            "executable_now": False,
            "runtime_available": False,
            "runtime": runtime.get("runtime", "unavailable"),
            "reason": "runtime_unavailable",
        }

    if not runtime.get("executable", False):
        return {
            **validation,
            "preflight": False,
            "executable_now": False,
            "runtime_available": runtime.get(
                "available",
                False,
            ),
            "runtime": runtime.get(
                "runtime",
                "unknown",
            ),
            "reason": "runtime_not_executable",
        }

    return {
        **validation,
        "preflight": True,
        "executable_now": True,
        "runtime_available": True,
        "runtime": runtime.get(
            "runtime",
            "unknown",
        ),
        "reason": "ready",
    }


def preflight_whatsapp_send(
    recipient: str,
    message: str,
    confirmed: bool = False,
) -> dict:
    """
    Preflight a WhatsApp send operation.

    No WhatsApp message is sent.
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
