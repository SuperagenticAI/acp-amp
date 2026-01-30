# Zed Setup

This guide explains how to run **acp-amp** in Zed.

## Prerequisites

- [Amp CLI](https://ampcode.com) installed and authenticated (`amp login`)
- **Python version**: Python 3.10+
- **Node.js version**: Node.js 18+

## Option 1: Python Version

### Step 1: Install

```bash
# Recommended
uv tool install acp-amp

# Or with pip
pip install acp-amp
```

### Step 2: Configure Zed

1. Open Zed
2. Open **Settings** (`Cmd+,` on macOS or `Ctrl+,` on Linux/Windows)
3. Add to `settings.json`:

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

With API key:

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

## Option 2: Node.js Version

### Step 1: Install

```bash
npm install -g @superagenticai/acp-amp
```

### Step 2: Configure Zed

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp"
    }
  }
}
```

Or using npx (no global install):

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

## Step 3: Use the Agent

1. Open the agent panel in Zed
2. Choose **Amp**
3. Type a prompt and press Enter

## Python Driver Options

If using the Python version, you can specify a driver:

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

| Driver | Description |
|--------|-------------|
| `python` | Uses `amp-sdk` Python package (default) |
| `node` | Uses Node.js shim fallback |

## Troubleshooting

- Make sure the **AMP_API_KEY** is correct (if using API key auth)
- Make sure `amp login` was successful
- Try closing and reopening Zed
- Check Zed's output panel for errors
- See [Troubleshooting](troubleshooting.md) for more help
