"""
AURA Android runtime interface.

Colab implementation is deliberately dry-run only.
The real Android implementation will live inside the Android app.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from .app_model import AndroidAppRequest, AndroidAppResult


class AndroidRuntime(ABC):
    """Interface implemented by the real Android application."""

    @abstractmethod
    def open_application(
        self,
        request: AndroidAppRequest
    ) -> AndroidAppResult:
        raise NotImplementedError


class ColabAndroidRuntime(AndroidRuntime):
    """
    Safe runtime used during development in Google Colab.

    It does not claim to control an Android device.
    """

    def open_application(
        self,
        request: AndroidAppRequest
    ) -> AndroidAppResult:

        application = request.application.strip()

        if not application:
            return AndroidAppResult(
                success=False,
                message="Application name is required.",
                application=application,
                dry_run=True,
            )

        return AndroidAppResult(
            success=True,
            message=(
                f"Android application request prepared for "
                f"'{application}' (Colab dry-run)."
            ),
            application=application,
            dry_run=True,
            data={
                "operation": "open_application",
                "application": application,
            },
        )
