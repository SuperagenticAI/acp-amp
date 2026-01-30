import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acp_amp.mapping.to_acp import amp_event_to_updates
from acp.schema import (
    AgentMessageChunk,
    AgentThoughtChunk,
    ToolCallProgress,
    ToolCallStart,
    UserMessageChunk,
)


def _find_type(updates, cls):
    return [u for u in updates if isinstance(u, cls)]


def test_amp_text_message_to_agent_chunk():
    event = {"type": "assistant", "message": {"content": "hello"}}
    updates = amp_event_to_updates(event)
    chunks = _find_type(updates, AgentMessageChunk)
    assert chunks
    assert chunks[0].content.text == "hello"


def test_amp_thinking_to_thought_chunk():
    event = {
        "type": "assistant",
        "message": {"content": [{"type": "thinking", "thinking": "hmm"}]},
    }
    updates = amp_event_to_updates(event)
    chunks = _find_type(updates, AgentThoughtChunk)
    assert chunks
    assert chunks[0].content.text == "hmm"


def test_amp_tool_use_to_tool_call_start():
    event = {
        "type": "assistant",
        "message": {
            "content": [
                {"type": "tool_use", "id": "t1", "name": "Tool", "input": {"a": 1}}
            ]
        },
    }
    updates = amp_event_to_updates(event)
    starts = _find_type(updates, ToolCallStart)
    assert starts
    assert starts[0].tool_call_id == "t1"
    assert starts[0].status == "pending"


def test_amp_tool_result_to_tool_call_update():
    event = {
        "type": "assistant",
        "message": {
            "content": [
                {"type": "tool_result", "tool_use_id": "t1", "is_error": False, "content": "ok"}
            ]
        },
    }
    updates = amp_event_to_updates(event)
    updates_tc = _find_type(updates, ToolCallProgress)
    assert updates_tc
    assert updates_tc[0].tool_call_id == "t1"
    assert updates_tc[0].status == "completed"


def test_amp_user_text_maps_to_user_chunk():
    event = {"type": "user", "message": {"content": [{"type": "text", "text": "hi"}]}}
    updates = amp_event_to_updates(event)
    chunks = _find_type(updates, UserMessageChunk)
    assert chunks
    assert chunks[0].content.text == "hi"


def test_amp_error_result_maps_to_agent_message():
    event = {"type": "result", "is_error": True, "error": "boom"}
    updates = amp_event_to_updates(event)
    chunks = _find_type(updates, AgentMessageChunk)
    assert chunks
    assert "Error:" in chunks[0].content.text
