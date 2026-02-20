"""
CLI - Argument parsing and command routing.
"""

import argparse
from .commands import cmd_status


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="School CLI - The Curriculum Resolver",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # status command
    status_parser = subparsers.add_parser("status", help="Show progress status")
    status_parser.add_argument(
        "--scope",
        choices=["total", "module", "campaign"],
        default="total",
        help="Scope of progress to display"
    )
    status_parser.add_argument(
        "--id",
        type=str,
        help="Specific module or campaign ID"
    )
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "status":
        cmd_status(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
