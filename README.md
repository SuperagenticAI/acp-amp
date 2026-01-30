# acp-amp

![CI](https://github.com/SuperagenticAI/acp-amp/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docs](https://img.shields.io/badge/docs-live-brightgreen.svg)

ACP adapter for [Amp Code](https://ampcode.com) - bridges Amp to [Agent Client Protocol (ACP)](https://github.com/anthropics/agent-client-protocol) compatible clients like [Zed](https://zed.dev).

Available in both **Python** and **Node.js** - choose whichever fits your stack.

Docs: https://superagenticai.github.io/acp-amp/

Brought to you by [Superagentic AI](https://super-agentic.ai)

## Quick Start

### Python (pip/uv)

```bash
pip install acp-amp
# or
uv tool install acp-amp
```

### Node.js (npm)

```bash
npm install -g @superagenticai/acp-amp
```

## Zed Configuration

### Python Version

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": []
    }
  }
}
```

### Node.js Version

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

## Where You Can Use It

- **Zed editor** via `agent_servers`
- **SuperQode** via ACP agent config
- Any ACP client that can launch a subprocess and speak JSON-RPC over stdio

Python-based ACP clients:
- [Toad](https://github.com/batrachianai/toad)
- [fast-agent](https://github.com/evalstate/fast-agent)
- [SuperQode](https://github.com/SuperagenticAI/superqode)

## Prerequisites

- [Amp CLI](https://ampcode.com) installed and authenticated (`amp login`)
- Python 3.10+ (for Python version) or Node.js 18+ (for Node.js version)

## Python Usage

```bash
# Run with Python SDK (default)
acp-amp run

# Run with Node shim fallback (if Python SDK has issues)
acp-amp run --driver node
```

### Python Driver Options

| Driver | Description |
|--------|-------------|
| `python` | Uses `amp-sdk` Python package (default) |
| `node` | Uses Node.js shim with `@sourcegraph/amp-sdk` |
| `auto` | Tries Python first, falls back to Node |

### Node Shim Setup (fallback only)

If you need the Node shim fallback:

```bash
acp-amp setup
cd ~/.acp-amp/shim
npm install
```

## Node.js Usage

```bash
# After npm install -g @superagenticai/acp-amp
acp-amp
```

Or run directly with npx:

```bash
npx @superagenticai/acp-amp
```

## Features

- Full Amp Code agent capabilities
- Multi-turn conversations with thread continuity
- Tool execution with permission modes (default/bypass)
- MCP server integration
- Image support

## ACP Client Examples

### SuperQode

```yaml
agents:
  amp:
    description: "Amp ACP adapter"
    protocol: acp
    command: acp-amp
    args: []
```

```bash
superqode connect acp amp
```

### Zed (with API key)

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": [],
      "env": {
        "AMP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Development

### Python

```bash
pip install -e .[test]
pytest

# or with uv
uv sync
uv run pytest
```

### Node.js

```bash
cd node
npm install
npm start
```

### Docs

```bash
pip install -e .[docs]
mkdocs serve

# or with uv
uv run mkdocs serve
```

## Project Structure

```
acp-amp/
├── acp_amp/           # Python package
│   └── driver/
│       ├── python_sdk.py   # Python SDK driver (default)
│       └── node_sdk.py     # Node shim driver (fallback)
├── node/              # Node.js package (@superagenticai/acp-amp)
│   └── src/
├── node-shim/         # Minimal shim for Python's --driver node
└── docs/
```

## Notes

- Stdout is reserved for ACP JSON-RPC messages; logs go to stderr
- Both packages use the official Amp SDK (`amp-sdk` for Python, `@sourcegraph/amp-sdk` for Node.js)

## License

Apache-2.0
