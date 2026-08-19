"""
AURA Android Bridge
===================

Provides a safe abstraction between AURA's Python core and Android.

The bridge supports:

    - ADB discovery
    - device information
    - shell execution
    - application launching
    - dry-run mode

The bridge does NOT bypass Android security.

A physical Android device must be connected through ADB before
real commands can execute.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
import shutil
import subprocess


@dataclass
class AndroidResult:
    """Result returned by AndroidBridge operations."""

    success: bool
    message: str
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AndroidBridge:
    """
    Safe Android execution abstraction.

    By default the bridge operates in dry-run mode when requested.
    Real execution requires adb to be installed and a device to be
    available.
    """

    def __init__(
        self,
        adb_path: Optional[str] = None,
        device_id: Optional[str] = None,
        dry_run: bool = False,
        timeout: int = 15,
    ) -> None:

        self.timeout = timeout
        self.device_id = device_id
        self.dry_run = dry_run

        self.adb_path = (
            adb_path
            or shutil.which("adb")
            or "adb"
        )

    # --------------------------------------------------------------
    # ADB availability
    # --------------------------------------------------------------

    def adb_available(self) -> bool:
        """Return whether adb is available."""

        if self.dry_run:
            return True

        return shutil.which(
            self.adb_path
        ) is not None

    # --------------------------------------------------------------
    # Internal command runner
    # --------------------------------------------------------------

    def _command(
        self,
        args: List[str],
    ) -> AndroidResult:

        command = [
            self.adb_path
        ]

        if self.device_id:
            command.extend(
                [
                    "-s",
                    self.device_id
                ]
            )

        command.extend(args)

        if self.dry_run:

            return AndroidResult(
                success=True,
                message=(
                    "Dry-run Android command prepared."
                ),
                data={
                    "command": command,
                    "dry_run": True,
                }
            )

        if not self.adb_available():

            return AndroidResult(
                success=False,
                message=(
                    "ADB is not installed or not available."
                ),
                data={
                    "command": command,
                    "dry_run": False,
                }
            )

        try:

            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            stdout = (
                completed.stdout or ""
            ).strip()

            stderr = (
                completed.stderr or ""
            ).strip()

            success = (
                completed.returncode == 0
            )

            return AndroidResult(
                success=success,
                message=(
                    stdout
                    if success and stdout
                    else (
                        stderr
                        if stderr
                        else (
                            "Android command completed."
                            if success
                            else "Android command failed."
                        )
                    )
                ),
                data={
                    "command": command,
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": completed.returncode,
                    "dry_run": False,
                }
            )

        except subprocess.TimeoutExpired:

            return AndroidResult(
                success=False,
                message=(
                    "Android command timed out."
                ),
                data={
                    "command": command,
                    "timeout": self.timeout,
                }
            )

        except Exception as error:

            return AndroidResult(
                success=False,
                message=(
                    f"Android command error: {error}"
                ),
                data={
                    "command": command,
                    "error": str(error),
                }
            )

    # --------------------------------------------------------------
    # Device discovery
    # --------------------------------------------------------------

    def devices(self) -> AndroidResult:
        """Return connected Android devices."""

        result = self._command(
            ["devices"]
        )

        if not result.success:
            return result

        if result.data.get("dry_run"):

            return AndroidResult(
                success=True,
                message="Dry-run device discovery.",
                data={
                    "devices": [],
                    "dry_run": True,
                }
            )

        devices = []

        stdout = result.data.get(
            "stdout",
            ""
        )

        for line in stdout.splitlines():

            line = line.strip()

            if (
                not line
                or line.startswith("List of devices")
            ):
                continue

            parts = line.split()

            if len(parts) >= 2:

                devices.append(
                    {
                        "id": parts[0],
                        "state": parts[1],
                    }
                )

        return AndroidResult(
            success=True,
            message=(
                f"Found {len(devices)} Android device(s)."
            ),
            data={
                "devices": devices,
                "dry_run": False,
            }
        )

    # --------------------------------------------------------------
    # Device information
    # --------------------------------------------------------------

    def device_info(self) -> AndroidResult:
        """Return basic Android device properties."""

        properties = {}

        for prop in (
            "ro.product.manufacturer",
            "ro.product.model",
            "ro.build.version.release",
            "ro.build.version.sdk",
        ):

            result = self._command(
                [
                    "shell",
                    "getprop",
                    prop
                ]
            )

            if not result.success:
                return result

            if result.data.get("dry_run"):

                properties[prop] = "<dry-run>"

            else:

                properties[prop] = (
                    result.data
                    .get("stdout", "")
                    .strip()
                )

        return AndroidResult(
            success=True,
            message="Android device information retrieved.",
            data={
                "properties": properties
            }
        )

    # --------------------------------------------------------------
    # Shell
    # --------------------------------------------------------------

    def shell(
        self,
        command: str,
    ) -> AndroidResult:
        """
        Execute a normal Android shell command.

        This method does not bypass Android permissions.
        """

        if not isinstance(command, str):
            return AndroidResult(
                success=False,
                message="Shell command must be a string.",
                data={}
            )

        command = command.strip()

        if not command:
            return AndroidResult(
                success=False,
                message="Shell command cannot be empty.",
                data={}
            )

        return self._command(
            [
                "shell",
                command
            ]
        )

    # --------------------------------------------------------------
    # Launch application
    # --------------------------------------------------------------

    def open_app(
        self,
        package_name: str,
    ) -> AndroidResult:
        """
        Launch an Android application by package name.

        The caller is responsible for selecting a valid package.
        """

        if not isinstance(package_name, str):
            return AndroidResult(
                success=False,
                message="Package name must be a string.",
                data={}
            )

        package_name = package_name.strip()

        if not package_name:
            return AndroidResult(
                success=False,
                message="Package name cannot be empty.",
                data={}
            )

        return self._command(
            [
                "shell",
                "monkey",
                "-p",
                package_name,
                "-c",
                "android.intent.category.LAUNCHER",
                "1",
            ]
        )

    # --------------------------------------------------------------
    # Generic activity launch
    # --------------------------------------------------------------

    def launch(
        self,
        component: str,
    ) -> AndroidResult:
        """Launch an explicitly specified Android component."""

        if not component:
            return AndroidResult(
                success=False,
                message="Component cannot be empty.",
                data={}
            )

        return self._command(
            [
                "shell",
                "am",
                "start",
                "-n",
                component,
            ]
        )
