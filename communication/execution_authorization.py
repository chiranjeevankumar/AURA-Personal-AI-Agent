"""
AURA execution authorization layer.

This module evaluates whether an operation has received
the required authorization to proceed.

Read-only:
- Does not execute communication.
- Does not send messages.
- Does not create real connections.
- Does not bypass confirmation requirements.
"""

from communication.execution_decision import decide_execution


def authorize_execution(
    service,
    operation,
    parameters=None,
    confirmed=False,
):
    """
    Determine whether an operation is authorized for execution.

    This function is read-only. It does not execute the operation.
    """

    from communication.execution_preflight import preflight_operation

    preflight = preflight_operation(
        service=service,
        operation=operation,
        parameters=parameters,
        confirmed=confirmed,
    )

    decision = decide_execution(preflight)

    if decision.get("decision") != "ready":
        return {
            "authorized": False,
            "executable": False,
            "reason": decision.get("reason"),
            "service": service,
            "operation": operation,
            "decision": decision,
        }

    return {
        "authorized": True,
        "executable": True,
        "reason": "authorized",
        "service": service,
        "operation": operation,
        "parameters": decision.get("parameters"),
        "decision": decision,
    }


def authorize_whatsapp_send(
    recipient,
    message,
    confirmed=False,
):
    """
    Authorize a WhatsApp send operation.

    This function only evaluates authorization.
    It never sends a WhatsApp message.
    """

    return authorize_execution(
        service="whatsapp",
        operation="send_message",
        parameters={
            "recipient": recipient,
            "message": message,
        },
        confirmed=confirmed,
    )
