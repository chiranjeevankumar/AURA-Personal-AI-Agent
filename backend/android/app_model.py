"""
AURA Android application model.

This module describes Android application requests without pretending
that Google Colab has access to the real Android device.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AndroidAppRequest:
    application: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AndroidAppResult:
    success: bool
    message: str
    application: str
    dry_run: bool = True
    data: Dict[str, Any] = field(default_factory=dict)
