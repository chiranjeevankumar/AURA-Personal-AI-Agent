
"""
AURA Follow-up Reference Integration

Routes supported conversational follow-ups through the
reference action pipeline while leaving normal commands
on the existing AURAAgent path.

Flow:

    User text
        ↓
    Reference detection
        ↓
    ActionPipeline
        ↓
    AgentExecutor

This module does not execute tools directly.
"""

from dataclasses import dataclass
from typing import Optional, Any

from memory.context_manager import ConversationContext

from brain.reference_resolver import ReferenceResolver
from brain.reference_action_planner import ReferenceActionPlanner
from brain.reference_safety import ReferenceSafetyValidator
from brain.action_pipeline import ActionPipeline


@dataclass
class FollowUpResult:
    """Result of attempting follow-up routing."""

    is_follow_up: bool
    handled: bool
    result: Optional[Any] = None
    reason: str = ""


class FollowUpIntegration:
    """
    Detects and routes conversational references.

    Normal commands are deliberately left untouched so the
    existing AURAAgent remains responsible for ordinary
    intent routing and execution.
    """

    def __init__(
        self,
        context: ConversationContext,
        executor=None,
    ):
        self.context = context

        self.resolver = ReferenceResolver(
            context
        )

        self.planner = ReferenceActionPlanner(
            context
        )

        self.safety_validator = (
            ReferenceSafetyValidator()
        )

        self.pipeline = ActionPipeline(
            planner=self.planner,
            safety_validator=self.safety_validator,
            executor=executor,
        )

    def detect(
        self,
        text: str,
    ) -> bool:
        """
        Return True only when the resolver recognizes
        a supported conversational reference.
        """

        reference = self.resolver.resolve(text)

        return reference.resolved

    def handle(
        self,
        text: str,
        user_confirmed: bool = False,
    ) -> FollowUpResult:
        """
        Attempt to route a conversational follow-up.

        If the text is not a supported reference, the caller
        should continue through the normal AURAAgent path.
        """

        reference = self.resolver.resolve(text)

        if not reference.resolved:

            return FollowUpResult(
                is_follow_up=False,
                handled=False,
                reason=reference.reason,
            )

        result = self.pipeline.execute(
            text,
            user_confirmed=user_confirmed,
        )

        return FollowUpResult(
            is_follow_up=True,
            handled=True,
            result=result,
            reason=reference.reason,
        )
