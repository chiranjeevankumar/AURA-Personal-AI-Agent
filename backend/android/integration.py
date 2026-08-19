"""
AURA Android integration layer.

This layer keeps Android-specific execution separate from the
reasoning/planning system.
"""

from .service import AndroidService


class AndroidIntegration:
    def __init__(self, service=None):
        self.service = service or AndroidService()

    def open_app(self, application: str):
        return self.service.open_application(application)
