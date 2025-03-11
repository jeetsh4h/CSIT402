import argparse

from .log import setup_logging
from .commands import logical, vector


logger = setup_logging()


def main():
    parser = argparse.ArgumentParser(description="Dist Clocks CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    logical_parser = logical.add_parser(subparsers)
    vector_parser = vector.add_parser(subparsers)

    args = parser.parse_args()

    match args.command:
        case "logical":
            logical.run(args.n_processes, args.n_events)

        case "vector":
            vector.run(args.n_processes, args.n_events)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
