import argparse
import sys

from ops_toolkit.config import load_config
from ops_toolkit.main import run_checks, run_loop


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ops-toolkit",
        description="Operations reliability toolkit for health checks and monitoring."
    )

    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Path to config YAML file"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run", help="Run continuous monitoring loop")
    subparsers.add_parser("check-now", help="Run checks once and exit")
    subparsers.add_parser("test-config", help="Validate config and exit")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "run":
            run_loop(args.config)
        elif args.command == "check-now":
            run_checks(args.config)
        elif args.command == "test-config":
            load_config(args.config)
            print(f"Config validation successful: {args.config}")
        else:
            parser.print_help()
            return 1

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())