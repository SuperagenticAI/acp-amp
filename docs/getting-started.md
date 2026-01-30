# Getting Started (simple)

This is the shortest path to run **acp-amp**.

## 1) Install (recommended)

```bash
uv tool install acp-amp
```

## 1b) Install with pip

```bash
pip install acp-amp
```

## 2) Install Node shim

```bash
cd node-shim
npm install
```

## 3) Run the agent

```bash
acp-amp
```

## 3b) Run with uv

```bash
uv run acp-amp
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
