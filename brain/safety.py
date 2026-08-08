
"""
AURA Permission & Safety Engine

The Safety Engine evaluates an action before execution.

It does NOT execute actions.

Decision levels:

ALLOW
    Safe action. Can proceed automatically.

PERMISSION
    Android/service permission may be required.

CONFIRM
    User confirmation is required before execution.

BLOCK
    Action is not permitted.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class SafetyDecision(str, Enum):
    ALLOW = "allow"
    PERMISSION = "permission"
    CONFIRM = "confirm"
    BLOCK = "block"


@dataclass
class SafetyResult:
    decision: SafetyDecision
    reason: str
    tool: str
    requires_confirmation: bool = False
    requires_permission: bool = False


@dataclass
class SafetyRule:
    tool: str
    decision: SafetyDecision
    reason: str


class SafetyEngine:
    """
    Central policy engine for AURA actions.
    """

    def __init__(self):
        self.rules: Dict[str, SafetyRule] = {}

        self._load_default_rules()

    # --------------------------------------------------------
    # Default rules
    # --------------------------------------------------------

    def _load_default_rules(self):

        # Safe actions
        self.add_rule(
            "android.open_app",
            SafetyDecision.ALLOW,
            "Opening an application is normally safe."
        )

        self.add_rule(
            "web.search",
            SafetyDecision.ALLOW,
            "Web search is normally safe."
        )

        self.add_rule(
            "web.open_result",
            SafetyDecision.ALLOW,
            "Opening a previously identified web result is normally safe."
        )

        self.add_rule(
            "files.read",
            SafetyDecision.PERMISSION,
            "Reading device files requires appropriate permission."
        )

        # Communication
        self.add_rule(
            "communication.whatsapp.send",
            SafetyDecision.CONFIRM,
            "Sending an external message requires user confirmation."
        )

        self.add_rule(
            "communication.instagram.send",
            SafetyDecision.CONFIRM,
            "Sending an Instagram message requires user confirmation."
        )

        self.add_rule(
            "communication.email.send",
            SafetyDecision.CONFIRM,
            "Sending an email requires user confirmation."
        )

        # Notifications
        self.add_rule(
            "android.notifications.read",
            SafetyDecision.PERMISSION,
            "Notification access requires explicit Android permission."
        )

        # Device control
        self.add_rule(
            "android.device.control",
            SafetyDecision.PERMISSION,
            "Device control requires appropriate Android permissions."
        )

        # Explicitly blocked examples
        self.add_rule(
            "security.bypass",
            SafetyDecision.BLOCK,
            "AURA will not bypass security controls."
        )

    # --------------------------------------------------------
    # Add / update rule
    # --------------------------------------------------------

    def add_rule(
        self,
        tool: str,
        decision: SafetyDecision,
        reason: str
    ):

        self.rules[tool] = SafetyRule(
            tool=tool,
            decision=decision,
            reason=reason
        )

    # --------------------------------------------------------
    # Remove rule
    # --------------------------------------------------------

    def remove_rule(self, tool: str):

        if tool in self.rules:
            del self.rules[tool]

    # --------------------------------------------------------
    # Evaluate action
    # --------------------------------------------------------

    def evaluate(self, tool: str) -> SafetyResult:

        rule = self.rules.get(tool)

        # Unknown tools are NOT automatically trusted.
        if rule is None:
            return SafetyResult(
                decision=SafetyDecision.PERMISSION,
                reason="Unknown tool requires explicit permission.",
                tool=tool,
                requires_permission=True
            )

        if rule.decision == SafetyDecision.ALLOW:

            return SafetyResult(
                decision=SafetyDecision.ALLOW,
                reason=rule.reason,
                tool=tool
            )

        if rule.decision == SafetyDecision.PERMISSION:

            return SafetyResult(
                decision=SafetyDecision.PERMISSION,
                reason=rule.reason,
                tool=tool,
                requires_permission=True
            )

        if rule.decision == SafetyDecision.CONFIRM:

            return SafetyResult(
                decision=SafetyDecision.CONFIRM,
                reason=rule.reason,
                tool=tool,
                requires_confirmation=True
            )

        return SafetyResult(
            decision=SafetyDecision.BLOCK,
            reason=rule.reason,
            tool=tool
        )

    # --------------------------------------------------------
    # Can execute automatically?
    # --------------------------------------------------------

    def can_execute_automatically(self, tool: str) -> bool:

        result = self.evaluate(tool)

        return result.decision == SafetyDecision.ALLOW

    # --------------------------------------------------------
    # List policies
    # --------------------------------------------------------

    def list_rules(self):

        return list(self.rules.values())
