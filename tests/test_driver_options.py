import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acp_amp.driver.python_sdk import format_driver_error, option_attempts


def test_option_attempts_request_private_visibility_first():
    attempts = option_attempts({"cwd": "/tmp"})
    assert attempts[0]["visibility"] == "private"
    assert attempts[0]["cwd"] == "/tmp"
    assert all(attempt.get("visibility") == "private" for attempt in attempts[:6])


def test_format_driver_error_includes_cli_stderr():
    class ProcessError(Exception):
        def __init__(self):
            super().__init__("Process exited with code 1")
            self.stderr = "Error: Invalid visibility. Must be one of: private, unlisted"

    message = format_driver_error(ProcessError())
    assert "Process exited with code 1" in message
    assert "Invalid visibility" in message
