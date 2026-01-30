# Development

## Tests

```bash
pip install -e .[test]
pytest
```

## Node shim protocol

The Python adapter talks to the shim over NDJSON:

- `start` to begin a prompt stream
- `cancel` to abort a prompt

See `node-shim/README.md` for the full message schema.
