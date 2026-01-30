from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from acp.core import run_agent

from acp_amp.driver.node_sdk import NodeAmpDriver
from acp_amp.driver.python_sdk import PythonAmpDriver
from acp_amp.server import AmpAcpAgent
from acp_amp.shim import ensure_shim_dir, default_shim_dir, shim_paths


def _default_shim_path() -> Path | None:
    env_path = os.environ.get("ACP_AMP_SHIM")
    if env_path:
        return Path(env_path)

    user_shim = default_shim_dir() / "index.js"
    if user_shim.exists():
        return user_shim

    # Try repo-local layout: acp_amp/../node-shim/index.js
    here = Path(__file__).resolve()
    candidate = here.parent.parent / "node-shim" / "index.js"
    if candidate.exists():
        return candidate

    return None


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ACP adapter for Amp Code")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run the ACP adapter")
    run_parser.add_argument(
        "--driver",
        choices=["python", "node", "auto"],
        default=os.environ.get("ACP_AMP_DRIVER", "auto"),
        help="Amp SDK driver to use (default: auto)",
    )
    run_parser.add_argument(
        "--node",
        default=os.environ.get("ACP_AMP_NODE", "node"),
        help="Node.js executable (default: node)",
    )
    run_parser.add_argument(
        "--shim",
        default=str(_default_shim_path() or ""),
        help="Path to the Node shim (default: auto-detect or ACP_AMP_SHIM)",
    )

    setup_parser = subparsers.add_parser("setup", help="Create the local Node shim files")
    setup_parser.add_argument(
        "--path",
        default=str(default_shim_dir()),
        help="Directory to write the shim files (default: ~/.acp-amp/shim)",
    )

    return parser.parse_args()


async def _run() -> None:
    args = _parse_args()
    if args.command == "setup":
        shim_dir = Path(args.path).expanduser()
        ensure_shim_dir(shim_dir)
        index_js, package_json = shim_paths(shim_dir)
        print(f"Shim files written to {shim_dir}")
        print("Install dependencies with:")
        print(f"  cd {shim_dir} && npm install")
        print("Then run:")
        print("  acp-amp run")
        return

    if args.command in (None, "run"):
        driver_choice = args.driver if args.command == "run" else "auto"
        driver = None
        if driver_choice in ("python", "auto"):
            try:
                driver = PythonAmpDriver()
            except Exception:
                if driver_choice == "python":
                    raise
        if driver is None:
            node_cmd = args.node if args.command == "run" else os.environ.get("ACP_AMP_NODE", "node")
            shim = args.shim if args.command == "run" else str(_default_shim_path() or "")
            if not shim:
                raise SystemExit("ACP AMP: node shim not found; run `acp-amp setup` or set ACP_AMP_SHIM")
            driver = NodeAmpDriver(node_cmd=node_cmd, shim_path=Path(shim))
        agent = AmpAcpAgent(driver)
        await run_agent(agent)


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
