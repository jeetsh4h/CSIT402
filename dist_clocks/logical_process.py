import random
from time import sleep

from .process import Process


# process implemented with a logical clock
class LogicalProcess(Process):
    def __init__(self, process_id, num_processes, num_events=10):
        super().__init__(process_id, num_events)
        self.num_processes = num_processes  # number of processes in the pool
        self.clock: int = 0

    def run(self):
        for _ in range(self.num_events):
            event = random.choice(["INTERNAL", "SEND", "RECV"])

            sleep(random.uniform(0.0, 1.5))

            match event:
                case "SEND":
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

                    print(
                        f"PID: {self.process_id}; {event} to {recv_pid}; CLK: {prev_clock} -> {self.clock}"
                    )

                case "RECV":
                    prev_clock = self.clock

                    msg: dict | None = super().receive_message()
                    if msg is None:
                        self.clock += 1
                        print(
                            f"PID: {self.process_id}; INTERNAL: RECV timed out; CLK: {prev_clock} -> {self.clock}"
                        )
                        continue

                    self.clock = max(self.clock, msg["clock"]) + 1

                    print(
                        f"PID: {self.process_id}; {event} from {msg['send_pid']}; CLK: {prev_clock} -> {self.clock}"
                    )

                case "INTERNAL":
                    prev_clock = self.clock
                    self.clock += 1

                    print(
                        f"PID: {self.process_id}; {event}; CLK: {prev_clock} -> {self.clock}"
                    )
