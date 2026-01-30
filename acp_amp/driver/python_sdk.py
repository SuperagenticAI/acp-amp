from __future__ import annotations

from typing import Any, AsyncIterator

from acp_amp.driver.base import AmpDriver, DriverCapabilities


class PythonAmpDriver(AmpDriver):
    capabilities = DriverCapabilities(
        supports_images=True,
        supports_embedded_context=True,
        supports_mcp_http=True,
        supports_mcp_sse=True,
    )

    def __init__(self) -> None:
        try:
            from amp_sdk import execute, AmpOptions  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("amp-sdk is not installed") from exc
        self._execute = execute
        self._AmpOptions = AmpOptions

    async def start(self) -> None:
        return None

    async def close(self) -> None:
        return None

    async def stream_prompt(
        self,
        *,
        prompt: str,
        cwd: str | None,
        allow_all: bool,
        mcp_config: dict[str, Any] | None,
        thread_id: str | None,
        request_id: str,
    ) -> AsyncIterator[dict[str, Any]]:
        options = self._build_options(
            cwd=cwd,
            allow_all=allow_all,
            mcp_config=mcp_config,
            thread_id=thread_id,
        )
        try:
            async for message in self._execute(prompt, options=options):
                yield {"type": "event", "id": request_id, "event": _normalize_event(message)}
            yield {"type": "done", "id": request_id, "stopReason": "end_turn"}
        except Exception as exc:  # pragma: no cover
            yield {"type": "error", "id": request_id, "error": {"message": str(exc)}}

    async def cancel(self, request_id: str) -> None:
        return None

    def _build_options(
        self,
        *,
        cwd: str | None,
        allow_all: bool,
        mcp_config: dict[str, Any] | None,
        thread_id: str | None,
    ) -> Any:
        base: dict[str, Any] = {}
        if cwd:
            base["cwd"] = cwd
        if allow_all:
            base["dangerously_allow_all"] = True
            base["dangerouslyAllowAll"] = True
        if mcp_config:
            base["mcp_config"] = mcp_config
            base["mcpConfig"] = mcp_config
        if thread_id:
            base["continue"] = thread_id
            base["continue_thread"] = thread_id
            base["thread_id"] = thread_id

        candidates = [
            base,
            {k: v for k, v in base.items() if k not in ("dangerouslyAllowAll", "mcpConfig", "thread_id")},
            {k: v for k, v in base.items() if k not in ("dangerously_allow_all", "mcp_config", "continue_thread")},
            {k: v for k, v in base.items() if k in ("cwd", "dangerously_allow_all")},
            {k: v for k, v in base.items() if k in ("cwd", "dangerouslyAllowAll")},
            {},
        ]
        for attempt in candidates:
            try:
                return self._AmpOptions(**attempt)
            except TypeError:
                continue
        return self._AmpOptions()


def _normalize_event(message: Any) -> dict[str, Any]:
    import json
    
    # First try: use pydantic's JSON serialization (handles all nested models)
    if hasattr(message, "model_dump_json"):
        try:
            result = json.loads(message.model_dump_json())
            if isinstance(result, dict):
                return result
        except Exception:
            pass
    
    # Second try: use model_dump with json mode
    if hasattr(message, "model_dump"):
        try:
            result = message.model_dump(mode="json")
            if isinstance(result, dict):
                return _deep_to_dict(result)
        except Exception:
            pass
        try:
            result = message.model_dump()
            if isinstance(result, dict):
                return _deep_to_dict(result)
        except Exception:
            pass
    
    # Third try: use older pydantic .json() method
    if hasattr(message, "json") and callable(getattr(message, "json")):
        try:
            result = json.loads(message.json())
            if isinstance(result, dict):
                return result
        except Exception:
            pass
    
    # Fourth try: use .dict() method
    if hasattr(message, "dict") and callable(getattr(message, "dict")):
        try:
            result = message.dict()
            if isinstance(result, dict):
                return _deep_to_dict(result)
        except Exception:
            pass
    
    # Fifth try: manually extract attributes
    if hasattr(message, "__dict__"):
        return _deep_to_dict(dict(message.__dict__))
    
    # Last resort
    return {"type": "assistant", "message": {"content": str(message)}}


def _deep_to_dict(value: Any) -> Any:
    """Recursively convert any non-dict objects to dicts."""
    import json
    
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    
    if isinstance(value, dict):
        return {str(k): _deep_to_dict(v) for k, v in value.items()}
    
    if isinstance(value, (list, tuple)):
        return [_deep_to_dict(v) for v in value]
    
    # Handle pydantic models that might be nested
    if hasattr(value, "model_dump_json"):
        try:
            return json.loads(value.model_dump_json())
        except Exception:
            pass
    
    if hasattr(value, "model_dump"):
        try:
            return _deep_to_dict(value.model_dump(mode="json"))
        except Exception:
            pass
        try:
            return _deep_to_dict(value.model_dump())
        except Exception:
            pass
    
    if hasattr(value, "json") and callable(getattr(value, "json")):
        try:
            return json.loads(value.json())
        except Exception:
            pass
    
    if hasattr(value, "dict") and callable(getattr(value, "dict")):
        try:
            return _deep_to_dict(value.dict())
        except Exception:
            pass
    
    if hasattr(value, "__dict__"):
        return _deep_to_dict(dict(value.__dict__))
    
    # Convert anything else to string
    return str(value)
