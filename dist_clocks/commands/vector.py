from ..log import setup_logging
from ..clocks.vector_clock import VectorProcess

logger = setup_logging()


def add_parser(subparsers):
    vector_parser = subparsers.add_parser("vector", help="Run Vector Clock simulation")
    vector_parser.add_argument(
        "--n_processes",
        "-p",
        type=int,
        default=3,
        help="Number of processes to simulate.",
    )
    vector_parser.add_argument(
        "--n_events",
        "-e",
        type=int,
        default=10,
        help="Number of events per process that will occur.",
    )
    return vector_parser


def run(n_processes, n_events):
    logger.info(
        f"Starting vector clock simulation with {n_processes} processes & {n_events} events per process."
    )
    processes = []
    for i in range(n_processes):
        process = VectorProcess(
            process_id=i,
            num_processes=n_processes,
            num_events=n_events,
        )
        processes.append(process)
        logger.debug(f"VectorProcess {i} initialized.")

    for process in processes:
        process.start()
        logger.debug(f"VectorProcess {process.process_id} started.")

    # TODO: seems wrong
    for process in processes:
        process.join()
        logger.debug(f"VectorProcess {process.process_id} finished.")

    logger.info("Vector clock simulation finished.\n")
