# acp-amp Documentation

**ACP adapter for [Amp Code](https://ampcode.com)** — Use Amp in any [Agent Client Protocol (ACP)](https://github.com/agentclientprotocol/agent-client-protocol) compatible client like [Zed](https://zed.dev).

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 1rem 0;">
  <iframe
    src="https://www.youtube.com/embed/Yt9-aSzPMhY"
    title="acp-amp demo"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
  ></iframe>
</div>

---

## What is acp-amp?

acp-amp bridges [Amp Code](https://ampcode.com) to the [Agent Client Protocol (ACP)](https://github.com/agentclientprotocol/agent-client-protocol), allowing you to use Amp's powerful AI coding capabilities in any ACP-compatible client.

**Important:** ACP requires a paid Amp credit balance. The free credit version does not work for ACP. Top up a few dollars in Amp to enable ACP access.

**Available in two versions:**

| Version | Install | Best For |
|---------|---------|----------|
| **Python** | `pip install acp-amp` | Python developers, uv/pip users |
| **Node.js** | `npm install -g @superagenticai/acp-amp` | JavaScript developers, npm users |

Both versions provide identical functionality.

---

## Quick Start

=== "Python"

    ```bash
    uv tool install acp-amp
    acp-amp run
    ```

=== "Node.js"

    ```bash
    npm install -g @superagenticai/acp-amp
    acp-amp
    ```

=== "Zed (No Install)"

    Add to `~/.config/zed/settings.json`:
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

## Where You Can Use It

### Editors

- **[Zed](https://zed.dev)** — Modern code editor with native ACP support

### ACP Clients

- **[SuperQode](https://github.com/SuperagenticAI/superqode)** — AI coding agent platform
- **[Toad](https://github.com/batrachianai/toad)** — Python ACP client
- **[fast-agent](https://github.com/evalstate/fast-agent)** — Fast Python ACP client
- Any client that speaks JSON-RPC over stdio

acp-amp works with any ACP-compatible client. See the official ACP ecosystem list on the [Zed ACP page](https://zed.dev/acp) and the [ACP Registry announcement](https://zed.dev/blog/acp-registry).

**Agents on ACP (from the ecosystem list):**
- Gemini CLI (ACP Registry)
- Claude Code (ACP Registry, via adapter)
- Codex (ACP Registry, via adapter)
- GitHub Copilot (ACP Registry)
- JetBrains Junie (In Progress)
- Goose
- Kimi CLI
- OpenCode (ACP Registry)
- Stakpak
- VT Code
- Auggie CLI (ACP Registry)
- Code Assistant
- cagent
- fast-agent
- LLMling-Agent

---

## Features

| Feature | Description |
|---------|-------------|
| **Full Amp capabilities** | All Amp Code features in your ACP client |
| **Multi-turn conversations** | Thread continuity across interactions |
| **Tool execution** | Permission modes: default or bypass |
| **MCP integration** | Connect to Model Context Protocol servers |
| **Image support** | Send and receive images |
| **Session management** | Multiple concurrent sessions |

---

## Documentation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Install and run acp-amp in minutes

    [:octicons-arrow-right-24: Getting Started](getting-started.md)

-   :material-code-braces:{ .lg .middle } **Zed Setup**

    ---

    Step-by-step Zed editor configuration

    [:octicons-arrow-right-24: Zed Setup](zed.md)

-   :material-connection:{ .lg .middle } **ACP Clients**

    ---

    Configure other ACP clients

    [:octicons-arrow-right-24: ACP Clients](acp-clients.md)

-   :material-wrench:{ .lg .middle } **Troubleshooting**

    ---

    Common issues and solutions

    [:octicons-arrow-right-24: Troubleshooting](troubleshooting.md)

</div>

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   ACP Client    │────▶│    acp-amp      │────▶│    Amp Code     │
│  (Zed, etc.)    │◀────│  (Python/Node)  │◀────│    (Cloud)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │    JSON-RPC/stdio     │     Amp SDK          │
        │◀─────────────────────▶│◀─────────────────────▶│
```

---

## Credits

Brought to you by [Superagentic AI](https://super-agentic.ai)

Built with:

- [Amp Code](https://ampcode.com) by Amp
- [Agent Client Protocol](https://github.com/agentclientprotocol/agent-client-protocol)
