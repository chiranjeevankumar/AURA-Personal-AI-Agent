
"""
AURA Action Pipeline

Connects:

    Reference Resolution
        ↓
    Action Planning
        ↓
    Safety Validation
        ↓
    Agent Execution

The pipeline is an orchestration layer.

It does NOT bypass safety policies.
It does NOT execute blocked actions.
It does NOT automatically confirm external communication.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

from brain.reference_action_planner import (
    ReferenceActionPlanner,
    PlannedReferenceAction,
)

from brain.reference_safety import (
    ReferenceSafetyValidator,
    ReferenceSafetyResult,
    ReferenceSafetyDecision,
)


@dataclass
class PipelineResult:
    """Result returned by the AURA action pipeline."""

    success: bool

    stage: str

    message: str

    action: Optional[
        PlannedReferenceAction
    ] = None

    safety: Optional[
        ReferenceSafetyResult
    ] = None

    execution_result: Any = None

    requires_confirmation: bool = False

    requires_permission: bool = False

    blocked: bool = False


class ActionPipeline:
    """
    Coordinates reference planning, safety validation,
    and optional execution.

    The executor is injected so this class remains
    independent from a particular execution engine.
    """

    def __init__(
        self,
        planner: ReferenceActionPlanner,
        safety_validator: ReferenceSafetyValidator,
        executor=None,
    ):

        self.planner = planner

        self.safety_validator = (
            safety_validator
        )

        self.executor = executor


    # ========================================================
    # PLAN + VALIDATE
    # ========================================================

    def prepare(
        self,
        text: str,
    ) -> PipelineResult:

        # ----------------------------------------------------
        # Planning
        # ----------------------------------------------------

        action = self.planner.plan(text)

        if not action.resolved:

            return PipelineResult(
                success=False,
                stage="planning",
                message=(
                    "AURA could not resolve "
                    "the requested reference."
                ),
                action=action,
            )

        # ----------------------------------------------------
        # Safety
        # ----------------------------------------------------

        safety = self.safety_validator.validate(
            action
        )

        if (
            safety.decision
            == ReferenceSafetyDecision.BLOCK
        ):

            return PipelineResult(
                success=False,
                stage="safety",
                message=safety.reason,
                action=action,
                safety=safety,
                blocked=True,
            )

        if (
            safety.decision
            == ReferenceSafetyDecision.CONFIRM
        ):

            return PipelineResult(
                success=False,
                stage="confirmation",
                message=safety.reason,
                action=action,
                safety=safety,
                requires_confirmation=True,
            )

        if (
            safety.decision
            == ReferenceSafetyDecision.PERMISSION
        ):

            return PipelineResult(
                success=False,
                stage="permission",
                message=safety.reason,
                action=action,
                safety=safety,
                requires_permission=True,
            )

        # ----------------------------------------------------
        # ALLOW
        # ----------------------------------------------------

        return PipelineResult(
            success=True,
            stage="ready",
            message=(
                "Action passed planning "
                "and safety validation."
            ),
            action=action,
            safety=safety,
        )


    # ========================================================
    # EXECUTE SAFE ACTION
    # ========================================================

    def execute(
        self,
        text: str,
        user_confirmed: bool = False,
    ) -> PipelineResult:

        prepared = self.prepare(text)

        # ----------------------------------------------------
        # Stop if preparation failed
        # ----------------------------------------------------

        if not prepared.success:

            # Confirmation is handled here only when
            # explicitly supplied by the caller.
            if (
                prepared.requires_confirmation
                and user_confirmed
            ):
                pass
            else:
                return prepared

        # ----------------------------------------------------
        # Executor must exist
        # ----------------------------------------------------

        if self.executor is None:

            return PipelineResult(
                success=False,
                stage="execution",
                message=(
                    "No executor has been "
                    "connected to the pipeline."
                ),
                action=prepared.action,
                safety=prepared.safety,
            )

        # ----------------------------------------------------
        # Execute through existing executor
        # ----------------------------------------------------

        try:

            execution_result = (
                self.executor.execute_action(
                    prepared.action,
                    user_confirmed=user_confirmed,
                )
            )

        except Exception as error:

            return PipelineResult(
                success=False,
                stage="execution",
                message=(
                    f"Execution failed: {error}"
                ),
                action=prepared.action,
                safety=prepared.safety,
            )

        # ----------------------------------------------------
        # Normalize result
        # ----------------------------------------------------

        success = bool(
            getattr(
                execution_result,
                "success",
                False,
            )
        )

        message = str(
            getattr(
                execution_result,
                "message",
                "Action completed.",
            )
        )

        return PipelineResult(
            success=success,
            stage="completed" if success else "execution",
            message=message,
            action=prepared.action,
            safety=prepared.safety,
            execution_result=execution_result,
        )
