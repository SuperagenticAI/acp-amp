# Zed (step-by-step)

This guide explains how to run **acp-amp** in Zed in very simple steps.

## What you need

- Python 3.10 or newer
- Node.js 18 or newer
- An Amp API key (if you use API key login)

## Step 1: Install the package (recommended)

Open a terminal in this repo and run:

```bash
uv tool install acp-amp
```

If you prefer pip:

```bash
pip install acp-amp
```

## Step 2: Install Amp CLI if needed

Some Amp setups require the Amp CLI. If your SDK setup needs it, install:

```bash
npm install -g @sourcegraph/amp
```

## Step 2b: Optional Node shim

If you installed from PyPI and do not have the source code, run:

```bash
acp-amp setup
```

Then install the shim dependencies:

```bash
cd ~/.acp-amp/shim
npm install
```

## Step 2c: Install the Node shim from the repo

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

## Optional: force the Node shim

If you want to use the Node shim instead of the Python SDK, set your command to:

```
acp-amp run --driver node
```

## Optional: force the Python SDK

```
acp-amp run --driver python
```

## If it does not work

- Make sure the **AMP_API_KEY** is correct
- Make sure `node-shim` dependencies are installed
- Try closing and reopening Zed
- Check Zed’s output panel for errors
