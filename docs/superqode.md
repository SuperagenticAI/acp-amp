# SuperQode

SuperQode can connect to any ACP agent by spawning the adapter command.

## Example config

```yaml
agents:
  amp:
    description: "Amp ACP adapter"
    protocol: acp
    command: acp-amp
    args: []
```

Connect from the CLI:

```bash
superqode connect acp amp
```
