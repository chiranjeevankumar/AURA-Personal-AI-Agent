"""
AURA Android tool adapter.

This layer translates AURA tool calls into AndroidBridge operations.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .bridge import AndroidBridge
from .policy import is_allowed


class AndroidToolAdapter:

    def __init__(
        self,
        bridge: Optional[AndroidBridge] = None,
    ) -> None:

        self.bridge = (
            bridge
            if bridge is not None
            else AndroidBridge(
                dry_run=True
            )
        )

    def execute(
        self,
        operation: str,
        parameters: Optional[Dict[str, Any]] = None,
    ):

        parameters = (
            parameters
            if parameters is not None
            else {}
        )

        if not is_allowed(operation):

            return {
                "success": False,
                "message": (
                    "Android operation is not allowed "
                    "by the Day-2 execution policy."
                ),
                "data": {
                    "operation": operation
                }
            }

        if operation == "device.list":

            return self.bridge.devices().to_dict()

        if operation == "device.info":

            return self.bridge.device_info().to_dict()

        if operation == "app.open":

            package_name = parameters.get(
                "package_name"
            )

            if not package_name:

                return {
                    "success": False,
                    "message": (
                        "package_name is required."
                    ),
                    "data": {}
                }

            return self.bridge.open_app(
                package_name
            ).to_dict()

        return {
            "success": False,
            "message": (
                "Unknown Android operation."
            ),
            "data": {
                "operation": operation
            }
        }
