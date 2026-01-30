# acp-amp

![CI](https://github.com/SuperagenticAI/acp-amp/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

acp-amp is an open source ACP adapter for Amp Code. It runs as a standard ACP agent over stdin and stdout and can be used from any ACP client, for example Zed or SuperQode.

## Where you can use it

- Zed editor via `agent_servers`
- SuperQode via ACP agent config
- Any ACP client that can launch a subprocess and speak JSON-RPC over stdio

## Install (recommended)

```bash
uv tool install acp-amp
```

## Install (pip)

```bash
pip install acp-amp
```

## Install (dev)

```bash
pip install -e .
```

## Install with uv

```bash
uv sync
```

## Install Node shim deps

```bash
cd node-shim
npm install
```

## Run

```bash
acp-amp
```

## Tests

```bash
pip install -e .[test]
pytest
```

## Tests with uv

```bash
uv run pytest
```

## Docs

```bash
pip install -e .[docs]
mkdocs serve
```

## Docs with uv

```bash
uv run mkdocs serve
```

## Use from an ACP client (example: SuperQode)

```yaml
agents:
  amp:
    description: "Amp ACP adapter"
    protocol: acp
    command: acp-amp
    args: []
```

Then connect:

```bash
superqode connect acp amp
```

## Zed example

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

## Notes

- Stdout is reserved for ACP JSON-RPC messages, logs go to stderr
- The Node shim lives in `node-shim/` and is launched automatically
