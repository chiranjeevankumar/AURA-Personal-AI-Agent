"""
AURA Android execution policy.

This module intentionally keeps Android execution conservative.

Allowed foundation operations:
    - device discovery
    - device information
    - application launch

The policy does not grant unrestricted Android control.
"""

from __future__ import annotations

from typing import Dict


SAFE_ANDROID_OPERATIONS: Dict[str, str] = {
    "device.list": "Discover connected Android devices.",
    "device.info": "Read basic Android device information.",
    "app.open": "Open an Android application.",
}


def is_allowed(operation: str) -> bool:
    """Return whether an Android foundation operation is allowed."""

    return operation in SAFE_ANDROID_OPERATIONS


def reason(operation: str) -> str:

    if operation in SAFE_ANDROID_OPERATIONS:
        return SAFE_ANDROID_OPERATIONS[operation]

    return (
        "Android operation is not part of the Day-2 "
        "safe execution foundation."
    )
