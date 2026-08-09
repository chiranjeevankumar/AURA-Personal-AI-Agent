"""
Android application operations for AURA.
"""

from typing import Dict


# Common Android application aliases.
APPLICATION_PACKAGES = {
    "youtube": "com.google.android.youtube",
    "youtube music": "com.google.android.apps.youtube.music",
    "gmail": "com.google.android.gm",
    "chrome": "com.android.chrome",
    "whatsapp": "com.whatsapp",
}


def resolve_package(application: str) -> str:
    """
    Resolve an application name or package name.
    """

    value = str(application).strip()

    if not value:
        raise ValueError(
            "Application name cannot be empty."
        )

    return APPLICATION_PACKAGES.get(
        value.lower(),
        value
    )


def open_app(application: str) -> Dict:
    """
    Open an Android application.

    The actual Android runtime is supplied by the device
    integration layer. Google Colab does not provide that
    runtime, so this function reports that condition rather
    than pretending the application was opened.
    """

    package = resolve_package(application)

    return {
        "success": False,
        "message": (
            "Android runtime is not available "
            "in the current environment."
        ),
        "error": "android_runtime_unavailable",
        "application": application,
        "package": package,
    }
