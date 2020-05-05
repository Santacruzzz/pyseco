import socket
from struct import unpack, pack
from src.includes.log import setup_logger

logger = setup_logger(__name__)


class Transport:
    def __init__(self, ip, port, events_queue):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.request_num = 0x80000000
        self.events_queue = events_queue

    def _read_response(self, wait_for_number):
        while True:
            size, request_number = self.read_message_info()
            logger.debug(f'READ LEN={size}, NUM={request_number}')
            msg = self.recv_decoded(size)

            if not wait_for_number or request_number == wait_for_number:
                return msg
            else:
                logger.debug(f'Putting event to queue, size before={self.events_queue.qsize()}')
                self.events_queue.put(msg)

    def read_init_resp_size(self):
        return unpack('<L', self.sock.recv(4))[0]

    def read_message_info(self):
        return unpack('<LL', self.sock.recv(8))

    def send_request(self, request) -> int:
        """Returns request number"""
        try:
            self.request_num += 1
            self.sock.sendall(self.pack_message(request))
            return self.request_num
        except BrokenPipeError:
            self.request_num -= 1
            raise

    def pack_message(self, msg):
        encoded_message = msg.encode('utf-8')
        preamble = pack('<LL', len(encoded_message), self.request_num)
        return b''.join([preamble, encoded_message])

    def recv_decoded(self, size):
        bytes_received = bytearray()
        while len(bytes_received) < size:
            bytes_received.extend(self.sock.recv(size - len(bytes_received)))
            if len(bytes_received) < size:
                bytes_left = size - len(bytes_received)
                logger.debug(f'waiting for next {bytes_left} byte(s)')
        return bytes_received.decode('utf-8')

    def disconnect(self):
        self.sock.close()

    def get_any_message(self):
        return self._read_response(None)

    def get_response(self):
        return self._read_response(self.request_num)

    def connect(self):
        logger.debug('connecting')
        self.sock.connect((self.ip, self.port))
        data_length = self.read_init_resp_size()
        protocol_version = self.recv_decoded(data_length)
        logger.info(f'Connected, protocol used: {protocol_version}')
