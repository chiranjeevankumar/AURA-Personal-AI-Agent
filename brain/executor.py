
"""
AURA Agent Executor

Responsible for safely executing planned actions.

Flow:

Plan
 ↓
Safety Check
 ↓
Tool Lookup
 ↓
Confirmation Check
 ↓
Execution
 ↓
Result
 ↓
Verification
"""

from typing import List

from brain.agent_models import (
    AgentPlan,
    ActionResult,
    ActionStatus,
)

from brain.safety import (
    SafetyEngine,
    SafetyDecision,
)

from tools.registry import ToolRegistry


class AgentExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
        safety_engine: SafetyEngine
    ):

        self.registry = registry
        self.safety_engine = safety_engine

    # --------------------------------------------------------
    # Execute complete plan
    # --------------------------------------------------------

    def execute_plan(
        self,
        plan: AgentPlan,
        user_confirmed: bool = False
    ) -> List[ActionResult]:

        results = []

        for action in plan.actions:

            result = self.execute_action(
                action,
                user_confirmed=user_confirmed
            )

            results.append(result)

            # Stop if an action fails or is blocked.
            if not result.success:

                break

        return results

    # --------------------------------------------------------
    # Execute one action
    # --------------------------------------------------------

    def execute_action(
        self,
        action,
        user_confirmed: bool = False
    ) -> ActionResult:

        tool_name = action.tool

        # ----------------------------------------------------
        # Safety evaluation
        # ----------------------------------------------------

        safety = self.safety_engine.evaluate(tool_name)

        if safety.decision == SafetyDecision.BLOCK:

            action.status = ActionStatus.CANCELLED

            return ActionResult(
                success=False,
                message=(
                    f"Action blocked: {safety.reason}"
                ),
                verified=False,
                status=ActionStatus.CANCELLED
            )

        # ----------------------------------------------------
        # Permission
        # ----------------------------------------------------

        if safety.decision == SafetyDecision.PERMISSION:

            action.status = ActionStatus.CANCELLED

            return ActionResult(
                success=False,
                message=(
                    f"Permission required: {safety.reason}"
                ),
                verified=False,
                status=ActionStatus.CANCELLED
            )

        # ----------------------------------------------------
        # Confirmation
        # ----------------------------------------------------

        if safety.decision == SafetyDecision.CONFIRM:

            if not user_confirmed:

                action.status = (
                    ActionStatus.WAITING_CONFIRMATION
                )

                return ActionResult(
                    success=False,
                    message=(
                        "User confirmation is required "
                        "before this action can be executed."
                    ),
                    verified=False,
                    status=(
                        ActionStatus.WAITING_CONFIRMATION
                    )
                )

        # ----------------------------------------------------
        # Tool lookup
        # ----------------------------------------------------

        tool = self.registry.get(tool_name)

        if tool is None:

            action.status = ActionStatus.FAILED

            return ActionResult(
                success=False,
                message=f"Tool not found: {tool_name}",
                verified=False,
                status=ActionStatus.FAILED
            )

        if not tool.enabled:

            action.status = ActionStatus.FAILED

            return ActionResult(
                success=False,
                message=f"Tool disabled: {tool_name}",
                verified=False,
                status=ActionStatus.FAILED
            )

        # ----------------------------------------------------
        # Execute
        # ----------------------------------------------------

        action.status = ActionStatus.EXECUTING

        try:

            raw_result = self.registry.execute(
                tool_name,
                action.parameters
            )

        except Exception as error:

            action.status = ActionStatus.FAILED

            return ActionResult(
                success=False,
                message=(
                    f"Tool execution failed: {error}"
                ),
                verified=False,
                status=ActionStatus.FAILED
            )

        # ----------------------------------------------------
        # Basic result normalization
        # ----------------------------------------------------

        if isinstance(raw_result, dict):

            success = bool(
                raw_result.get("success", True)
            )

            message = str(
                raw_result.get(
                    "message",
                    "Action completed."
                )
            )

            data = raw_result

        else:

            success = True
            message = str(raw_result)
            data = {
                "result": raw_result
            }

        # ----------------------------------------------------
        # Verification
        # ----------------------------------------------------

        verified = self.verify_result(
            success=success,
            data=data
        )

        if success and verified:

            action.status = ActionStatus.SUCCESS

            return ActionResult(
                success=True,
                message=message,
                data=data,
                verified=True,
                status=ActionStatus.SUCCESS
            )

        action.status = ActionStatus.FAILED

        return ActionResult(
            success=False,
            message=message,
            data=data,
            verified=False,
            status=ActionStatus.FAILED
        )

    # --------------------------------------------------------
    # Verification
    # --------------------------------------------------------

    def verify_result(
        self,
        success: bool,
        data: dict
    ) -> bool:

        """
        Basic verification layer.

        Real device tools will eventually provide stronger
        verification signals.

        For example:

        Open YouTube
            ↓
        Verify package/activity is actually running.
        """

        return success
