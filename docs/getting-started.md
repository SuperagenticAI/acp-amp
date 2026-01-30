# Getting Started (simple)

This is the shortest path to run **acp-amp**. We built it to bring Amp to Python based ACP clients and to extend Amp usage beyond TypeScript only setups. The default driver uses the Amp Python SDK, with a Node shim fallback.

Python based ACP clients you can use today:

- Toad https://github.com/batrachianai/toad
- fast-agent https://github.com/evalstate/fast-agent
- SuperQode https://github.com/SuperagenticAI/superqode

## 1) Install (recommended)

```bash
uv tool install acp-amp
```

## 1b) Install with pip

```bash
pip install acp-amp
```

## 2) Install Amp CLI if needed

Some Amp setups require the Amp CLI. If your SDK setup needs it, install:

```bash
npm install -g @sourcegraph/amp
```

## 2b) Optional Node shim (fallback)

If you installed from PyPI and do not have the source code, run:

```bash
acp-amp setup
```

This creates the shim files in `~/.acp-amp/shim`.

Then install the shim dependencies:

```bash
cd ~/.acp-amp/shim
npm install
```

## 2c) Install Node shim from the repo

```bash
cd node-shim
npm install
```

## 3) Run the agent

```bash
acp-amp
```

By default the Python SDK driver is used. To force the Node shim:

```bash
acp-amp run --driver node
```

## 3b) Run with uv

```bash
uv run acp-amp
```

## 3c) Force the Python SDK explicitly

```bash
acp-amp run --driver python
```

## 4) Connect from your client

Tell your ACP client to run the `acp-amp` command.
If the client supports environment variables, set:

```
AMP_API_KEY=your-api-key-here
```

## Custom shim path (optional)

If your shim is not at `node-shim/index.js`, set:

```bash
ACP_AMP_SHIM=/path/to/index.js acp-amp
```
