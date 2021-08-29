import socket
from multiprocessing.queues import Queue
from struct import unpack, pack
from src.includes.log import setup_logger
from src.includes.config import Config

logger = setup_logger(__name__)


class Transport():
    def __init__(self, config: Config, events_queue: Queue):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = config
        self.request_num = 0x80000000
        self.events_queue = events_queue

    def _read_response(self, expected_request_number):
        while True:
            size, request_number = self._read_message_info()
            msg = self._receive(size)

            if not expected_request_number or request_number == expected_request_number:
                return msg
            else:
                logger.debug(f'Queue event, current size = {self.events_queue.qsize()}')
                self.events_queue.put(msg)

    def _read_init_resp_size(self):
        return unpack('<L', self.sock.recv(4))[0]

    def _read_message_info(self):
        return unpack('<LL', self.sock.recv(8))

    def _pack_message(self, msg):
        encoded_message = msg.encode('utf-8')
        preamble = pack('<LL', len(encoded_message), self.request_num)
        return b''.join([preamble, encoded_message])

    def _receive(self, size):
        bytes_received = bytearray()
        while len(bytes_received) < size:
            bytes_received.extend(self.sock.recv(size - len(bytes_received)))
            if len(bytes_received) < size:
                bytes_left = size - len(bytes_received)
                logger.debug(f'waiting for next {bytes_left} byte(s)')
        return bytes_received.decode('utf-8')

    def send_request(self, request):
        try:
            self.request_num += 1
            self.sock.sendall(self._pack_message(request))
        except BrokenPipeError:
            self.request_num -= 1
            raise

    def disconnect(self):
        self.sock.close()

    def get_any_message(self):
        return self._read_response(None)

    def get_response(self):
        return self._read_response(self.request_num)

    def connect(self):
        logger.debug('connecting')
        self.sock.connect((self.config.rpc_ip, self.config.rpc_port))
        data_length = self._read_init_resp_size()
        protocol_version = self._receive(data_length)
        logger.info(f'Connected, protocol used: {protocol_version}')
