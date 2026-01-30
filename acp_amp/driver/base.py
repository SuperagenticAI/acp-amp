from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, Protocol


@dataclass
class DriverCapabilities:
    supports_images: bool = False
    supports_embedded_context: bool = True
    supports_mcp_http: bool = False
    supports_mcp_sse: bool = False


class AmpDriver(Protocol):
    capabilities: DriverCapabilities

    async def start(self) -> None:
        ...

    async def close(self) -> None:
        ...

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
        ...

    async def cancel(self, request_id: str) -> None:
        ...
