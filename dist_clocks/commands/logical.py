from ..log import setup_logging
from ..clocks.logical_clock import LogicalProcess


logger = setup_logging()


def add_parser(subparsers):
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

    return logical_parser


def run(n_processes, n_events):
    logger.info(
        f"Starting logical clock simulation with {n_processes} processes & {n_events} events per process."
    )
    processes = []
    for i in range(n_processes):
        process = LogicalProcess(
            process_id=i,
            num_processes=n_processes,
            num_events=n_events,
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
