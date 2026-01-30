# Getting Started

Choose your preferred version - Python or Node.js. Both provide the same Amp Code capabilities.

## Python Version

### Install

```bash
# Recommended
uv tool install acp-amp

# Or with pip
pip install acp-amp
```

### Run

```bash
acp-amp run
```

### Driver Options (Python only)

The Python version supports multiple drivers:

| Driver | Command | Description |
|--------|---------|-------------|
| `python` | `acp-amp run` | Uses `amp-sdk` Python package (default) |
| `node` | `acp-amp run --driver node` | Uses Node.js shim fallback |
| `auto` | `acp-amp run --driver auto` | Tries Python first, falls back to Node |

If using the Node shim fallback, first run:

```bash
acp-amp setup
cd ~/.acp-amp/shim
npm install
```

## Node.js Version

### Install

```bash
npm install -g @superagenticai/acp-amp
```

### Run

```bash
acp-amp
```

Or run directly with npx (no install needed):

```bash
npx @superagenticai/acp-amp
```

## Prerequisites

Both versions require:

- [Amp CLI](https://ampcode.com) installed and authenticated (`amp login`)

Version-specific:

- **Python**: Python 3.10+
- **Node.js**: Node.js 18+

### Install Amp CLI

```bash
npm install -g @sourcegraph/amp
amp login
```

## Connect from Your Client

Configure your ACP client to run the appropriate command:

**Python:**
```bash
acp-amp
```

**Node.js:**
```bash
npx @superagenticai/acp-amp
```

If your client supports environment variables:

```
AMP_API_KEY=your-api-key-here
```

## Next Steps

- [Zed Setup](zed.md) - Configure Zed editor
- [SuperQode Setup](superqode.md) - Configure SuperQode
- [Troubleshooting](troubleshooting.md) - Common issues
