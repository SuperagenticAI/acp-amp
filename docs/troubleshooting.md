# Troubleshooting

Common issues and solutions for acp-amp.

---

## Installation Issues

### "pip: command not found"

Install Python first:

```bash
# macOS
brew install python

# Ubuntu/Debian
sudo apt install python3 python3-pip

# Or use uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install acp-amp
```

### "npm: command not found"

Install Node.js first:

```bash
# macOS
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### "acp-amp: command not found" (after pip install)

The install location might not be in your PATH:

```bash
# Find where it was installed
python -m site --user-base
# Usually: ~/.local/bin/acp-amp

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Or use the full path
~/.local/bin/acp-amp run
```

### "Permission denied" during install

Don't use sudo with pip. Instead:

```bash
# Use --user flag
pip install --user acp-amp

# Or use pipx/uv
pipx install acp-amp
uv tool install acp-amp
```

---

## Amp CLI Issues

### "amp: command not found"

Install the Amp CLI:

```bash
curl -fsSL https://ampcode.com/install.sh | bash
```

If still not found, check npm global bin path:

```bash
npm bin -g
# Add this to your PATH
```

### "Not authenticated" or "API key required"

Login to Amp:

```bash
amp login
```

Or provide an API key:

```bash
export AMP_API_KEY="your-api-key"
acp-amp run
```

### "Invalid API key"

1. Check your API key is correct
2. Try logging in again: `amp login`
3. Get a new key from [Amp settings](https://ampcode.com/settings)

---

## Python SDK Issues

### "'SystemMessage' object has no attribute 'get'"

This was a bug in older versions. Update to latest:

```bash
pip install --upgrade acp-amp
```

If it persists, use the Node shim fallback:

```bash
acp-amp run --driver node
```

### "amp-sdk is not installed"

The Python SDK should install automatically. If not:

```bash
pip install amp-sdk
```

### "No module named 'acp_amp'"

Reinstall the package:

```bash
pip uninstall acp-amp
pip install acp-amp
```

### Python version too old

acp-amp requires Python 3.10+:

```bash
python --version
# If < 3.10, upgrade Python
```

---

## Node Shim Issues

### "Cannot find module" errors

Install the shim dependencies:

```bash
acp-amp setup
cd ~/.acp-amp/shim
npm install
```

### "Node.js version too old"

acp-amp requires Node.js 18+:

```bash
node --version
# If < 18, upgrade Node.js
```

### Shim not found

Specify the shim path:

```bash
ACP_AMP_SHIM=/path/to/shim/index.js acp-amp run --driver node
```

---

## Zed Issues

### Agent doesn't appear in dropdown

1. Check your `settings.json` syntax
2. Make sure there are no trailing commas
3. Restart Zed completely (Cmd+Q / Ctrl+Q)

### "Failed to start agent"

1. Test the command manually:
   ```bash
   acp-amp run
   # or
   npx @superagenticai/acp-amp
   ```
2. Check Zed's output panel for errors
3. Use full path in settings

### Agent starts but no response

1. Make sure you're logged into Amp: `amp login`
2. Check if API key is set correctly in env
3. Check Zed's output panel for errors

### npx is slow on first run

First run downloads the package. For faster startup:

```bash
# Install globally instead
npm install -g @superagenticai/acp-amp
```

Then update Zed settings to use `acp-amp` instead of `npx`.

---

## Connection Issues

### "Connection refused" or timeout

1. Check internet connection
2. Try `amp login` to verify authentication
3. Check if Amp service is up

### "Stream closed unexpectedly"

1. Update to latest version
2. Check stderr output for errors
3. Try the other version (Python ↔ Node.js)

---

## Debugging

### Enable verbose output

```bash
# See what's happening
acp-amp run 2>&1 | tee debug.log
```

### Check stderr

Logs go to stderr, not stdout:

```bash
acp-amp run 2>error.log
cat error.log
```

### Test JSON-RPC manually

```bash
# Start acp-amp
acp-amp run

# In another terminal, send test message
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":1}}' | nc localhost 3000
```

### Zed logs

Check Zed's logs:

```bash
# macOS
tail -f ~/Library/Logs/Zed/Zed.log

# Linux
tail -f ~/.local/share/zed/logs/Zed.log
```

---

## Getting Help

If none of these solutions work:

1. **Check GitHub Issues**: [github.com/SuperagenticAI/acp-amp/issues](https://github.com/SuperagenticAI/acp-amp/issues)

2. **Open a new issue** with:
   - Your OS and version
   - Python/Node.js version
   - acp-amp version (`pip show acp-amp` or `npm list -g @superagenticai/acp-amp`)
   - Full error message
   - Steps to reproduce

3. **Community support**: 
   - [Amp Discord](https://discord.gg/ampcode)
   - [Zed Discord](https://discord.gg/zed)

---

## Version Information

Get version info for bug reports:

```bash
# Python version
pip show acp-amp
python --version

# Node.js version
npm list -g @superagenticai/acp-amp
node --version

# Amp CLI version
amp --version
```
