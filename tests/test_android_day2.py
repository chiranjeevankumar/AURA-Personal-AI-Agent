"""
AURA Day-2 Android foundation tests.

These tests intentionally run without requiring a physical
Android device or ADB installation.
"""

from brain.agent_models import UserRequest
from brain.intent_router import IntentRouter

from backend.android.bridge import AndroidBridge
from backend.android.policy import is_allowed
from backend.android.tools import AndroidToolAdapter


def test_bridge_dry_run():

    bridge = AndroidBridge(
        dry_run=True
    )

    result = bridge.devices()

    assert result.success
    assert result.data["dry_run"] is True


def test_open_app_dry_run():

    bridge = AndroidBridge(
        dry_run=True
    )

    result = bridge.open_app(
        "com.google.android.youtube"
    )

    assert result.success
    assert result.data["dry_run"] is True


def test_android_policy():

    assert is_allowed(
        "device.list"
    )

    assert is_allowed(
        "device.info"
    )

    assert is_allowed(
        "app.open"
    )

    assert not is_allowed(
        "security.bypass"
    )


def test_tool_adapter():

    adapter = AndroidToolAdapter(
        AndroidBridge(
            dry_run=True
        )
    )

    result = adapter.execute(
        "app.open",
        {
            "package_name":
                "com.google.android.youtube"
        }
    )

    assert result["success"] is True


def test_tool_adapter_blocks_unknown_operation():

    adapter = AndroidToolAdapter(
        AndroidBridge(
            dry_run=True
        )
    )

    result = adapter.execute(
        "device.root"
    )

    assert result["success"] is False


def test_existing_aura_intent_router():

    router = IntentRouter()

    request = UserRequest(
        text="open youtube"
    )

    intent = router.route(
        request
    )

    assert intent.name == "open_application"
