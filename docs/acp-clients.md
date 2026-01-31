# ACP Clients

acp-amp works with any [Agent Client Protocol (ACP)](https://github.com/anthropics/agent-client-protocol) compatible client. This guide covers configuration for popular ACP clients.

---

## How ACP Works

ACP clients communicate with agents via JSON-RPC over stdin/stdout:

```
┌─────────────────┐     stdin/stdout      ┌─────────────────┐
│   ACP Client    │◀────────────────────▶│    acp-amp      │
│  (Zed, etc.)    │      JSON-RPC         │  (Python/Node)  │
└─────────────────┘                       └─────────────────┘
```

Any client that can:

1. Launch a subprocess
2. Send JSON-RPC over stdin
3. Receive JSON-RPC from stdout

...can use acp-amp.

---

## SuperQode

[SuperQode](https://github.com/SuperagenticAI/superqode) is an AI coding agent platform with native ACP support.

### Configuration

Add to your SuperQode config:

=== "Python Version"

    ```yaml
    agents:
      amp:
        description: "Amp Code agent"
        protocol: acp
        command: acp-amp
        args: ["run"]
    ```

=== "Node.js Version"

    ```yaml
    agents:
      amp:
        description: "Amp Code agent"
        protocol: acp
        command: npx
        args: ["@superagenticai/acp-amp"]
    ```

### Usage

```bash
# Connect to Amp
superqode connect acp amp

# Start a conversation
superqode chat amp "Explain this codebase"
```

---

## Toad

[Toad](https://github.com/batrachianai/toad) is a Python-based ACP client.

### Configuration

```python
from toad import ACPClient

# Python version
client = ACPClient(
    command="acp-amp",
    args=["run"]
)

# Node.js version
client = ACPClient(
    command="npx",
    args=["@superagenticai/acp-amp"]
)
```

### Usage

```python
async with client:
    response = await client.prompt("Explain this function")
    print(response)
```

---

## fast-agent

[fast-agent](https://github.com/evalstate/fast-agent) is a fast Python ACP client.

### Configuration

```python
from fast_agent import Agent

# Create Amp agent
amp = Agent(
    command="acp-amp",
    args=["run"],
    env={"AMP_API_KEY": "your-key"}  # optional
)
```

### Usage

```python
result = await amp.run("Refactor this code")
```

---

## Generic ACP Client

For any ACP-compatible client, provide these details:

### Command

=== "Python Version"

    ```
    Command: acp-amp
    Arguments: run
    ```

=== "Node.js Version"

    ```
    Command: npx
    Arguments: @superagenticai/acp-amp
    ```

=== "Node.js Global"

    ```
    Command: acp-amp
    Arguments: (none)
    ```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AMP_API_KEY` | Amp API key | Only if not using `amp login` |

### Protocol Details

- **Transport**: stdin/stdout
- **Format**: Newline-delimited JSON (NDJSON)
- **Protocol**: JSON-RPC 2.0
- **ACP Version**: 1

---

## Building Your Own Client

If you're building an ACP client, here's how to integrate with acp-amp:

### 1. Spawn the Process

```python
import subprocess

# Python version
process = subprocess.Popen(
    ["acp-amp", "run"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Node.js version
process = subprocess.Popen(
    ["npx", "@superagenticai/acp-amp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
```

### 2. Initialize

Send the initialize request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": 1,
    "clientCapabilities": {}
  }
}
```

### 3. Create a Session

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "newSession",
  "params": {
    "cwd": "/path/to/project",
    "mcpServers": []
  }
}
```

### 4. Send a Prompt

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "prompt",
  "params": {
    "sessionId": "session-id-from-step-3",
    "prompt": [
      {"type": "text", "text": "Explain this codebase"}
    ]
  }
}
```

### 5. Handle Notifications

The agent sends `sessionUpdate` notifications with:

- `agent_message_chunk` — Text from the agent
- `tool_call` — Tool execution started
- `tool_call_update` — Tool execution completed
- `agent_thought_chunk` — Agent's thinking process

---

## Troubleshooting

### Connection Issues

1. Make sure the command is in your PATH
2. Test the command directly:
   ```bash
   acp-amp run
   # or
   npx @superagenticai/acp-amp
   ```
3. Check stderr for error messages

### Authentication

Make sure Amp is authenticated:

```bash
amp login
```

Or provide an API key:

```bash
AMP_API_KEY="your-key" acp-amp run
```

### Protocol Debugging

Enable verbose logging (check your client's documentation) to see the JSON-RPC messages being exchanged.

---

## Resources

- [ACP Specification](https://github.com/anthropics/agent-client-protocol)
- [Amp Documentation](https://ampcode.com/manual)
- [acp-amp GitHub](https://github.com/SuperagenticAI/acp-amp)
