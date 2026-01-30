import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acp_amp.mapping.to_amp import prompt_to_text
from acp.schema import (
    EmbeddedResourceContentBlock,
    TextContentBlock,
    TextResourceContents,
)


def test_prompt_to_text_plain_text():
    prompt = [TextContentBlock(type="text", text="hello")]
    assert prompt_to_text(prompt) == "hello"


def test_prompt_to_text_init_command_expands():
    prompt = [TextContentBlock(type="text", text="/init")]
    result = prompt_to_text(prompt)
    assert "AGENTS.md" in result
    assert "Analyze this codebase" in result or "Please analyze this codebase" in result


def test_prompt_to_text_embedded_resource():
    resource = TextResourceContents(uri="file:///tmp/a.txt", text="context")
    prompt = [EmbeddedResourceContentBlock(type="resource", resource=resource)]
    result = prompt_to_text(prompt)
    assert "embedded context" in result
    assert "context" in result
