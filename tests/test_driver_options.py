import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acp_amp.driver.python_sdk import (
    apply_private_visibility,
    format_driver_error,
    option_attempts,
)


def test_option_attempts_always_request_private_visibility():
    attempts = option_attempts({"cwd": "/tmp"})
    assert attempts[0]["visibility"] == "private"
    assert attempts[0]["cwd"] == "/tmp"
    assert attempts
    assert all(attempt.get("visibility") == "private" for attempt in attempts)


def test_apply_private_visibility_overrides_workspace_default():
    class Options:
        def __init__(self, visibility: str = "workspace") -> None:
            self.visibility = visibility

        def model_copy(self, update: dict | None = None) -> "Options":
            copied = Options(self.visibility)
            if update and "visibility" in update:
                copied.visibility = update["visibility"]
            return copied

    fixed = apply_private_visibility(Options())
    assert fixed.visibility == "private"


def test_driver_builds_private_thread_options():
    pytest.importorskip("amp_sdk")
    from acp_amp.driver.python_sdk import PythonAmpDriver
    from amp_sdk.core import _build_cli_args

    options = PythonAmpDriver()._build_options(
        cwd="/tmp",
        allow_all=False,
        mcp_config=None,
        thread_id=None,
    )
    assert options.visibility == "private"
    args = _build_cli_args(options)
    assert args[args.index("--visibility") + 1] == "private"
    assert "workspace" not in args


def test_format_driver_error_includes_cli_stderr():
    class ProcessError(Exception):
        def __init__(self):
            super().__init__("Process exited with code 1")
            self.stderr = "Error: Invalid visibility. Must be one of: private, unlisted"

    message = format_driver_error(ProcessError())
    assert "Process exited with code 1" in message
    assert "Invalid visibility" in message
