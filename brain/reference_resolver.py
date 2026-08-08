
"""
AURA Reference Resolver

Resolves simple conversational references using
AURA's short-term conversation context.

Examples:
    "the first result"
    "the second result"
    "the last result"
    "that app"
    "that search"
    "the previous result"
"""

from dataclasses import dataclass
from typing import Any, Optional
import re

from memory.context_manager import ConversationContext


@dataclass
class ReferenceResult:
    """Result of reference resolution."""

    resolved: bool

    reference_type: Optional[str] = None

    index: Optional[int] = None

    value: Any = None

    source: Optional[str] = None

    reason: str = ""


class ReferenceResolver:
    """
    Converts supported conversational references
    into structured references.
    """

    ORDINALS = {
        "first": 0,
        "1st": 0,

        "second": 1,
        "2nd": 1,

        "third": 2,
        "3rd": 2,

        "fourth": 3,
        "4th": 3,

        "fifth": 4,
        "5th": 4,
    }

    def __init__(
        self,
        context: ConversationContext
    ):
        self.context = context

    def resolve(
        self,
        text: str
    ) -> ReferenceResult:

        normalized = text.strip().lower()

        # ----------------------------------------------------
        # ORDINAL RESULT
        # ----------------------------------------------------

        match = re.search(
            r"\bthe\s+(first|second|third|fourth|fifth|"
            r"1st|2nd|3rd|4th|5th)"
            r"\s+result\b",
            normalized
        )

        if match:

            word = match.group(1)

            return ReferenceResult(
                resolved=True,
                reference_type="result",
                index=self.ORDINALS[word],
                source="conversation",
                reason=f"Resolved ordinal result: {word}"
            )

        # ----------------------------------------------------
        # LAST RESULT
        # ----------------------------------------------------

        if re.search(
            r"\bthe\s+last\s+result\b",
            normalized
        ):

            return ReferenceResult(
                resolved=True,
                reference_type="result",
                index=-1,
                source="conversation",
                reason="Resolved last result."
            )

        # ----------------------------------------------------
        # PREVIOUS RESULT
        # ----------------------------------------------------

        if re.search(
            r"\bthe\s+previous\s+result\b",
            normalized
        ):

            return ReferenceResult(
                resolved=True,
                reference_type="result",
                index=-1,
                source="conversation",
                reason="Resolved previous result."
            )

        # ----------------------------------------------------
        # THAT APP
        # ----------------------------------------------------

        if re.search(
            r"\bthat\s+app\b",
            normalized
        ):

            application = self._find_previous_app()

            if application is not None:

                return ReferenceResult(
                    resolved=True,
                    reference_type="application",
                    value=application,
                    source="conversation",
                    reason="Resolved previous application."
                )

            return ReferenceResult(
                resolved=False,
                reference_type="application",
                source="conversation",
                reason="No previous application found."
            )

        # ----------------------------------------------------
        # THAT SEARCH
        # ----------------------------------------------------

        if re.search(
            r"\bthat\s+search\b",
            normalized
        ):

            query = self._find_previous_search()

            if query is not None:

                return ReferenceResult(
                    resolved=True,
                    reference_type="search",
                    value=query,
                    source="conversation",
                    reason="Resolved previous search."
                )

            return ReferenceResult(
                resolved=False,
                reference_type="search",
                source="conversation",
                reason="No previous search found."
            )

        # ----------------------------------------------------
        # NO SUPPORTED REFERENCE
        # ----------------------------------------------------

        return ReferenceResult(
            resolved=False,
            reason="No supported reference detected."
        )

    def _find_previous_app(self):

        for item in reversed(
            self.context.recent()
        ):

            parameters = item.data.get(
                "parameters",
                {}
            )

            application = parameters.get(
                "application"
            )

            if application:
                return application

        return None

    def _find_previous_search(self):

        for item in reversed(
            self.context.recent()
        ):

            parameters = item.data.get(
                "parameters",
                {}
            )

            query = parameters.get(
                "query"
            )

            if query:
                return query

        return None
