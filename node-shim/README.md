# ACP AMP Node Shim

This shim wraps the closed-source Amp SDK and streams events over NDJSON to the Python ACP adapter.

## Install dependencies

```bash
cd node-shim
npm install
```

## Protocol (NDJSON)

Requests from Python:

- `{"type":"start","id":"...","prompt":"...","cwd":"...","allowAll":false,"mcpConfig":{},"threadId":null}`
- `{"type":"cancel","id":"..."}`

Responses to Python:

- `{"type":"event","id":"...","event":{...}}`
- `{"type":"done","id":"...","stopReason":"end_turn"}`
- `{"type":"error","id":"...","error":{"message":"..."}}`
