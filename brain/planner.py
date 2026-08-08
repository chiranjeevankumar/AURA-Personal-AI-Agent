
"""
AURA Agent Planner

Converts structured intents into executable plans.

IMPORTANT:

The Planner DOES NOT execute tools.

It only decides what actions would be required.

Execution happens later through:

    Safety Engine
          ↓
    Tool Registry
          ↓
       Executor
"""


from brain.agent_models import (
    UserRequest,
    Intent,
    PlannedAction,
    AgentPlan,
    RiskLevel
)


class AgentPlanner:

    def create_plan(
        self,
        request: UserRequest,
        intent: Intent
    ) -> AgentPlan:

        actions = []

        # ====================================================
        # OPEN APPLICATION
        # ====================================================

        if intent.name == "open_application":

            application = intent.parameters.get(
                "application"
            )

            if application:

                actions.append(
                    PlannedAction(
                        tool="android.open_app",

                        action="open_app",

                        parameters={
                            "application": application
                        },

                        risk=RiskLevel.SAFE,

                        requires_confirmation=False
                    )
                )


        # ====================================================
        # WEB SEARCH
        # ====================================================

        elif intent.name == "web_search":

            query = intent.parameters.get(
                "query"
            )

            if query:

                actions.append(
                    PlannedAction(
                        tool="web.search",

                        action="search",

                        parameters={
                            "query": query
                        },

                        risk=RiskLevel.SAFE,

                        requires_confirmation=False
                    )
                )


        # ====================================================
        # WHATSAPP MESSAGE
        # ====================================================

        elif intent.name == "send_message":

            platform = intent.parameters.get(
                "platform"
            )

            recipient = intent.parameters.get(
                "recipient"
            )

            message = intent.parameters.get(
                "message"
            )

            if platform == "whatsapp":

                actions.append(
                    PlannedAction(
                        tool="communication.whatsapp.send",

                        action="send",

                        parameters={
                            "recipient": recipient,
                            "message": message
                        },

                        risk=RiskLevel.EXTERNAL_COMMUNICATION,

                        requires_confirmation=True
                    )
                )


        # ====================================================
        # EMAIL
        # ====================================================

        elif intent.name == "send_email":

            recipient = intent.parameters.get(
                "recipient"
            )

            message = intent.parameters.get(
                "message"
            )

            actions.append(
                PlannedAction(
                    tool="communication.email.send",

                    action="send",

                    parameters={
                        "recipient": recipient,
                        "message": message
                    },

                    risk=RiskLevel.EXTERNAL_COMMUNICATION,

                    requires_confirmation=True
                )
            )


        # ====================================================
        # MEMORY
        # ====================================================

        elif intent.name == "remember":

            memory = intent.parameters.get(
                "memory"
            )

            actions.append(
                PlannedAction(
                    tool="memory.remember",

                    action="remember",

                    parameters={
                        "memory": memory
                    },

                    risk=RiskLevel.SAFE,

                    requires_confirmation=False
                )
            )


        # ====================================================
        # UNKNOWN
        # ====================================================

        elif intent.name == "unknown":

            # No action is created.

            actions = []


        # ====================================================
        # RETURN PLAN
        # ====================================================

        return AgentPlan(
            request=request,
            intent=intent,
            actions=actions
        )
