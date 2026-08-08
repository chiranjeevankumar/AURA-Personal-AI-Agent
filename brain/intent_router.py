
"""
AURA Intent Router v1.2

Adds local memory recall capability.
"""

import re

from brain.agent_models import (
    UserRequest,
    Intent,
    RiskLevel
)


class IntentRouter:

    def route(
        self,
        request: UserRequest
    ) -> Intent:

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
        # RECALL
        # ====================================================

        # IMPORTANT:
        # Check recall BEFORE remember.
        #
        # Example:
        # "What do you remember about my project?"
        # must become RECALL, not REMEMBER.

        recall_patterns = [
            r"\bwhat\s+do\s+you\s+remember\s+about\s+(.+)",
            r"\bwhat\s+do\s+you\s+know\s+about\s+(.+)",
            r"\brecall\s+(.+)",
            r"\bremember\s+anything\s+about\s+(.+)",
        ]

        for pattern in recall_patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                return Intent(
                    name="recall",
                    confidence=0.95,
                    parameters={
                        "query": match.group(1).strip()
                    },
                    risk=RiskLevel.SAFE
                )

        # ====================================================
        # REMEMBER
        # ====================================================

        remember_patterns = [
            r"^\s*remember\s+that\s+(.+)",
            r"^\s*remember\s+(.+)",
            r"^\s*save\s+this\s+(.+)",
        ]

        for pattern in remember_patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                memory = match.group(1).strip()

                # Do not treat:
                # "remember about X"
                # as a memory to save.

                if memory.startswith("about "):

                    continue

                return Intent(
                    name="remember",
                    confidence=0.95,
                    parameters={
                        "memory": memory
                    },
                    risk=RiskLevel.SAFE
                )

        # ====================================================
        # OPEN APPLICATION
        # ====================================================

        for pattern in [
            r"\bopen\s+(.+)",
            r"\blaunch\s+(.+)",
            r"\bstart\s+(.+)",
        ]:

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

        for pattern in [
            r"\bsearch\s+(?:for\s+)?(.+)",
            r"\blook\s+up\s+(.+)",
            r"\bfind\s+information\s+about\s+(.+)",
        ]:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                return Intent(
                    name="web_search",
                    confidence=0.93,
                    parameters={
                        "query": match.group(1).strip()
                    },
                    risk=RiskLevel.SAFE
                )

        # ====================================================
        # WHATSAPP
        # ====================================================

        whatsapp_pattern = (
            r"(?:send|message)\s+(.+?)"
            r"\s+(?:on\s+)?whatsapp"
            r"\s+(?:saying|that)\s+(.+)"
        )

        match = re.search(
            whatsapp_pattern,
            normalized
        )

        if match:

            return Intent(
                name="send_message",
                confidence=0.92,
                parameters={
                    "platform": "whatsapp",
                    "recipient": match.group(1).strip(),
                    "message": match.group(2).strip()
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

                return Intent(
                    name="send_email",
                    confidence=0.90,
                    parameters={
                        "recipient": match.group(1).strip(),
                        "message": match.group(2).strip()
                    },
                    risk=RiskLevel.EXTERNAL_COMMUNICATION
                )

        # ====================================================
        # UNKNOWN
        # ====================================================

        return Intent(
            name="unknown",
            confidence=0.20,
            parameters={
                "original_text": text
            },
            risk=RiskLevel.SENSITIVE
        )
