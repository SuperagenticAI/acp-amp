from __future__ import annotations

from typing import Any, Iterable

from acp.helpers import (
    image_block,
    text_block,
    tool_content,
    update_agent_message,
    update_agent_thought_text,
    update_user_message,
    start_tool_call,
    update_tool_call,
)


def amp_event_to_updates(event: dict[str, Any]) -> list[Any]:
    """Convert a single Amp SDK event into ACP session updates."""
    updates: list[Any] = []

    if event.get("type") == "result" and event.get("is_error"):
        error_text = str(event.get("error", "Unknown error"))
        updates.append(update_agent_message(text_block(f"Error: {error_text}")))
        return updates

    content = event.get("message", {}).get("content")
    if isinstance(content, str):
        updates.extend(_message_to_updates(event, [content]))
        return updates

    if isinstance(content, list):
        updates.extend(_message_to_updates(event, content))

    return updates


def _message_to_updates(event: dict[str, Any], content: Iterable[Any]) -> list[Any]:
    updates: list[Any] = []
    role = event.get("type")
    for chunk in content:
        if isinstance(chunk, str):
            updates.append(_text_update(role, chunk))
            continue

        chunk_type = chunk.get("type")
        if chunk_type == "text":
            updates.append(_text_update(role, chunk.get("text", "")))
            continue

        if chunk_type == "thinking":
            updates.append(update_agent_thought_text(chunk.get("thinking", "")))
            continue

        if chunk_type == "image":
            source = chunk.get("source", {})
            if source.get("type") == "base64":
                updates.append(
                    update_agent_message(
                        image_block(
                            data=source.get("data", ""),
                            mime_type=source.get("media_type", "application/octet-stream"),
                            uri=None,
                        )
                    )
                )
            elif source.get("type") == "url":
                updates.append(
                    update_agent_message(
                        image_block(
                            data="",
                            mime_type="",
                            uri=source.get("url"),
                        )
                    )
                )
            continue

        if chunk_type == "tool_use":
            updates.append(
                start_tool_call(
                    tool_call_id=chunk.get("id", ""),
                    title=chunk.get("name") or "Tool",
                    kind="other",
                    status="pending",
                    raw_input=_safe_json(chunk.get("input")),
                )
            )
            continue

        if chunk_type == "tool_result":
            updates.append(
                update_tool_call(
                    tool_call_id=chunk.get("tool_use_id", ""),
                    status="failed" if chunk.get("is_error") else "completed",
                    content=_tool_result_content(chunk.get("content"), is_error=bool(chunk.get("is_error"))),
                )
            )
            continue

    return updates


def _text_update(role: str | None, text: str) -> Any:
    if role == "assistant":
        return update_agent_message(text_block(text))
    return update_user_message(text_block(text))


def _tool_result_content(content: Any, *, is_error: bool) -> list[Any] | None:
    def wrap(text: str) -> str:
        if not is_error:
            return text
        return f"```\n{text}\n```"
    if isinstance(content, str) and content:
        return [tool_content(text_block(wrap(content)))]
    if isinstance(content, list) and content:
        blocks: list[Any] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                blocks.append(tool_content(text_block(wrap(item.get("text", "")))))
        return blocks if blocks else None
    return None


def _safe_json(value: Any) -> Any:
    try:
        return jsonable(value)
    except Exception:
        return None


def jsonable(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    return str(value)
