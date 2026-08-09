"""
AURA built-in tool registration.
"""

from tools.registry import (
    ToolDefinition,
    ToolRegistry,
)

from backend.android.apps import open_app
from backend.web.search import search
from communication.whatsapp import send as whatsapp_send


def register_builtin_tools(
    registry: ToolRegistry
) -> ToolRegistry:
    """
    Register all built-in AURA tools.
    """

    if not registry.has("android.open_app"):

        registry.register(
            ToolDefinition(
                name="android.open_app",
                description="Open an Android application.",
                category="android",
                risk_level="safe",
                requires_confirmation=False,
                parameters={
                    "application": {
                        "type": "string",
                        "required": True,
                        "description": (
                            "Application name or "
                            "Android package name."
                        ),
                    }
                },
                handler=open_app,
            )
        )


    if not registry.has("web.search"):

        registry.register(
            ToolDefinition(
                name="web.search",
                description="Search the web for information.",
                category="web",
                risk_level="safe",
                requires_confirmation=False,
                parameters={
                    "query": {
                        "type": "string",
                        "required": True,
                        "description": "Web search query.",
                    }
                },
                handler=search,
            )
        )

    if not registry.has("communication.whatsapp.send"):

        registry.register(
            ToolDefinition(
                name="communication.whatsapp.send",
                description="Send a WhatsApp message.",
                category="communication",
                risk_level="external_communication",
                requires_confirmation=True,
                parameters={
                    "recipient": {
                        "type": "string",
                        "required": True,
                        "description": "WhatsApp recipient.",
                    },
                    "message": {
                        "type": "string",
                        "required": True,
                        "description": "WhatsApp message text.",
                    },
                },
                handler=whatsapp_send,
            )
        )

    return registry
