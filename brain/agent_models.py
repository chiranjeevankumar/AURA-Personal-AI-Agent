
"""
AURA Agent Core
Data models used throughout the Personal AI Agent.

These models deliberately do not depend on any AI provider.
That allows us to change AI backends later without rebuilding
the entire agent.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class RiskLevel(str, Enum):
    SAFE = "safe"
    PERSONAL_DATA = "personal_data"
    EXTERNAL_COMMUNICATION = "external_communication"
    SENSITIVE = "sensitive"
    BLOCKED = "blocked"


class ActionStatus(str, Enum):
    PENDING = "pending"
    WAITING_CONFIRMATION = "waiting_confirmation"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class UserRequest:
    """
    The original instruction received from the user.
    """

    text: str
    source: str = "text"
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


@dataclass
class Intent:
    """
    AURA's interpretation of what the user wants.
    """

    name: str
    confidence: float = 0.0
    parameters: Dict[str, Any] = field(default_factory=dict)
    risk: RiskLevel = RiskLevel.SAFE


@dataclass
class PlannedAction:
    """
    One action that AURA intends to perform.
    """

    tool: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    risk: RiskLevel = RiskLevel.SAFE
    requires_confirmation: bool = False
    status: ActionStatus = ActionStatus.PENDING


@dataclass
class AgentPlan:
    """
    Complete plan generated for a user request.
    """

    request: UserRequest
    intent: Intent
    actions: List[PlannedAction] = field(default_factory=list)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


@dataclass
class ActionResult:
    """
    Result returned after an action is attempted.
    """

    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    verified: bool = False
    status: ActionStatus = ActionStatus.SUCCESS


@dataclass
class AgentResponse:
    """
    Final response presented to the user.
    """

    message: str
    success: bool
    plan: Optional[AgentPlan] = None
    results: List[ActionResult] = field(default_factory=list)
