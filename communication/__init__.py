"""
Public communication API for AURA.
"""

from communication.whatsapp import send as send_whatsapp_message

from communication.runtime_status import (
    get_runtime_status,
    get_whatsapp_status,
)

from communication.service_registry import (
    list_services,
    get_service_status,
    get_all_service_status,
)

from communication.service_capabilities import (
    get_service_capabilities,
    get_all_service_capabilities,
)

__all__ = [
    "send_whatsapp_message",
    "get_runtime_status",
    "get_whatsapp_status",
    "list_services",
    "get_service_status",
    "get_all_service_status",
    "get_service_capabilities",
    "get_all_service_capabilities",
    "list_operations",
    "get_operation",
    "get_all_operations",
]

from communication.operation_registry import (
    list_operations,
    get_operation,
    get_all_operations,
)
