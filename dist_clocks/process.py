import json
import socket
import multiprocessing as mp
from abc import ABC, abstractmethod


BASE_PORT = 6000  # base port to compute unique ports per process


class Process(ABC):
    def __init__(self, process_id, num_events=10):
        self.process_id = process_id
        self.num_events = num_events

        self.port = BASE_PORT + self.process_id
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # for dev #
        self.server.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # TIME_WAIT state
        ###########
        self.server.bind(("localhost", self.port))
        self.server.listen(5)

        self.os_process = mp.Process(target=self.run)

    # messages sent and received are "dicts" (simulating json)
    def send_message(self, recv_pid, msg):
        target_port = BASE_PORT + recv_pid
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", target_port))
            data = json.dumps(msg).encode("utf-8")
            s.sendall(data)

    def receive_message(self):
        self.server.settimeout(5.0)  # add timeout (in seconds)
        try:
            conn, _ = self.server.accept()
            with conn:
                data = conn.recv(4096)
                msg = json.loads(data.decode("utf-8"))
            return msg
        except socket.timeout:
            return None

    def start(self):
        self.os_process.start()

    def join(self):
        self.os_process.join()

    @abstractmethod
    def run(self):
        pass
