from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from acp import PROTOCOL_VERSION
from acp.exceptions import RequestError
from acp.helpers import update_available_commands, update_agent_message, text_block
from acp.schema import (
    AgentCapabilities,
    AuthenticateResponse,
    AvailableMode,
    Implementation,
    InitializeResponse,
    McpCapabilities,
    ModesResponse,
    NewSessionResponse,
    PromptResponse,
    PromptCapabilities,
)
from acp.interfaces import Agent, Client

from acp_amp.driver.base import AmpDriver
from acp_amp.mapping.to_acp import amp_event_to_updates
from acp_amp.mapping.to_amp import mcp_servers_to_amp_config, prompt_to_text


@dataclass
class _SessionState:
    session_id: str
    mode: str = "default"
    mcp_config: dict[str, Any] | None = None
    thread_id: str | None = None
    active_request_id: str | None = None
    cancelled: bool = False


class AmpAcpAgent(Agent):
    def __init__(self, driver: AmpDriver) -> None:
        self._driver = driver
        self._client: Client | None = None
        self._sessions: dict[str, _SessionState] = {}
        self._session_counter = 0

    def on_connect(self, conn: Client) -> None:
        self._client = conn

    async def initialize(
        self,
        protocol_version: int,
        client_capabilities: Any | None = None,
        client_info: Any | None = None,
        **_: Any,
    ) -> InitializeResponse:
        return InitializeResponse(
            protocol_version=PROTOCOL_VERSION,
            agent_capabilities=AgentCapabilities(
                load_session=False,
                mcp_capabilities=McpCapabilities(
                    http=True,
                    sse=True,
                ),
                prompt_capabilities=PromptCapabilities(
                    image=True,
                    embedded_context=True,
                    audio=False,
                ),
            ),
            agent_info=Implementation(
                name="acp-amp",
                title="Amp ACP Adapter",
                version="0.1.0",
            ),
            auth_methods=[],
        )

    async def authenticate(self, method_id: str, **_: Any) -> AuthenticateResponse | None:
        raise RequestError.auth_required()

    async def new_session(self, cwd: str, mcp_servers: list[Any], **_: Any) -> NewSessionResponse:
        session_id = f"amp-{self._session_counter}"
        self._session_counter += 1

        mcp_config = mcp_servers_to_amp_config(mcp_servers)
        self._sessions[session_id] = _SessionState(
            session_id=session_id,
            mcp_config=mcp_config,
        )

        if self._client:
            try:
                await self._client.session_update(
                    session_id=session_id,
                    update=update_available_commands(
                        [
                            {
                                "name": "init",
                                "description": "Generate an AGENTS.md file for the project",
                            }
                        ]
                    ),
                )
            except Exception:
                pass

        return NewSessionResponse(
            session_id=session_id,
            modes=ModesResponse(
                current_mode_id="default",
                available_modes=[
                    AvailableMode(id="default", name="Default", description="Prompt for tool permission"),
                    AvailableMode(id="bypass", name="Bypass", description="Skip tool permission prompts"),
                ],
            ),
        )

    async def load_session(self, cwd: str, mcp_servers: list[Any], session_id: str, **_: Any) -> None:
        return None

    async def set_session_mode(self, mode_id: str, session_id: str, **_: Any) -> None:
        session = self._sessions.get(session_id)
        if session:
            session.mode = mode_id
        return None

    async def prompt(self, prompt: list[Any], session_id: str, **kwargs: Any) -> PromptResponse:
        if not self._client:
            raise RuntimeError("client connection not ready")

        session = self._sessions.get(session_id)
        if not session:
            raise RuntimeError("session not found")

        session.cancelled = False
        request_id = f"{session_id}-{asyncio.get_running_loop().time()}"
        session.active_request_id = request_id

        text_prompt = prompt_to_text(prompt)
        cwd = kwargs.get("cwd")
        allow_all = session.mode == "bypass"

        stop_reason = "end_turn"
        async for item in self._driver.stream_prompt(
            prompt=text_prompt,
            cwd=cwd,
            allow_all=allow_all,
            mcp_config=session.mcp_config,
            thread_id=session.thread_id,
            request_id=request_id,
        ):
            item_type = item.get("type")
            if item_type == "event":
                event = item.get("event", {})
                thread_id = event.get("session_id") or event.get("threadId")
                if thread_id and not session.thread_id:
                    session.thread_id = str(thread_id)

                for update in amp_event_to_updates(event):
                    try:
                        await self._client.session_update(session_id=session_id, update=update)
                    except Exception:
                        pass
                continue

            if item_type == "error":
                error_text = str(item.get("error", {}).get("message", "Unknown error"))
                try:
                    await self._client.session_update(
                        session_id=session_id,
                        update=update_agent_message(text_block(f"Error: {error_text}")),
                    )
                except Exception:
                    pass
                stop_reason = "error"
                break

            if item_type == "done":
                stop_reason = item.get("stopReason") or "end_turn"
                break

        if session.cancelled:
            stop_reason = "cancelled"

        session.active_request_id = None
        session.cancelled = False

        return PromptResponse(stop_reason=stop_reason)

    async def cancel(self, session_id: str, **_: Any) -> None:
        session = self._sessions.get(session_id)
        if not session or not session.active_request_id:
            return None
        session.cancelled = True
        await self._driver.cancel(session.active_request_id)
        return None
