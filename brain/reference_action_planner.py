
"""
AURA Reference Action Planner

Converts conversational references into structured,
non-executing actions.

Pipeline:

    User input
        ↓
    ReferenceResolver
        ↓
    ReferenceActionPlanner
        ↓
    SafetyEngine
        ↓
    Executor

This module NEVER executes tools.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from memory.context_manager import ConversationContext
from brain.reference_resolver import (
    ReferenceResolver,
    ReferenceResult,
)


@dataclass
class PlannedReferenceAction:
    """Structured action produced from a conversation reference."""

    tool: str

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    source_reference: Optional[str] = None

    requires_resolution: bool = False

    resolved: bool = False

    reason: str = ""


class ReferenceActionPlanner:
    """
    Converts supported conversational references
    into structured actions.

    IMPORTANT:
        This class only plans.
        It does not execute tools.
    """

    def __init__(
        self,
        context: ConversationContext,
    ):
        self.context = context

        self.resolver = ReferenceResolver(
            context
        )

    def plan(
        self,
        text: str,
    ) -> PlannedReferenceAction:

        reference = self.resolver.resolve(
            text
        )

        if not reference.resolved:

            return PlannedReferenceAction(
                tool="",
                source_reference=text,
                requires_resolution=False,
                resolved=False,
                reason=(
                    "No supported conversational "
                    "reference found."
                ),
            )

        if reference.reference_type == "result":

            return self._plan_result(
                reference
            )

        if reference.reference_type == "application":

            return PlannedReferenceAction(
                tool="android.open_app",
                parameters={
                    "application": reference.value
                },
                source_reference=text,
                requires_resolution=True,
                resolved=True,
                reason=(
                    "Resolved application "
                    "reference."
                ),
            )

        if reference.reference_type == "search":

            return PlannedReferenceAction(
                tool="web.search",
                parameters={
                    "query": reference.value
                },
                source_reference=text,
                requires_resolution=True,
                resolved=True,
                reason=(
                    "Resolved search reference."
                ),
            )

        return PlannedReferenceAction(
            tool="",
            source_reference=text,
            requires_resolution=True,
            resolved=False,
            reason=(
                "Reference type is not supported "
                "by the action planner."
            ),
        )

    def _plan_result(
        self,
        reference: ReferenceResult,
    ) -> PlannedReferenceAction:

        return PlannedReferenceAction(
            tool="web.open_result",
            parameters={
                "index": reference.index
            },
            source_reference=(
                f"result[{reference.index}]"
            ),
            requires_resolution=True,
            resolved=True,
            reason=(
                "Resolved result reference "
                "into a structured web action."
            ),
        )
