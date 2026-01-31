# Development

This guide covers setting up a development environment for contributing to acp-amp.

---

## Project Structure

```
acp-amp/
├── acp_amp/              # Python package
│   ├── __init__.py
│   ├── cli.py            # Command-line interface
│   ├── server.py         # ACP server implementation
│   ├── shim.py           # Node shim template
│   ├── driver/
│   │   ├── base.py       # Driver base class
│   │   ├── python_sdk.py # Python SDK driver
│   │   └── node_sdk.py   # Node shim driver
│   └── mapping/
│       ├── to_acp.py     # Amp → ACP conversion
│       └── to_amp.py     # ACP → Amp conversion
├── node/                 # Node.js package
│   ├── package.json
│   └── src/
│       ├── index.js      # Entry point
│       ├── run-acp.js    # ACP connection
│       ├── server.js     # Agent implementation
│       ├── to-acp.js     # Event conversion
│       └── utils.js      # Stream utilities
├── node-shim/            # Minimal shim for --driver node
├── tests/                # Python tests
├── docs/                 # Documentation
├── pyproject.toml        # Python package config
└── mkdocs.yml            # Documentation config
```

---

## Python Development

### Setup

```bash
# Clone the repo
git clone https://github.com/SuperagenticAI/acp-amp.git
cd acp-amp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode
pip install -e .[test,docs]
```

### With uv

```bash
# Clone and setup
git clone https://github.com/SuperagenticAI/acp-amp.git
cd acp-amp

# Install dependencies
uv sync

# Run commands
uv run acp-amp --help
uv run pytest
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=acp_amp

# Specific test
pytest tests/test_server.py -v

# With uv
uv run pytest
```

### Code Style

```bash
# Format code
black acp_amp tests

# Sort imports
isort acp_amp tests

# Lint
ruff check acp_amp tests

# Type check
mypy acp_amp
```

### Building

```bash
# Build package
python -m build

# Check package
twine check dist/*
```

---

## Node.js Development

### Setup

```bash
cd node
npm install
```

### Running

```bash
# Run directly
node src/index.js

# Using npm
npm start
```

### Testing

```bash
npm test
```

### Linting

```bash
npm run lint
```

### Building for npm

```bash
# Check what will be published
npm pack --dry-run

# Publish (requires npm login)
npm publish --access public
```

---

## Documentation

### Setup

```bash
pip install -e .[docs]
# or
uv sync
```

### Local Development

```bash
# Start local server
mkdocs serve

# Visit http://localhost:8000
```

### Building

```bash
mkdocs build
# Output in site/
```

### Deploying

Documentation is automatically deployed to GitHub Pages on push to main.

Manual deploy:

```bash
mkdocs gh-deploy
```

---

## Node Shim Protocol

The Python adapter communicates with the Node shim via NDJSON over stdin/stdout.

### Messages

**Start a prompt:**

```json
{
  "type": "start",
  "id": "request-123",
  "prompt": "Explain this code",
  "cwd": "/path/to/project",
  "allowAll": false,
  "mcpConfig": {},
  "threadId": null
}
```

**Cancel a prompt:**

```json
{
  "type": "cancel",
  "id": "request-123"
}
```

### Responses

**Event (streaming):**

```json
{
  "type": "event",
  "id": "request-123",
  "event": { ... }
}
```

**Done:**

```json
{
  "type": "done",
  "id": "request-123",
  "stopReason": "end_turn"
}
```

**Error:**

```json
{
  "type": "error",
  "id": "request-123",
  "error": { "message": "Something went wrong" }
}
```

---

## Adding a New Driver

To add a new driver (e.g., for a different SDK):

### 1. Create the driver file

```python
# acp_amp/driver/my_sdk.py
from acp_amp.driver.base import AmpDriver, DriverCapabilities

class MySdkDriver(AmpDriver):
    capabilities = DriverCapabilities(
        supports_images=True,
        supports_embedded_context=True,
        supports_mcp_http=True,
        supports_mcp_sse=True,
    )

    async def start(self) -> None:
        # Initialize SDK
        pass

    async def close(self) -> None:
        # Cleanup
        pass

    async def stream_prompt(self, *, prompt, cwd, allow_all, mcp_config, thread_id, request_id):
        # Yield events
        yield {"type": "event", "id": request_id, "event": {...}}
        yield {"type": "done", "id": request_id, "stopReason": "end_turn"}

    async def cancel(self, request_id: str) -> None:
        # Cancel request
        pass
```

### 2. Register in cli.py

Add the driver to the `--driver` choices and instantiation logic.

---

## Releasing

### Python (PyPI)

```bash
# Update version in pyproject.toml
# Commit and tag
git tag v0.1.1
git push --tags

# Build and upload
python -m build
twine upload dist/*
```

### Node.js (npm)

```bash
cd node

# Update version in package.json
npm version patch  # or minor, major

# Publish
npm publish --access public
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests
5. Run tests: `pytest`
6. Commit: `git commit -m "Add my feature"`
7. Push: `git push origin feature/my-feature`
8. Open a Pull Request

### Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits focused
- Write clear commit messages
