"""Allowlisted application launcher used only after explicit approval."""

from __future__ import annotations

import platform
import subprocess


ALLOWED_APPLICATIONS = {
    "notepad": {
        "windows": ["notepad.exe"],
    },
    "calculator": {
        "windows": ["calc.exe"],
    },
    "explorer": {
        "windows": ["explorer.exe"],
    },
}


def open_application(application: str) -> dict[str, str]:
    """Launch one fixed application name. Arbitrary commands and paths are rejected."""
    name = application.casefold().strip()
    if name not in ALLOWED_APPLICATIONS:
        raise ValueError("application is not allowlisted")
    if platform.system() != "Windows":
        raise RuntimeError("allowlisted application launch is currently supported on Windows only")
    subprocess.Popen(ALLOWED_APPLICATIONS[name]["windows"], close_fds=True)
    return {"application": name, "status": "started"}
