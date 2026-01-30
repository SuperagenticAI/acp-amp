# Zed (step-by-step)

This guide explains how to run **acp-amp** in Zed in very simple steps.

## What you need

- Python 3.10 or newer
- Node.js 18 or newer
- An Amp API key (if you use API key login)

## Step 1: Install the Python package

Open a terminal in this repo and run:

```bash
pip install -e .
```

## Step 2: Install the Node shim

```bash
cd node-shim
npm install
```

## Step 3: Tell Zed about the agent

1. Open Zed
2. Open **Settings** (press `Cmd+,` on macOS or `Ctrl+,` on Linux/Windows)
3. Find or add `settings.json`
4. Paste this:

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

## Step 4: Start the agent

1. Open the agent panel in Zed
2. Choose **Amp**
3. Type a prompt and press Enter

If it works, you will see the response appear in Zed.

## If it does not work

- Make sure the **AMP_API_KEY** is correct
- Make sure `node-shim` dependencies are installed
- Try closing and reopening Zed
- Check Zed’s output panel for errors
