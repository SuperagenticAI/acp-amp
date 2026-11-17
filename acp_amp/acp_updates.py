"""Session-update builders that do not depend on ``acp.helpers``.

``agent-client-protocol`` 1.0 removed ``acp.helpers``. These builders construct
the same schema models the old helpers returned, and they work on 0.7+ and 1.0.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

from acp.schema import (
    AgentMessageChunk,
    AgentThoughtChunk,
    AvailableCommandsUpdate,
    ContentToolCallContent,
    ImageContentBlock,
    TextContentBlock,
    ToolCallProgress,
    ToolCallStart,
    UserMessageChunk,
)


def text_block(text: str) -> TextContentBlock:
    return TextContentBlock(type="text", text=text)


def image_block(data: str, mime_type: str, *, uri: str | None = None) -> ImageContentBlock:
    return ImageContentBlock(type="image", data=data, mime_type=mime_type, uri=uri)


def tool_content(block: TextContentBlock | ImageContentBlock) -> ContentToolCallContent:
    return ContentToolCallContent(type="content", content=block)


def update_user_message(content: TextContentBlock | ImageContentBlock) -> UserMessageChunk:
    return UserMessageChunk(session_update="user_message_chunk", content=content)


def update_agent_message(content: TextContentBlock | ImageContentBlock) -> AgentMessageChunk:
    return AgentMessageChunk(session_update="agent_message_chunk", content=content)


def update_agent_thought_text(text: str) -> AgentThoughtChunk:
    return AgentThoughtChunk(session_update="agent_thought_chunk", content=text_block(text))


def update_available_commands(commands: Iterable[Any]) -> AvailableCommandsUpdate:
    return AvailableCommandsUpdate(
        session_update="available_commands_update",
        available_commands=list(commands),
    )


def start_tool_call(
    tool_call_id: str,
    title: str,
    *,
    kind: str | None = None,
    status: str | None = None,
    content: Sequence[Any] | None = None,
    raw_input: Any | None = None,
) -> ToolCallStart:
    return ToolCallStart(
        session_update="tool_call",
        tool_call_id=tool_call_id,
        title=title,
        kind=kind,
        status=status,
        content=list(content) if content is not None else None,
        raw_input=raw_input,
    )


def update_tool_call(
    tool_call_id: str,
    *,
    status: str | None = None,
    content: Sequence[Any] | None = None,
) -> ToolCallProgress:
    return ToolCallProgress(
        session_update="tool_call_update",
        tool_call_id=tool_call_id,
        status=status,
        content=list(content) if content is not None else None,
    )
