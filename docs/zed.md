# Zed Setup

This guide shows you how to use Amp in [Zed](https://zed.dev) editor using acp-amp.

---

## Prerequisites

1. **Zed** installed ([download](https://zed.dev))
2. **Amp CLI** installed and authenticated:
   ```bash
   curl -fsSL https://ampcode.com/install.sh | bash
   amp login
   ```

---

## Quick Setup (Recommended)

The fastest way to get Amp running in Zed — no installation required!

### Step 1: Open Zed Settings

- Press `Cmd+,` (macOS) or `Ctrl+,` (Linux/Windows)
- Or: Menu → Zed → Settings

### Step 2: Add Agent Configuration

Add this to your `settings.json`:

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

### Step 3: Use Amp

1. Open the Agent Panel in Zed
2. Select **Amp** from the dropdown
3. Type your prompt and press Enter

That's it! 🎉

---

## Alternative Configurations

### Python Version

If you prefer using the Python package:

```bash
uv tool install acp-amp
```

Then configure Zed:

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

### Node.js Global Install

If you've installed the npm package globally:

```bash
npm install -g @superagenticai/acp-amp
```

Then configure Zed:

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp"
    }
  }
}
```

---

## Configuration with API Key

If you use an API key instead of `amp login`:

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

## Python Driver Options

When using the Python version, you can specify a driver:

### Default (Python SDK)

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

### Node Shim Fallback

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": ["run", "--driver", "node"]
    }
  }
}
```

### Auto-detect

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": ["run", "--driver", "auto"]
    }
  }
}
```

---

## Complete Example Configurations

### Minimal (npx)

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

### Python with API Key

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp",
      "args": ["run", "--driver", "python"],
      "env": {
        "AMP_API_KEY": "amp_xxx..."
      }
    }
  }
}
```

### Node.js with Full Path

```json
{
  "agent_servers": {
    "Amp": {
      "command": "/opt/homebrew/bin/node",
      "args": ["/usr/local/lib/node_modules/@superagenticai/acp-amp/src/index.js"]
    }
  }
}
```

---

## Troubleshooting

### Agent doesn't appear in Zed

1. Check your `settings.json` syntax (no trailing commas)
2. Restart Zed completely
3. Check Zed's output panel for errors

### "command not found"

Use the full path to the command:

```bash
# Find the path
which acp-amp

# Use it in settings.json
```

### "amp: command not found"

Install the Amp CLI:

```bash
curl -fsSL https://ampcode.com/install.sh | bash
amp login
```

### Authentication errors

Make sure you're logged in:

```bash
amp login
```

Or provide an API key in your Zed settings.

### npx is slow

The first run downloads the package. Subsequent runs are faster.

For faster startup, use a global install:

```bash
npm install -g @superagenticai/acp-amp
```

Then change your config:

```json
{
  "agent_servers": {
    "Amp": {
      "command": "acp-amp"
    }
  }
}
```

---

## Next Steps

- [Troubleshooting](troubleshooting.md) — More detailed problem solving
- [ACP Clients](acp-clients.md) — Use with other ACP clients
- [Development](development.md) — Contribute to acp-amp
