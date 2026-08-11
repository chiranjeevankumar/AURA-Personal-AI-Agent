"""
AURA communication execution guard.

This module performs a final read-only safety check before
communication execution.

It does not execute communication.
It does not connect to external services.
"""

from communication.execution_authorization import (
    authorize_execution,
    authorize_whatsapp_send,
)


def guard_execution(
    service,
    operation,
    parameters=None,
    confirmed=False,
):
    """
    Determine whether an operation is allowed past the
    communication execution guard.

    This function is read-only.
    It never executes the operation.
    """

    authorization = authorize_execution(
        service=service,
        operation=operation,
        parameters=parameters,
        confirmed=confirmed,
    )

    if authorization.get("authorized") is not True:
        return {
            "guarded": True,
            "allowed": False,
            "reason": authorization.get("reason"),
            "service": service,
            "operation": operation,
            "authorization": authorization,
        }

    return {
        "guarded": True,
        "allowed": True,
        "reason": "authorized",
        "service": service,
        "operation": operation,
        "parameters": authorization.get("parameters"),
        "authorization": authorization,
    }


def guard_whatsapp_send(
    recipient,
    message,
    confirmed=False,
):
    """
    Guard a WhatsApp send operation.

    This function only evaluates whether execution is allowed.
    It never sends a WhatsApp message.
    """

    return guard_execution(
        service="whatsapp",
        operation="send_message",
        parameters={
            "recipient": recipient,
            "message": message,
        },
        confirmed=confirmed,
    )
