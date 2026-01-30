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
                yield {"type": "event", "id": request_id, "event": message}
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
