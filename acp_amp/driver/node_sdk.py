from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator

from acp_amp.driver.base import AmpDriver, DriverCapabilities


@dataclass
class _PendingRequest:
    queue: asyncio.Queue[dict[str, Any]]


class NodeAmpDriver(AmpDriver):
    capabilities = DriverCapabilities(
        supports_images=False,
        supports_embedded_context=True,
        supports_mcp_http=False,
        supports_mcp_sse=False,
    )

    def __init__(self, *, node_cmd: str, shim_path: Path) -> None:
        self._node_cmd = node_cmd
        self._shim_path = shim_path
        self._proc: asyncio.subprocess.Process | None = None
        self._reader_task: asyncio.Task | None = None
        self._pending: dict[str, _PendingRequest] = {}

    async def start(self) -> None:
        if self._proc:
            return
        self._proc = await asyncio.create_subprocess_exec(
            self._node_cmd,
            str(self._shim_path),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=sys.stderr,
        )
        self._reader_task = asyncio.create_task(self._read_loop())

    async def close(self) -> None:
        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass
        if self._proc:
            self._proc.terminate()
            try:
                await asyncio.wait_for(self._proc.wait(), timeout=5)
            except asyncio.TimeoutError:
                self._proc.kill()
            self._proc = None

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
        await self.start()
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self._pending[request_id] = _PendingRequest(queue=queue)

        payload = {
            "type": "start",
            "id": request_id,
            "prompt": prompt,
            "cwd": cwd,
            "allowAll": allow_all,
            "mcpConfig": mcp_config or {},
            "threadId": thread_id,
        }
        await self._send(payload)

        while True:
            msg = await queue.get()
            msg_type = msg.get("type")
            if msg_type == "event":
                yield msg
                continue
            if msg_type in ("done", "error"):
                yield msg
                break

        self._pending.pop(request_id, None)

    async def cancel(self, request_id: str) -> None:
        await self.start()
        await self._send({"type": "cancel", "id": request_id})

    async def _send(self, data: dict[str, Any]) -> None:
        if not self._proc or not self._proc.stdin:
            raise RuntimeError("node shim process is not running")
        encoded = (json.dumps(data) + "\n").encode("utf-8")
        self._proc.stdin.write(encoded)
        await self._proc.stdin.drain()

    async def _read_loop(self) -> None:
        if not self._proc or not self._proc.stdout:
            return
        while True:
            line = await self._proc.stdout.readline()
            if not line:
                break
            raw = line.decode("utf-8", errors="replace").strip()
            if not raw:
                continue
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue
            request_id = str(msg.get("id", ""))
            if not request_id or request_id not in self._pending:
                continue
            await self._pending[request_id].queue.put(msg)
