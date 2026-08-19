"""
AURA Android service facade.

Provides one stable interface for the AURA core while the real
Android implementation is developed.
"""

from typing import Optional

from .app_model import AndroidAppRequest, AndroidAppResult
from .runtime import AndroidRuntime, ColabAndroidRuntime


class AndroidService:
    def __init__(
        self,
        runtime: Optional[AndroidRuntime] = None,
    ):
        self.runtime = runtime or ColabAndroidRuntime()

    def open_application(
        self,
        application: str,
    ) -> AndroidAppResult:

        request = AndroidAppRequest(
            application=application
        )

        return self.runtime.open_application(request)
