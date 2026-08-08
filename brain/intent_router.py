
"""
AURA Intent Router v1.1

Converts natural-language requests into structured intents.

Important distinction:

RiskLevel describes the risk of an action.

SafetyDecision describes what AURA should do with that action.

They are intentionally separate.
"""

import re

from brain.agent_models import (
    UserRequest,
    Intent,
    RiskLevel
)


class IntentRouter:

    def route(self, request: UserRequest) -> Intent:

        text = request.text.strip()

        if not text:

            return Intent(
                name="unknown",
                confidence=0.0,
                parameters={},
                risk=RiskLevel.BLOCKED
            )

        normalized = text.lower()

        # ====================================================
        # OPEN APPLICATION
        # ====================================================

        open_patterns = [
            r"\bopen\s+(.+)",
            r"\blaunch\s+(.+)",
            r"\bstart\s+(.+)",
        ]

        for pattern in open_patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                application = match.group(1).strip()

                application = re.sub(
                    r"\bplease\b",
                    "",
                    application
                ).strip()

                return Intent(
                    name="open_application",
                    confidence=0.95,
                    parameters={
                        "application": application
                    },
                    risk=RiskLevel.SAFE
                )

        # ====================================================
        # WEB SEARCH
        # ====================================================

        search_patterns = [
            r"\bsearch\s+(?:for\s+)?(.+)",
            r"\blook\s+up\s+(.+)",
            r"\bfind\s+information\s+about\s+(.+)",
        ]

        for pattern in search_patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                query = match.group(1).strip()

                return Intent(
                    name="web_search",
                    confidence=0.93,
                    parameters={
                        "query": query
                    },
                    risk=RiskLevel.SAFE
                )

        # ====================================================
        # WHATSAPP MESSAGE
        # ====================================================

        whatsapp_patterns = [
            r"(?:send|message)\s+(.+?)"
            r"\s+(?:on\s+)?whatsapp"
            r"\s+(?:saying|that)\s+(.+)",

            r"whatsapp\s+(.+?)"
            r"\s+(?:saying|that)\s+(.+)",
        ]

        for pattern in whatsapp_patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                recipient = match.group(1).strip()
                message = match.group(2).strip()

                return Intent(
                    name="send_message",
                    confidence=0.92,
                    parameters={
                        "platform": "whatsapp",
                        "recipient": recipient,
                        "message": message
                    },
                    risk=RiskLevel.EXTERNAL_COMMUNICATION
                )

        # ====================================================
        # EMAIL
        # ====================================================

        if (
            "email" in normalized
            or "e-mail" in normalized
        ):

            match = re.search(
                r"(?:send|write|compose)\s+"
                r"(?:an?\s+)?email\s+to\s+(.+?)"
                r"\s+(?:saying|that|message)\s+(.+)",
                normalized
            )

            if match:

                recipient = match.group(1).strip()
                message = match.group(2).strip()

                return Intent(
                    name="send_email",
                    confidence=0.90,
                    parameters={
                        "recipient": recipient,
                        "message": message
                    },
                    risk=RiskLevel.EXTERNAL_COMMUNICATION
                )

        # ====================================================
        # REMEMBER
        # ====================================================

        remember_patterns = [
            r"\bremember\s+that\s+(.+)",
            r"\bremember\s+(.+)",
            r"\bsave\s+this\s+(.+)",
        ]

        for pattern in remember_patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                memory = match.group(1).strip()

                return Intent(
                    name="remember",
                    confidence=0.95,
                    parameters={
                        "memory": memory
                    },
                    risk=RiskLevel.SAFE
                )

        # ====================================================
        # UNKNOWN
        # ====================================================

        # Unknown does NOT mean "blocked".
        # It simply means AURA does not understand the request yet.
        #
        # The Safety Engine will later decide whether an unknown
        # capability needs permission.

        return Intent(
            name="unknown",
            confidence=0.20,
            parameters={
                "original_text": text
            },
            risk=RiskLevel.SENSITIVE
        )
