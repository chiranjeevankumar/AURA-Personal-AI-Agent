"""
AURA built-in tool registration.
"""

from tools.registry import (
    ToolDefinition,
    ToolRegistry,
)

from backend.android.apps import open_app


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

    return registry
