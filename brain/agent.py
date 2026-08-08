
"""
AURA Personal Agent

Central orchestration layer.

Now includes Memory Manager.
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

from memory.manager import MemoryManager

from tools.registry import ToolRegistry


class AURAAgent:

    def __init__(
        self,
        registry: ToolRegistry,
        memory_manager: MemoryManager = None,
        safety_engine: SafetyEngine = None
    ):

        self.registry = registry

        self.router = IntentRouter()

        self.planner = AgentPlanner()

        self.safety = (
            safety_engine
            if safety_engine is not None
            else SafetyEngine()
        )

        self.executor = AgentExecutor(
            registry=self.registry,
            safety_engine=self.safety
        )

        self.memory = (
            memory_manager
            if memory_manager is not None
            else MemoryManager()
        )

    # ========================================================
    # MAIN ENTRY POINT
    # ========================================================

    def run(
        self,
        text: str,
        confirmed: bool = False
    ) -> AgentResponse:

        request = UserRequest(
            text=text
        )

        # ----------------------------------------------------
        # Remember current request
        # ----------------------------------------------------

        self.memory.remember_recent(
            text,
            metadata={
                "type": "user_request"
            }
        )

        # ----------------------------------------------------
        # Understand
        # ----------------------------------------------------

        intent = self.router.route(
            request
        )

        # ----------------------------------------------------
        # Direct memory recall
        # ----------------------------------------------------

        if intent.name == "recall":

            query = intent.parameters.get(
                "query",
                ""
            )

            memories = self.memory.recall(
                query
            )

            if not memories:

                message = (
                    "I don't have any stored memory "
                    "matching that."
                )

            else:

                message = (
                    "I remember: "
                    + " | ".join(
                        item.content
                        for item in memories
                    )
                )

            return AgentResponse(
                message=message,
                success=True,
                plan=None,
                results=[]
            )

        # ----------------------------------------------------
        # Create plan
        # ----------------------------------------------------

        plan = self.planner.create_plan(
            request=request,
            intent=intent
        )

        # ----------------------------------------------------
        # Unknown
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
        # Execute
        # ----------------------------------------------------

        results = self.executor.execute_plan(
            plan,
            user_confirmed=confirmed
        )

        # ----------------------------------------------------
        # Handle no result
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
        # Memory save result
        # ----------------------------------------------------

        if (
            intent.name == "remember"
            and last_result.success
        ):

            memory_text = intent.parameters.get(
                "memory",
                ""
            )

            self.memory.remember_recent(
                f"Saved memory: {memory_text}",
                metadata={
                    "type": "memory_saved"
                }
            )

            return AgentResponse(
                message=(
                    "I'll remember that: "
                    + memory_text
                ),
                success=True,
                plan=plan,
                results=results
            )

        # ----------------------------------------------------
        # Confirmation
        # ----------------------------------------------------

        if (
            last_result.status
            == ActionStatus.WAITING_CONFIRMATION
        ):

            return AgentResponse(
                message=(
                    "This action requires your "
                    "confirmation before I can continue."
                ),
                success=False,
                plan=plan,
                results=results
            )

        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        if last_result.success:

            self.memory.remember_recent(
                last_result.message,
                metadata={
                    "type": "action_result"
                }
            )

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
