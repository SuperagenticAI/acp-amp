from __future__ import annotations

from typing import Any

from acp.schema import (
    EmbeddedResourceContentBlock,
    ImageContentBlock,
    ResourceContentBlock,
    TextContentBlock,
)


def prompt_to_text(prompt: list[Any]) -> str:
    parts: list[str] = []
    for block in prompt:
        if isinstance(block, TextContentBlock):
            text = block.text
            if text.strip() == "/init":
                text = _init_instructions()
            parts.append(text)
            continue
        if isinstance(block, ResourceContentBlock):
            parts.append(f"\n[resource link] {block.uri}\n")
            continue
        if isinstance(block, EmbeddedResourceContentBlock):
            resource = block.resource
            text = getattr(resource, "text", None)
            uri = getattr(resource, "uri", "")
            if text is not None:
                parts.append(f"\n[embedded context {uri}]\n{text}\n[context end]\n")
            continue
        if isinstance(block, ImageContentBlock):
            parts.append("\n[image omitted]\n")
            continue
    return "".join(parts)


def _init_instructions() -> str:
    return (
        "Please analyze this codebase and create an AGENTS.md file containing:\n"
        "1. Build/lint/test commands - especially for running a single test\n"
        "2. Architecture and codebase structure information, including important subprojects, "
        "internal APIs, databases, etc.\n"
        "3. Code style guidelines, including imports, conventions, formatting, types, naming "
        "conventions, error handling, etc.\n\n"
        "The file you create will be given to agentic coding tools (such as yourself) that "
        "operate in this repository. Make it about 20 lines long.\n\n"
        "If there are Cursor rules (in .cursor/rules/ or .cursorrules), Claude rules (CLAUDE.md), "
        "Windsurf rules (.windsurfrules), Cline rules (.clinerules), Goose rules (.goosehints), "
        "or Copilot rules (in .github/copilot-instructions.md), make sure to include them. "
        "Also, first check if there is an existing AGENTS.md or AGENT.md file, and if so, "
        "update it instead of overwriting it."
    )


def mcp_servers_to_amp_config(mcp_servers: list[Any]) -> dict[str, Any]:
    mcp_config: dict[str, Any] = {}
    for server in mcp_servers:
        name = getattr(server, "name", None)
        command = getattr(server, "command", None)
        args = getattr(server, "args", None)
        env = getattr(server, "env", None)
        if not name or not command:
            continue
        env_map = None
        if env:
            env_map = {e.name: e.value for e in env}
        mcp_config[name] = {
            "command": command,
            "args": args or [],
            "env": env_map,
        }
    return mcp_config
