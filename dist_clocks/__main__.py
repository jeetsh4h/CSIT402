import argparse

from .logical_process import LogicalProcess


def main():
    parser = argparse.ArgumentParser(description="Dist Clocks CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    logical_parser = subparsers.add_parser(
        "logical", help="Run Logical Clock simulation"
    )
    logical_parser.add_argument(
        "--n_processes",
        "-p",
        type=int,
        default=3,
        help="Number of processes to simulate.",
    )
    logical_parser.add_argument(
        "--n_events",
        "-e",
        type=int,
        default=10,
        help="Number of events per process that will occur.",
    )

    # Additional commands can be added here with more subparsers

    args = parser.parse_args()

    match args.command:
        case "logical":
            processes = []
            for i in range(args.n_processes):
                process = LogicalProcess(
                    process_id=i,
                    num_processes=args.n_processes,
                    num_events=args.n_events,
                )
                processes.append(process)

            for process in processes:
                process.start()

            for process in processes:
                process.join()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
