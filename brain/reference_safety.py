
"""
AURA Reference Safety Validation

Validates planned actions before execution.

Safety decisions:

    ALLOW
        Action may proceed automatically.

    CONFIRM
        AURA must ask the user for confirmation.

    PERMISSION
        Required device/application permission is missing.

    BLOCK
        Action must never be executed.

This module NEVER executes tools.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from brain.reference_action_planner import (
    PlannedReferenceAction,
)


class ReferenceSafetyDecision(str, Enum):
    """Safety decisions for planned reference actions."""

    ALLOW = "allow"

    CONFIRM = "confirm"

    PERMISSION = "permission"

    BLOCK = "block"


@dataclass
class ReferenceSafetyResult:
    """Result of safety validation."""

    decision: ReferenceSafetyDecision

    tool: str

    reason: str

    safe_to_execute: bool = False

    requires_confirmation: bool = False

    requires_permission: bool = False


class ReferenceSafetyValidator:
    """
    Validates planned reference actions.

    This class does not execute actions.
    """

    def __init__(self):

        self.rules: Dict[
            str,
            ReferenceSafetyDecision
        ] = {

            # Safe
            "android.open_app":
                ReferenceSafetyDecision.ALLOW,

            "web.search":
                ReferenceSafetyDecision.ALLOW,

            # Reference-based web navigation
            "web.open_result":
                ReferenceSafetyDecision.ALLOW,

            # Permission
            "files.read":
                ReferenceSafetyDecision.PERMISSION,

            "android.notifications.read":
                ReferenceSafetyDecision.PERMISSION,

            "android.device.control":
                ReferenceSafetyDecision.PERMISSION,

            # External communication
            "communication.whatsapp.send":
                ReferenceSafetyDecision.CONFIRM,

            "communication.instagram.send":
                ReferenceSafetyDecision.CONFIRM,

            "communication.email.send":
                ReferenceSafetyDecision.CONFIRM,

            # Explicitly blocked
            "security.bypass":
                ReferenceSafetyDecision.BLOCK,
        }


    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(
        self,
        action: PlannedReferenceAction,
    ) -> ReferenceSafetyResult:

        tool = action.tool

        # ----------------------------------------------------
        # Invalid / unresolved action
        # ----------------------------------------------------

        if not action.resolved:

            return ReferenceSafetyResult(
                decision=(
                    ReferenceSafetyDecision.BLOCK
                ),
                tool=tool,
                reason=(
                    "Action contains an unresolved "
                    "reference."
                ),
            )

        # ----------------------------------------------------
        # Empty tool
        # ----------------------------------------------------

        if not tool:

            return ReferenceSafetyResult(
                decision=(
                    ReferenceSafetyDecision.BLOCK
                ),
                tool=tool,
                reason=(
                    "No executable tool was "
                    "specified."
                ),
            )

        # ----------------------------------------------------
        # Unknown tool
        # ----------------------------------------------------

        decision = self.rules.get(
            tool
        )

        if decision is None:

            return ReferenceSafetyResult(
                decision=(
                    ReferenceSafetyDecision.PERMISSION
                ),
                tool=tool,
                reason=(
                    "Unknown tool requires "
                    "explicit permission."
                ),
                requires_permission=True,
            )

        # ----------------------------------------------------
        # ALLOW
        # ----------------------------------------------------

        if decision == ReferenceSafetyDecision.ALLOW:

            return ReferenceSafetyResult(
                decision=decision,
                tool=tool,
                reason=(
                    "Action is allowed by "
                    "AURA safety policy."
                ),
                safe_to_execute=True,
            )

        # ----------------------------------------------------
        # CONFIRM
        # ----------------------------------------------------

        if decision == ReferenceSafetyDecision.CONFIRM:

            return ReferenceSafetyResult(
                decision=decision,
                tool=tool,
                reason=(
                    "External communication "
                    "requires user confirmation."
                ),
                requires_confirmation=True,
            )

        # ----------------------------------------------------
        # PERMISSION
        # ----------------------------------------------------

        if decision == ReferenceSafetyDecision.PERMISSION:

            return ReferenceSafetyResult(
                decision=decision,
                tool=tool,
                reason=(
                    "Required permission must "
                    "be granted first."
                ),
                requires_permission=True,
            )

        # ----------------------------------------------------
        # BLOCK
        # ----------------------------------------------------

        return ReferenceSafetyResult(
            decision=(
                ReferenceSafetyDecision.BLOCK
            ),
            tool=tool,
            reason=(
                "This action is blocked by "
                "AURA safety policy."
            ),
        )


    # ========================================================
    # CAN EXECUTE AUTOMATICALLY
    # ========================================================

    def can_execute_automatically(
        self,
        action: PlannedReferenceAction,
    ) -> bool:

        result = self.validate(
            action
        )

        return (
            result.decision
            == ReferenceSafetyDecision.ALLOW
        )


    # ========================================================
    # ADD / UPDATE RULE
    # ========================================================

    def set_rule(
        self,
        tool: str,
        decision: ReferenceSafetyDecision,
    ) -> None:

        self.rules[tool] = decision


    # ========================================================
    # REMOVE RULE
    # ========================================================

    def remove_rule(
        self,
        tool: str,
    ) -> bool:

        if tool in self.rules:

            del self.rules[tool]

            return True

        return False
