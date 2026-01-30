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


def amp_event_to_updates(event: dict[str, Any] | Any) -> list[Any]:
    """Convert a single Amp SDK event into ACP session updates."""
    updates: list[Any] = []
    event = _ensure_dict(_normalize_recursive(event))

    if _safe_get(event, "type") == "result" and _safe_get(event, "is_error"):
        error_text = str(_safe_get(event, "error", "Unknown error"))
        updates.append(update_agent_message(text_block(f"Error: {error_text}")))
        return updates

    message = _ensure_dict(_safe_get(event, "message", {}))
    content = _safe_get(message, "content")
    if isinstance(content, str):
        updates.extend(_message_to_updates(event, [content]))
        return updates

    if isinstance(content, list):
        updates.extend(_message_to_updates(event, content))

    return updates


def _message_to_updates(event: dict[str, Any], content: Iterable[Any]) -> list[Any]:
    updates: list[Any] = []
    role = _safe_get(event, "type")
    for chunk in content:
        if isinstance(chunk, str):
            updates.append(_text_update(role, chunk))
            continue
        if not isinstance(chunk, dict):
            chunk = _ensure_dict(chunk)

        chunk_type = _safe_get(chunk, "type")
        if chunk_type == "text":
            updates.append(_text_update(role, _safe_get(chunk, "text", "")))
            continue

        if chunk_type == "thinking":
            updates.append(update_agent_thought_text(_safe_get(chunk, "thinking", "")))
            continue

        if chunk_type == "image":
            source = _ensure_dict(_safe_get(chunk, "source", {}))
            if _safe_get(source, "type") == "base64":
                updates.append(
                    update_agent_message(
                        image_block(
                            data=_safe_get(source, "data", ""),
                            mime_type=_safe_get(source, "media_type", "application/octet-stream"),
                            uri=None,
                        )
                    )
                )
            elif _safe_get(source, "type") == "url":
                updates.append(
                    update_agent_message(
                        image_block(
                            data="",
                            mime_type="",
                            uri=_safe_get(source, "url"),
                        )
                    )
                )
            continue

        if chunk_type == "tool_use":
            updates.append(
                start_tool_call(
                    tool_call_id=_safe_get(chunk, "id", ""),
                    title=_safe_get(chunk, "name") or "Tool",
                    kind="other",
                    status="pending",
                    raw_input=_safe_json(_safe_get(chunk, "input")),
                )
            )
            continue

        if chunk_type == "tool_result":
            updates.append(
                update_tool_call(
                    tool_call_id=_safe_get(chunk, "tool_use_id", ""),
                    status="failed" if _safe_get(chunk, "is_error") else "completed",
                    content=_tool_result_content(_safe_get(chunk, "content"), is_error=bool(_safe_get(chunk, "is_error"))),
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


def _normalize_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return {"content": str(value)}


def _ensure_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return {"content": value}
    return _normalize_obj(value)


def _safe_get(obj: Any, key: str, default: Any = None) -> Any:
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        if hasattr(obj, "get"):
            return obj.get(key, default)
        if hasattr(obj, key):
            return getattr(obj, key)
    except Exception:
        return default
    return default


def _normalize_recursive(value: Any) -> Any:
    import json
    
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    
    if isinstance(value, dict):
        return {str(k): _normalize_recursive(v) for k, v in value.items()}
    
    if isinstance(value, (list, tuple)):
        return [_normalize_recursive(v) for v in value]
    
    # Handle pydantic models
    if hasattr(value, "model_dump_json"):
        try:
            return json.loads(value.model_dump_json())
        except Exception:
            pass
    
    if hasattr(value, "model_dump"):
        try:
            return _normalize_recursive(value.model_dump(mode="json"))
        except Exception:
            pass
        try:
            return _normalize_recursive(value.model_dump())
        except Exception:
            pass
    
    if hasattr(value, "json") and callable(getattr(value, "json")):
        try:
            return json.loads(value.json())
        except Exception:
            pass
    
    if hasattr(value, "dict") and callable(getattr(value, "dict")):
        try:
            return _normalize_recursive(value.dict())
        except Exception:
            pass
    
    if hasattr(value, "__dict__"):
        return _normalize_recursive(dict(value.__dict__))
    
    return str(value)
