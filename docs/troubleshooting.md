# Troubleshooting

## Adapter does not start

- Check Python and Node versions
- Ensure `node-shim` dependencies are installed

## No output in client

- Make sure the client is not capturing stderr for protocol output
- The adapter writes ACP JSON-RPC to stdout only

## Authentication errors

- Set `AMP_API_KEY` in the client environment
- If you use Amp CLI auth, ensure it is logged in

## Cancellation does not stop

- The adapter sends a cancel to the shim; if Amp SDK ignores it, it may complete the turn anyway
