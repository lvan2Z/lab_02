import argparse
import logging
import sys

from .errors import StreamStatsError
from .models import parse_event
from .parsers import get_parser
from .analysis import Stats
from .report import write_report


def main():
    parser = argparse.ArgumentParser(prog="streamstats")
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze")
    analyze.add_argument("inputs", nargs="+")
    analyze.add_argument("--format", required=True, choices=["csv", "jsonl"])
    analyze.add_argument("--output")
    analyze.add_argument("--skip-invalid", action="store_true")

    args = parser.parse_args()

    if args.command != "analyze":
        parser.print_help()
        sys.exit(1)

    if args.skip_invalid:
        logging.basicConfig(level=logging.WARNING, format="WARNING: %(message)s")

    parser_fn = get_parser(args.format)
    stats = Stats()

    for filename in args.inputs:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line_number, row in parser_fn(f, file_name=filename):
                    try:
                        event = parse_event(row, file_name=filename, line_number=line_number)
                        stats.add_event(event)
                    except StreamStatsError as e:
                        if args.skip_invalid:
                            logging.warning(str(e))
                            stats.skip_invalid()
                        else:
                            print(f"Error: {e}", file=sys.stderr)
                            sys.exit(2)
        except FileNotFoundError:
            print(f"File not found: {filename}", file=sys.stderr)
            sys.exit(2)
        except StreamStatsError as e:
            if args.skip_invalid:
                logging.warning(str(e))
                stats.skip_invalid()
            else:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(2)

    if args.output:
        write_report(stats, args.output)
        print(f"Report written to {args.output}")
    else:
        print(f"Total events: {stats.total_events}")
        print(f"Skipped invalid lines: {stats.skipped_invalid_lines}")


if __name__ == "__main__":
    main()