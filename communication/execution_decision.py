"""
AURA communication execution decision layer.

This module converts execution-preflight results into a
read-only execution decision.

No communication is performed here.
No runtime is started here.
No real WhatsApp connection is created here.
"""

from typing import Any, Dict


BLOCKING_REASONS = {
    "confirmation_required",
    "runtime_unavailable",
    "missing_parameters",
    "unsupported_service",
    "unsupported_operation",
    "invalid_service",
    "invalid_operation",
}


def decide_execution(preflight: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide whether a preflighted operation is eligible for execution.

    This function performs no communication and has no side effects.
    """

    if not isinstance(preflight, dict):
        return {
            "decision": "blocked",
            "executable": False,
            "reason": "invalid_preflight",
        }

    if preflight.get("valid") is not True:
        reason = preflight.get("reason") or preflight.get(
            "error",
            "invalid_preflight",
        )

        return {
            "decision": "blocked",
            "executable": False,
            "reason": reason,
        }

    reason = preflight.get("reason")

    if reason in BLOCKING_REASONS:
        return {
            "decision": "blocked",
            "executable": False,
            "reason": reason,
            "service": preflight.get("service"),
            "operation": preflight.get("operation"),
        }

    if preflight.get("executable_now") is True:
        return {
            "decision": "ready",
            "executable": True,
            "reason": "ready",
            "service": preflight.get("service"),
            "operation": preflight.get("operation"),
            "parameters": preflight.get("parameters", {}),
        }

    return {
        "decision": "blocked",
        "executable": False,
        "reason": reason or "not_ready",
        "service": preflight.get("service"),
        "operation": preflight.get("operation"),
    }


def decide_whatsapp_send(
    recipient: str,
    message: str,
    confirmed: bool = False,
) -> Dict[str, Any]:
    """
    Convenience wrapper for WhatsApp send decisions.

    Imports preflight lazily to avoid introducing circular imports.
    """

    from communication.execution_preflight import preflight_whatsapp_send

    preflight = preflight_whatsapp_send(
        recipient,
        message,
        confirmed=confirmed,
    )

    decision = decide_execution(preflight)

    decision["preflight"] = preflight

    return decision
