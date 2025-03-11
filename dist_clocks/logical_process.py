import random
from time import sleep

from .process import Process
from .log_utils import setup_logging


logger = setup_logging()


# process implemented with a logical clock
class LogicalProcess(Process):
    def __init__(self, process_id, num_processes, num_events=10):
        super().__init__(process_id, num_events)
        self.num_processes = num_processes  # number of processes in the pool
        self.clock: int = 0

    def run(self):
        logger.debug(
            f"LogicalProcess {self.process_id} starting run with {self.num_events} events"
        )
        for _ in range(self.num_events):
            event = random.choice(["INTERNAL", "SEND", "RECV"])
            logger.debug(f"LogicalProcess {self.process_id} selected event: {event}")

            sleep(random.uniform(0.0, 1.5))

            match event:
                case "SEND":
                    logger.debug(
                        f"LogicalProcess {self.process_id} preparing to send message"
                    )
                    prev_clock = self.clock

                    self.clock += 1
                    # PIDs start from 0
                    recv_pid = random.choice(
                        [
                            pid
                            for pid in range(self.num_processes)
                            if pid != self.process_id
                        ]
                    )

                    msg = {
                        "send_pid": self.process_id,
                        "clock": self.clock,
                        "message": "ack",
                    }
                    super().send_message(recv_pid, msg)

                    logger.debug(
                        f"LogicalProcess {self.process_id} sent message: {msg}"
                    )
                    logger.info(
                        f"PID: {self.process_id}; {event} to {recv_pid}; CLK: {prev_clock} -> {self.clock}"
                    )

                case "RECV":
                    logger.debug(
                        f"LogicalProcess {self.process_id} waiting to receive message"
                    )
                    prev_clock = self.clock

                    msg: dict | None = super().receive_message()
                    if msg is None:
                        self.clock += 1
                        logger.info(
                            f"PID: {self.process_id}; INTERNAL: RECV timed out; CLK: {prev_clock} -> {self.clock}"
                        )
                        continue

                    self.clock = max(self.clock, msg["clock"]) + 1

                    logger.debug(
                        f"LogicalProcess {self.process_id} received message {msg}"
                    )
                    logger.info(
                        f"PID: {self.process_id}; {event} from {msg['send_pid']}; CLK: {prev_clock} -> {self.clock}"
                    )

                case "INTERNAL":
                    logger.debug(
                        f"LogicalProcess {self.process_id} executing internal event"
                    )
                    prev_clock = self.clock
                    self.clock += 1

                    logger.info(
                        f"PID: {self.process_id}; {event}; CLK: {prev_clock} -> {self.clock}"
                    )
