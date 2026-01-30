# acp-amp

ACP adapter for [Amp Code](https://ampcode.com) - bridges Amp to [Agent Client Protocol (ACP)](https://github.com/anthropics/agent-client-protocol) compatible clients like [Zed](https://zed.dev).

Available in both **Python** and **Node.js** - choose whichever fits your stack.

Brought to you by [Superagentic AI](https://super-agentic.ai)

## Choose Your Version

| Version | Install | Best For |
|---------|---------|----------|
| **Python** | `pip install acp-amp` | Python developers, uv users |
| **Node.js** | `npm install -g @superagenticai/acp-amp` | Node.js developers, npm users |

Both versions provide the same functionality - full Amp Code agent capabilities in ACP-compatible clients.

## Where You Can Use It

- **Zed editor** via `agent_servers`
- **SuperQode** via ACP agent config
- Any ACP client that can launch a subprocess and speak JSON-RPC over stdio

Python-based ACP clients:

- [Toad](https://github.com/batrachianai/toad)
- [fast-agent](https://github.com/evalstate/fast-agent)
- [SuperQode](https://github.com/SuperagenticAI/superqode)

## Features

- Full Amp Code agent capabilities
- Multi-turn conversations with thread continuity
- Tool execution with permission modes (default/bypass)
- MCP server integration
- Image support

## Quick Links

- [Getting Started](getting-started.md)
- [Zed Setup](zed.md)
- [SuperQode Setup](superqode.md)
- [Generic ACP Client Notes](acp-clients.md)
- [Development](development.md)
- [Troubleshooting](troubleshooting.md)
