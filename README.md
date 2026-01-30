# acp-amp

Clean-room ACP adapter for Amp Code. It runs as a standard ACP agent over stdin and stdout and can be used from any ACP client, for example Zed or SuperQode.

## Install (dev)

```bash
pip install -e .
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

## Docs

```bash
pip install -e .[docs]
mkdocs serve
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
