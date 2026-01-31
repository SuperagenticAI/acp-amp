# SuperQode Setup

[SuperQode](https://github.com/SuperagenticAI/superqode) is an AI coding agent platform with native ACP support. This guide shows how to use Amp with SuperQode.

---

## Prerequisites

1. **SuperQode** installed
2. **Amp CLI** authenticated:
   ```bash
   curl -fsSL https://ampcode.com/install.sh | bash
   amp login
   ```

---

## Quick Setup

### Python Version

```bash
pip install acp-amp
```

Add to your SuperQode config:

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: acp-amp
    args: ["run"]
```

### Node.js Version

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: npx
    args: ["@superagenticai/acp-amp"]
```

Or with global install:

```bash
npm install -g @superagenticai/acp-amp
```

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: acp-amp
```

---

## Usage

### Connect to Amp

```bash
superqode connect acp amp
```

### Chat with Amp

```bash
superqode chat amp "Explain this codebase"
```

### Run a task

```bash
superqode run amp "Refactor the authentication module"
```

---

## Configuration Options

### With API Key

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: acp-amp
    args: ["run"]
    env:
      AMP_API_KEY: "your-api-key"
```

### With Working Directory

```yaml
agents:
  amp:
    description: "Amp Code agent"
    protocol: acp
    command: acp-amp
    args: ["run"]
    cwd: "/path/to/project"
```

### Python Driver Options

```yaml
agents:
  amp-python:
    description: "Amp with Python SDK"
    protocol: acp
    command: acp-amp
    args: ["run", "--driver", "python"]

  amp-node:
    description: "Amp with Node shim"
    protocol: acp
    command: acp-amp
    args: ["run", "--driver", "node"]
```

---

## Troubleshooting

### "Agent not found"

Make sure the agent is defined in your SuperQode config file.

### "Connection failed"

Test the command manually:

```bash
acp-amp run
# or
npx @superagenticai/acp-amp
```

### "Authentication error"

Login to Amp:

```bash
amp login
```

---

## More Information

- [SuperQode Documentation](https://github.com/SuperagenticAI/superqode)
- [ACP Clients Guide](acp-clients.md)
- [Troubleshooting](troubleshooting.md)
