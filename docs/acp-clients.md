# Any ACP Client (step-by-step)

This guide explains how to run **acp-amp** from any ACP-compatible client.

## What you need

- Python 3.10 or newer
- Node.js 18 or newer
- An Amp API key (if you use API key login)

## Step 1: Install the Python package

In this repo, run:

```bash
pip install -e .
```

## Step 2: Install the Node shim

```bash
cd node-shim
npm install
```

## Step 3: Run the agent

In a terminal, run:

```bash
acp-amp
```

Your ACP client should launch this command as a subprocess and talk over stdin/stdout.

## Step 4: Configure your client

Every ACP client has a place to configure agents. Add a command that points to `acp-amp`.

Example settings (generic):

```
command: acp-amp
args: []
env:
  AMP_API_KEY: your-api-key-here
```

## Notes

- **Do not** log to stdout. ACP uses stdout for protocol messages.
- Logs should go to stderr.
- If your client allows environment variables, set `AMP_API_KEY` there.
