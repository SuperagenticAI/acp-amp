# acp-amp

acp-amp is a clean-room ACP adapter for Amp Code. It runs as a standard ACP agent over stdin/stdout and can be used from any ACP client, for example Zed or SuperQode. We built it to bring Amp to Python based ACP clients and to extend Amp usage beyond TypeScript only setups. This lets Python driven coding agents such as Toad, fast-agent, SuperQode, and other ACP clients use Amp natively.

Python based ACP clients you can use today:

- Toad https://github.com/batrachianai/toad
- fast-agent https://github.com/evalstate/fast-agent
- SuperQode https://github.com/SuperagenticAI/superqode

The default driver uses the Amp Python SDK, with a Node shim fallback.

Highlights:

- Python ACP server with strict JSON-RPC over stdio
- Small Node shim for the closed-source Amp SDK
- Compatible with any ACP client that can launch a subprocess

## Quick links

- [Getting Started](getting-started.md)
- [Zed setup](zed.md)
- [SuperQode setup](superqode.md)
- [Generic ACP client notes](acp-clients.md)
- [Troubleshooting](troubleshooting.md)
