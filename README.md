# acp-amp

![CI](https://github.com/SuperagenticAI/acp-amp/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

acp-amp is an open source ACP adapter for Amp Code. It runs as a standard ACP agent over stdin and stdout and can be used from any ACP client, for example Zed or SuperQode. We built it to bring Amp to Python based ACP clients and to extend Amp usage beyond TypeScript only setups. This lets Python driven coding agents such as Toad, fast-agent, SuperQode, and other ACP clients use Amp natively.

In short, acp-amp bridges Amp into the ACP ecosystem and keeps the protocol surface clean and consistent for editors and clients. The default driver uses the Amp Python SDK, with a Node shim fallback.

## Where you can use it

- Zed editor via `agent_servers`
- SuperQode via ACP agent config
- Any ACP client that can launch a subprocess and speak JSON-RPC over stdio

Python based ACP clients you can use today:

- Toad https://github.com/batrachianai/toad
- fast-agent https://github.com/evalstate/fast-agent
- SuperQode https://github.com/SuperagenticAI/superqode

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

## Install Amp CLI if needed

Some Amp setups require the Amp CLI. If your SDK setup needs it, install:

```bash
npm install -g @sourcegraph/amp
```

## Optional Node shim fallback

If you cannot use the Python SDK, you can run the Node shim instead.

```bash
acp-amp setup
cd ~/.acp-amp/shim
npm install
```

## Run

```bash
acp-amp
```

By default the Python SDK driver is used. To force the Node shim:

```bash
acp-amp run --driver node
```

To force the Python SDK explicitly:

```bash
acp-amp run --driver python
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
