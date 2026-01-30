from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from acp.core import run_agent

from acp_amp.driver.node_sdk import NodeAmpDriver
from acp_amp.server import AmpAcpAgent


def _default_shim_path() -> Path | None:
    env_path = os.environ.get("ACP_AMP_SHIM")
    if env_path:
        return Path(env_path)

    # Try repo-local layout: acp_amp/../node-shim/index.js
    here = Path(__file__).resolve()
    candidate = here.parent.parent / "node-shim" / "index.js"
    if candidate.exists():
        return candidate

    return None


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ACP adapter for Amp Code")
    parser.add_argument(
        "--node",
        default=os.environ.get("ACP_AMP_NODE", "node"),
        help="Node.js executable (default: node)",
    )
    parser.add_argument(
        "--shim",
        default=str(_default_shim_path() or ""),
        help="Path to the Node shim (default: auto-detect or ACP_AMP_SHIM)",
    )
    return parser.parse_args()


async def _run() -> None:
    args = _parse_args()
    if not args.shim:
        raise SystemExit("ACP AMP: node shim not found; set ACP_AMP_SHIM or --shim")

    driver = NodeAmpDriver(node_cmd=args.node, shim_path=Path(args.shim))
    agent = AmpAcpAgent(driver)
    await run_agent(agent)


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
