# @superagenticai/acp-amp

[![npm](https://img.shields.io/npm/v/@superagenticai/acp-amp)](https://www.npmjs.com/package/@superagenticai/acp-amp)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**ACP adapter for [Amp Code](https://ampcode.com)** — Use Amp in any [Agent Client Protocol (ACP)](https://github.com/agentclientprotocol/agent-client-protocol) compatible client like [Zed](https://zed.dev).

---

## 🚀 Quick Start

### No Installation Required

Use with npx — downloads and runs automatically:

```bash
npx @superagenticai/acp-amp
```

### Or Install Globally

```bash
npm install -g @superagenticai/acp-amp
acp-amp
```

---

## 📋 Prerequisites

1. **Node.js 18+**

2. **Amp CLI** installed and authenticated:
   ```bash
   curl -fsSL https://ampcode.com/install.sh | bash
   amp login
   ```

---

## 🔧 Zed Configuration

Add to your Zed settings (`~/.config/zed/settings.json`):

### Quickest Setup (npx)

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

### With Global Install

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp"
    }
  }
}
```

### With API Key

```json
{
  "agent_servers": {
    "Amp": {
      "command": "npx",
      "args": ["@superagenticai/acp-amp"],
      "env": {
        "AMP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

---

## ✨ Features

- **Full Amp Code capabilities** — All Amp features in your ACP client
- **Multi-turn conversations** — Thread continuity across interactions
- **Tool execution** — Permission modes (default/bypass)
- **MCP integration** — Connect to Model Context Protocol servers
- **Image support** — Send and receive images

---

## 🔌 Other ACP Clients

### SuperQode

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: npx
    args: ["@superagenticai/acp-amp"]
```

### Generic ACP Client

Any client that can spawn a subprocess with stdin/stdout JSON-RPC:

```bash
npx @superagenticai/acp-amp
```

---

## 🐍 Python Alternative

If you prefer Python, use the uv package:

```bash
uv tool install acp-amp
acp-amp run
```

See [acp-amp on PyPI](https://pypi.org/project/acp-amp/)

---

## 📖 Documentation

Full documentation: [superagenticai.github.io/acp-amp](https://superagenticai.github.io/acp-amp/)

- [Getting Started](https://superagenticai.github.io/acp-amp/getting-started/)
- [Zed Setup](https://superagenticai.github.io/acp-amp/zed/)
- [Troubleshooting](https://superagenticai.github.io/acp-amp/troubleshooting/)

---

## 🐛 Troubleshooting

### "amp: command not found"

```bash
curl -fsSL https://ampcode.com/install.sh | bash
amp login
```

### "Not authenticated"

```bash
amp login
```

### npx is slow

First run downloads the package. For faster startup:

```bash
npm install -g @superagenticai/acp-amp
```

---

## 📄 License

Apache-2.0

---

## 🙏 Credits

Brought to you by [Superagentic AI](https://super-agentic.ai)

Built with:
- [Amp Code](https://ampcode.com) by Amp
- [Agent Client Protocol](https://github.com/agentclientprotocol/agent-client-protocol)
