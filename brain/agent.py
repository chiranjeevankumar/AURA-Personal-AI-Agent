
"""
AURA Personal Agent

The central orchestrator connecting:

    User Request
          ↓
    Intent Router
          ↓
    Planner
          ↓
    Safety Engine
          ↓
    Tool Registry
          ↓
    Executor
          ↓
    Response

This class provides the main interface:

    aura.run("Open YouTube")
"""


from brain.agent_models import (
    UserRequest,
    AgentResponse,
    ActionStatus
)

from brain.intent_router import IntentRouter
from brain.planner import AgentPlanner
from brain.safety import SafetyEngine
from brain.executor import AgentExecutor

from tools.registry import ToolRegistry


class AURAAgent:

    def __init__(
        self,
        registry: ToolRegistry
    ):

        self.registry = registry

        self.router = IntentRouter()

        self.planner = AgentPlanner()

        self.safety = SafetyEngine()

        self.executor = AgentExecutor(
            registry=self.registry,
            safety_engine=self.safety
        )

    # ========================================================
    # MAIN ENTRY POINT
    # ========================================================

    def run(
        self,
        text: str,
        confirmed: bool = False
    ) -> AgentResponse:

        # ----------------------------------------------------
        # 1. Create request
        # ----------------------------------------------------

        request = UserRequest(
            text=text
        )

        # ----------------------------------------------------
        # 2. Understand request
        # ----------------------------------------------------

        intent = self.router.route(
            request
        )

        # ----------------------------------------------------
        # 3. Create plan
        # ----------------------------------------------------

        plan = self.planner.create_plan(
            request=request,
            intent=intent
        )

        # ----------------------------------------------------
        # 4. Unknown request
        # ----------------------------------------------------

        if intent.name == "unknown":

            return AgentResponse(
                message=(
                    "I don't understand that instruction yet."
                ),
                success=False,
                plan=plan,
                results=[]
            )

        # ----------------------------------------------------
        # 5. No actions
        # ----------------------------------------------------

        if not plan.actions:

            return AgentResponse(
                message=(
                    "I understood the request, "
                    "but there is no available action "
                    "for it yet."
                ),
                success=False,
                plan=plan,
                results=[]
            )

        # ----------------------------------------------------
        # 6. Execute
        # ----------------------------------------------------

        results = self.executor.execute_plan(
            plan,
            user_confirmed=confirmed
        )

        # ----------------------------------------------------
        # 7. Analyze results
        # ----------------------------------------------------

        if not results:

            return AgentResponse(
                message="No action was executed.",
                success=False,
                plan=plan,
                results=[]
            )

        last_result = results[-1]

        # ----------------------------------------------------
        # Confirmation required
        # ----------------------------------------------------

        if (
            last_result.status
            == ActionStatus.WAITING_CONFIRMATION
        ):

            return AgentResponse(
                message=(
                    "This action requires your confirmation "
                    "before I can continue."
                ),
                success=False,
                plan=plan,
                results=results
            )

        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        if last_result.success:

            return AgentResponse(
                message=last_result.message,
                success=True,
                plan=plan,
                results=results
            )

        # ----------------------------------------------------
        # Failure
        # ----------------------------------------------------

        return AgentResponse(
            message=last_result.message,
            success=False,
            plan=plan,
            results=results
        )
