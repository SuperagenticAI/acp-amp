# acp-amp

[![CI](https://github.com/SuperagenticAI/acp-amp/actions/workflows/ci.yml/badge.svg)](https://github.com/SuperagenticAI/acp-amp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/acp-amp)](https://pypi.org/project/acp-amp/)
[![npm](https://img.shields.io/npm/v/@superagenticai/acp-amp)](https://www.npmjs.com/package/@superagenticai/acp-amp)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**ACP adapter for [Amp Code](https://ampcode.com)** — Use Amp in any [Agent Client Protocol (ACP)](https://github.com/anthropics/agent-client-protocol) compatible client like [Zed](https://zed.dev).

<p align="center">
  <img src="docs/img/acp-amp-diagram.png" alt="acp-amp architecture" width="600">
</p>

---

## 🎯 Choose Your Version

| If you prefer... | Install | Package |
|------------------|---------|---------|
| **Python** | `pip install acp-amp` | [PyPI](https://pypi.org/project/acp-amp/) |
| **Node.js** | `npm install -g @superagenticai/acp-amp` | [npm](https://www.npmjs.com/package/@superagenticai/acp-amp) |

Both versions provide identical functionality — full Amp Code agent capabilities in ACP-compatible clients.

---

## 🚀 Quick Start

### For Python Developers

```bash
# Install (recommended)
uv tool install acp-amp

# Run
acp-amp run
```

### For Node.js Developers

```bash
# Install
npm install -g @superagenticai/acp-amp

# Run
acp-amp
```

### For Zed Users (Quickest Setup)

Add to your Zed settings (`~/.config/zed/settings.json`):

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

No installation needed — npx downloads and runs automatically!

---

## 📋 Prerequisites

Before using acp-amp, you need:

1. **Amp CLI** installed and authenticated:
   ```bash
   curl -fsSL https://ampcode.com/install.sh | bash
   amp login
   ```

2. **Runtime** (one of):
   - Python 3.10+ and [uv](https://docs.astral.sh/uv/) (for Python version)
   - Node.js 18+ (for Node.js version)

---

## 🐍 Python Version (Detailed)

The Python version is ideal for Python developers and integrates with Python-based ACP clients.

### Installation

```bash
# Recommended
uv tool install acp-amp

# Alternative: pip
pip install acp-amp
```

### Running

```bash
# Default: uses Python SDK
acp-amp run

# Explicit Python SDK
acp-amp run --driver python

# Node shim fallback (if Python SDK has issues)
acp-amp run --driver node

# Auto-detect (tries Python first, falls back to Node)
acp-amp run --driver auto
```

### Driver Comparison

| Driver | Description | When to Use |
|--------|-------------|-------------|
| `python` | Native Python SDK (`amp-sdk`) | Default, best performance |
| `node` | Node.js shim fallback | If Python SDK has issues |
| `auto` | Tries Python, falls back to Node | Maximum compatibility |

### Setting Up Node Shim (Fallback Only)

Only needed if you want to use `--driver node`:

```bash
# Create shim files
acp-amp setup

# Install shim dependencies
cd ~/.acp-amp/shim
npm install
```

### Zed Configuration (Python)

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": ["run"]
    }
  }
}
```

With explicit driver:

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": ["run", "--driver", "python"]
    }
  }
}
```

---

## 📦 Node.js Version (Detailed)

The Node.js version is ideal for JavaScript/TypeScript developers and npm-based workflows.

### Installation

```bash
# Global install
npm install -g @superagenticai/acp-amp

# Or run directly with npx (no install)
npx @superagenticai/acp-amp
```

### Running

```bash
# If installed globally
acp-amp

# Using npx (no install needed)
npx @superagenticai/acp-amp
```

### Zed Configuration (Node.js)

With global install:

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp"
    }
  }
}
```

With npx (no install needed):

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

---

## 🔧 Zed Configuration (Complete Examples)

### Minimal Setup

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

### With API Key

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

### Python with Specific Driver

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": ["run", "--driver", "python"],
      "env": {
        "AMP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Full Path (if command not in PATH)

```json
{
  "agent_servers": {
    "Amp": {
      "command": "/Users/yourname/.local/bin/acp-amp",
      "args": ["run"]
    }
  }
}
```

---

## 🔌 Other ACP Clients

### SuperQode

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: acp-amp
    args: []
```

```bash
superqode connect acp amp
```

### Generic ACP Client

Any ACP client that can launch a subprocess and speak JSON-RPC over stdio:

```bash
# Python version
acp-amp run

# Node.js version
npx @superagenticai/acp-amp
```

### Python ACP Clients

These Python-based ACP clients work great with acp-amp:

- [Toad](https://github.com/batrachianai/toad)
- [fast-agent](https://github.com/evalstate/fast-agent)
- [SuperQode](https://github.com/SuperagenticAI/superqode)

---

## ✨ Features

- **Full Amp Code capabilities** — All Amp features available in your ACP client
- **Multi-turn conversations** — Thread continuity across interactions
- **Tool execution** — Run tools with permission modes (default/bypass)
- **MCP server integration** — Connect to Model Context Protocol servers
- **Image support** — Send and receive images
- **Session management** — Multiple concurrent sessions

---

## 🏗️ Project Structure

```
acp-amp/
├── acp_amp/              # Python package (pip install acp-amp)
│   ├── cli.py            # Command-line interface
│   ├── server.py         # ACP server implementation
│   └── driver/
│       ├── python_sdk.py # Python SDK driver (default)
│       └── node_sdk.py   # Node shim driver (fallback)
├── node/                 # Node.js package (@superagenticai/acp-amp)
│   └── src/
│       ├── index.js      # Entry point
│       ├── server.js     # ACP server implementation
│       └── to-acp.js     # Event conversion
├── node-shim/            # Minimal shim for Python's --driver node
└── docs/                 # Documentation
```

---

## 🧪 Development

### Python Development

```bash
# Clone and install
git clone https://github.com/SuperagenticAI/acp-amp.git
cd acp-amp
pip install -e .[test]

# Run tests
pytest

# With uv
uv sync
uv run pytest
```

### Node.js Development

```bash
cd node
npm install
npm start
```

### Documentation

```bash
pip install -e .[docs]
mkdocs serve
# Visit http://localhost:8000
```

---

## 🐛 Troubleshooting

### "amp: command not found"

Install the Amp CLI:
```bash
curl -fsSL https://ampcode.com/install.sh | bash
amp login
```

### "SystemMessage object has no attribute 'get'" (Python)

Update to the latest version:
```bash
pip install --upgrade acp-amp
```

### Python SDK issues

Use the Node shim fallback:
```bash
acp-amp run --driver node
```

### Zed doesn't show the agent

1. Check your settings.json syntax
2. Restart Zed
3. Check Zed's output panel for errors

### More help

See [Troubleshooting Guide](https://superagenticai.github.io/acp-amp/troubleshooting/)

---

## 📄 License

Apache-2.0

---

## 🙏 Credits

Brought to you by [Superagentic AI](https://super-agentic.ai)

Built with:
- [Amp Code](https://ampcode.com) by Sourcegraph
- [Agent Client Protocol](https://github.com/anthropics/agent-client-protocol) by Anthropic
