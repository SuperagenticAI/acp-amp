# @superagenticai/acp-amp (Node.js)

ACP adapter for Amp Code - bridges [Amp](https://ampcode.com) to [Agent Client Protocol (ACP)](https://github.com/anthropics/agent-client-protocol) compatible clients like [Zed](https://zed.dev).

## Installation

```bash
npm install -g @superagenticai/acp-amp
```

## Prerequisites

- Node.js 18+
- [Amp CLI](https://ampcode.com) installed and authenticated (`amp login`)

## Usage with Zed

Add to your Zed settings (`~/.config/zed/settings.json`):

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp"
    }
  }
}
```

Or with explicit path:

```json
{
  "agent_servers": {
    "Amp": {
      "command": "npx",
      "args": ["@superagenticai/acp-amp"]
    }
  }
}
```

## Features

- Full Amp Code agent capabilities in Zed
- Multi-turn conversations with thread continuity
- Tool execution with permission modes (default/bypass)
- MCP server integration
- Image support

## Python Alternative

If you prefer Python, see the main [acp-amp](https://pypi.org/project/acp-amp/) package:

```bash
pip install acp-amp
acp-amp run
```

## License

Apache-2.0
