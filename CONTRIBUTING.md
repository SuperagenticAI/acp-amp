# Contributing

Thanks for your interest in acp-amp.

## Development setup

1. Install Python 3.10 or newer
2. Install Node.js 18 or newer
3. Install package and test deps

```bash
pip install -e .[test]
```

4. Install the Node shim dependencies

```bash
cd node-shim
npm install
```

## Tests

```bash
pytest
```

## Pull request checklist

- Keep stdout reserved for ACP JSON-RPC
- Keep logs on stderr
- Add tests for mapping or protocol changes
- Update docs in `docs/` when behavior changes
