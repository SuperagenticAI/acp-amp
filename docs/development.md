# Development

## Tests

```bash
pip install -e .[test]
pytest
```

## Tests with uv

```bash
uv run pytest
```

## Node shim protocol

The Python adapter talks to the shim over NDJSON:

- `start` to begin a prompt stream
- `cancel` to abort a prompt

See `node-shim/README.md` for the full message schema.
