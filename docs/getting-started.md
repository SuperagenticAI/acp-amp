# Getting Started

This guide will help you install and run acp-amp. Choose the version that fits your stack.

---

## Prerequisites

Before installing acp-amp, you need the **Amp CLI** installed and authenticated:

```bash
# Install Amp CLI
curl -fsSL https://ampcode.com/install.sh | bash

# Login to Amp
amp login
```

---

## Choose Your Version

| If you are a... | Use | Install |
|-----------------|-----|---------|
| Python developer | Python version | `uv tool install acp-amp` |
| Node.js developer | Node.js version | `npm install -g @superagenticai/acp-amp` |
| Just want it to work | Node.js with npx | No install needed! |

---

## Python Version

### Who Should Use This

- Python developers
- Users of [uv](https://docs.astral.sh/uv/)
- Integration with Python-based ACP clients

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
```

### Driver Options

The Python version supports multiple drivers:

| Driver | Command | Description |
|--------|---------|-------------|
| `python` | `acp-amp run` | Native Python SDK (default, best performance) |
| `node` | `acp-amp run --driver node` | Node.js shim (fallback if Python has issues) |
| `auto` | `acp-amp run --driver auto` | Tries Python first, falls back to Node |

### Setting Up Node Shim (Optional Fallback)

Only needed if you want to use `--driver node`:

```bash
# Step 1: Create shim files
acp-amp setup

# Step 2: Install shim dependencies
cd ~/.acp-amp/shim
npm install
```

### Verify Installation

```bash
# Check version
acp-amp --help

# Test run (will wait for input, Ctrl+C to exit)
acp-amp run
```

---

## Node.js Version

### Who Should Use This

- JavaScript/TypeScript developers
- npm-based workflows
- Users who want the simplest setup

### Installation

=== "Global Install"

    ```bash
    npm install -g @superagenticai/acp-amp
    ```

=== "No Install (npx)"

    No installation needed! Just run:
    ```bash
    npx @superagenticai/acp-amp
    ```

### Running

```bash
# If installed globally
acp-amp

# Using npx (downloads automatically)
npx @superagenticai/acp-amp
```

### Verify Installation

```bash
# Check it runs (will wait for input, Ctrl+C to exit)
npx @superagenticai/acp-amp
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AMP_API_KEY` | Your Amp API key | Only if not using `amp login` |
| `ACP_AMP_DRIVER` | Default driver (`python`, `node`, `auto`) | No (Python version only) |
| `ACP_AMP_SHIM` | Custom path to Node shim | No |

### Using API Key

If you prefer using an API key instead of `amp login`:

```bash
export AMP_API_KEY="your-api-key-here"
acp-amp run
```

Or pass it directly:

```bash
AMP_API_KEY="your-api-key" acp-amp run
```

---

## Next Steps

Now that acp-amp is installed:

1. **[Set up Zed](zed.md)** — Configure Zed editor to use Amp
2. **[Configure other ACP clients](acp-clients.md)** — SuperQode, Toad, fast-agent
3. **[Troubleshooting](troubleshooting.md)** — If something doesn't work

---

## Quick Reference

### Python Commands

```bash
# Install
pip install acp-amp

# Run with Python SDK (default)
acp-amp run

# Run with Node shim fallback
acp-amp run --driver node

# Setup Node shim
acp-amp setup
```

### Node.js Commands

```bash
# Install globally
npm install -g @superagenticai/acp-amp

# Run
acp-amp

# Run without installing
npx @superagenticai/acp-amp
```
