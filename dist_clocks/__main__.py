import argparse

from .log_utils import setup_logging
from .logical_process import LogicalProcess


logger = setup_logging()


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
            logger.info(
                f"Starting logical clock simulation with {args.n_processes} processes & {args.n_events} events per process."
            )
            processes = []
            for i in range(args.n_processes):
                process = LogicalProcess(
                    process_id=i,
                    num_processes=args.n_processes,
                    num_events=args.n_events,
                )
                processes.append(process)
                logger.debug(f"LogicalProcess {i} initialized.")

            for process in processes:
                process.start()
                logger.debug(f"LogicalProcess {process.process_id} started.")

            # TODO: seems wrong
            for process in processes:
                process.join()
                logger.debug(f"LogicalProcess {process.process_id} finished.")

            logger.info("Logical clock simulation finished.\n")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
