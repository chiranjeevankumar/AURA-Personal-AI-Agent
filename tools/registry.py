
"""
AURA Tool Registry

The registry manages every capability available to AURA.

Important:
The registry does NOT execute dangerous actions itself.
It only describes and manages available tools.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolDefinition:
    """
    Description of one capability available to AURA.
    """

    name: str
    description: str
    category: str

    risk_level: str = "safe"

    requires_confirmation: bool = False

    parameters: Dict[str, Any] = field(default_factory=dict)

    handler: Optional[Callable] = None

    enabled: bool = True


class ToolRegistry:
    """
    Central registry containing AURA's available tools.
    """

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    # --------------------------------------------------------
    # Register
    # --------------------------------------------------------

    def register(self, tool: ToolDefinition) -> None:

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    # --------------------------------------------------------
    # Remove
    # --------------------------------------------------------

    def unregister(self, name: str) -> bool:

        if name in self._tools:
            del self._tools[name]
            return True

        return False

    # --------------------------------------------------------
    # Get
    # --------------------------------------------------------

    def get(self, name: str) -> Optional[ToolDefinition]:

        return self._tools.get(name)

    # --------------------------------------------------------
    # Check
    # --------------------------------------------------------

    def has(self, name: str) -> bool:

        return name in self._tools

    # --------------------------------------------------------
    # Enable / Disable
    # --------------------------------------------------------

    def enable(self, name: str) -> bool:

        tool = self.get(name)

        if tool is None:
            return False

        tool.enabled = True
        return True

    def disable(self, name: str) -> bool:

        tool = self.get(name)

        if tool is None:
            return False

        tool.enabled = False
        return True

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    def list_tools(
        self,
        category: Optional[str] = None,
        enabled_only: bool = True
    ) -> List[ToolDefinition]:

        tools = list(self._tools.values())

        if category:
            tools = [
                tool
                for tool in tools
                if tool.category == category
            ]

        if enabled_only:
            tools = [
                tool
                for tool in tools
                if tool.enabled
            ]

        return tools

    # --------------------------------------------------------
    # Categories
    # --------------------------------------------------------

    def categories(self) -> List[str]:

        return sorted(
            set(
                tool.category
                for tool in self._tools.values()
            )
        )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    def execute(
        self,
        name: str,
        parameters: Optional[Dict[str, Any]] = None
    ):

        tool = self.get(name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {name}"
            )

        if not tool.enabled:
            raise RuntimeError(
                f"Tool is disabled: {name}"
            )

        if tool.handler is None:
            raise RuntimeError(
                f"Tool has no handler: {name}"
            )

        parameters = parameters or {}

        return tool.handler(**parameters)
