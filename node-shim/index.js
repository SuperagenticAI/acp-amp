#!/usr/bin/env node
// stdout reserved for NDJSON protocol; log to stderr.
console.log = console.error;
console.info = console.error;
console.warn = console.error;
console.debug = console.error;

import { createInterface } from "node:readline";
import { execute } from "@sourcegraph/amp-sdk";

const sessions = new Map();

function write(msg) {
  process.stdout.write(JSON.stringify(msg) + "\n");
}

async function handleStart(msg) {
  const id = String(msg.id ?? "");
  if (!id) return;

  const controller = new AbortController();
  sessions.set(id, controller);

  const options = {
    cwd: msg.cwd || process.cwd(),
  };

  if (msg.allowAll) {
    options.dangerouslyAllowAll = true;
  }

  if (msg.mcpConfig && Object.keys(msg.mcpConfig).length > 0) {
    options.mcpConfig = msg.mcpConfig;
  }

  if (msg.threadId) {
    options.continue = msg.threadId;
  }

  let cancelled = false;

  try {
    for await (const event of execute({ prompt: msg.prompt || "", options, signal: controller.signal })) {
      write({ type: "event", id, event });
    }
  } catch (err) {
    if (controller.signal.aborted) {
      cancelled = true;
    } else {
      write({ type: "error", id, error: { message: String(err?.message || err) } });
      sessions.delete(id);
      return;
    }
  }

  write({ type: "done", id, stopReason: cancelled ? "cancelled" : "end_turn" });
  sessions.delete(id);
}

function handleCancel(msg) {
  const id = String(msg.id ?? "");
  const controller = sessions.get(id);
  if (controller) {
    controller.abort();
  }
}

const rl = createInterface({ input: process.stdin, crlfDelay: Infinity });
rl.on("line", (line) => {
  if (!line.trim()) return;
  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    return;
  }

  if (msg.type === "start") {
    handleStart(msg);
    return;
  }

  if (msg.type === "cancel") {
    handleCancel(msg);
    return;
  }
});
