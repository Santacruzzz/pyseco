import socket
import logging
from struct import unpack, pack
from src.errors import NotAnEvent, EventDiscarded, PysecoException
from src.includes.events import EVENTS_MAP
from xmlrpc.client import *
from queue import Queue
from src.APIs.trackmania_api import TrackmaniaAPI

logger = logging.getLogger(__name__)


class Client(TrackmaniaAPI):
    def __init__(self, ip, port, events_map):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.request_num = 2147483648
        self._events_map = events_map
        self._events_queue = Queue()
        self.debug_data = None

    def __getattr__(self, name):
        method = Method(self._request, name)
        if name == 'noresponse':
            method.set_send(self._no_response_request)
        return method

    def _read_init_resp_size(self):
        return unpack('<L', self.sock.recv(4))[0]

    def _read_message_info(self):
        return unpack('<LL', self.sock.recv(8))

    def _send_request(self, request):
        self.sock.sendall(self._pack_message(request))

    def _recv_decoded(self, size):
        bytes_received = bytearray()
        while len(bytes_received) < size:
            bytes_received.extend(self.sock.recv(size - len(bytes_received)))
            if len(bytes_received) < size:
                bytes_left = size - len(bytes_received)
                logger.debug(f'waiting for next {bytes_left} byte(s)')
        return bytes_received.decode('utf-8')

    def _read_any_message(self):
        return self._read_message(None)

    def _read_message(self, wait_for_number):
        while True:
            size, request_number = self._read_message_info()
            logger.debug(f'<- READ LEN={size}, NUM={request_number}')
            msg = self._recv_decoded(size)

            if not wait_for_number:
                return msg

            if request_number == wait_for_number:
                return msg
            else:
                logger.debug(f'Putting event to queue, size before={self._events_queue.qsize()}')
                self._events_queue.put(msg)

    def _pack_message(self, msg):
        # server expects 8 bytes preamble, [4 bytes for msg size, 4 bytes for request number, *content]
        encoded_message = msg.encode('utf-8')
        preamble = pack('<LL', len(encoded_message), self.request_num)
        return b''.join([preamble, encoded_message])

    def _prepare_event(self, msg):
        payload, name = loads(msg)
        event = EVENTS_MAP.get(name)
        data = event(*payload) if payload else None

        if not name:
            # TODO this is an side effect of noresponse method which should be deleted
            # if parsed xml has no "methodName" (second field in tuple) then this is a response
            # which belongs to noresponse.Request and should be discarded
            raise NotAnEvent('Not an event')

        if event.name not in self._events_map:
            raise EventDiscarded(f'No action registered for {event.name}. Data: {data}')

        return data, event.name

    def _handle_event(self, msg):
        try:
            payload, event = self._prepare_event(msg)

            logger.debug(f'{event} Data: {payload}')
            if event in self._events_map:
                for listener_method in self._events_map[event]:
                    if payload:
                        listener_method(payload)
                    else:
                        listener_method()

        except PysecoException as ex:
            logger.debug(f'Event discarded: {ex}')
        except UnicodeDecodeError as ex:
            logger.debug(f'Parsing xml failed. ({ex})')

    def _no_response_request(self, methodname, params):
        request = dumps(params, methodname)
        self.request_num += 1
        logger.debug(f'-> sending {methodname}')
        self._send_request(request)

    def _request(self, methodname, params):
        request = dumps(params, methodname)
        try:
            self.request_num += 1
            logger.debug(f'-> sending request: {methodname}, num: {self.request_num}')
            self._send_request(request)
            resp = self._read_message(self.request_num)
            try:
                response = loads(resp)[0][0]
            except Fault as ex:
                logger.error(str(ex))
                response = False
            logger.debug(f'<- received response: {response}')
            return response
        except BrokenPipeError:
            logger.error('Connection lost')
            self.request_num -= 1
            raise

    def _handle_buffered_events(self):
        logger.debug(f'Handling buffered {self._events_queue.qsize()} event(s)')
        while self._events_queue.qsize():
            self._handle_event(self._events_queue.get())

    def connect(self):
        try:
            self.sock.connect((self.ip, self.port))
            data_length = self._read_init_resp_size()
            protocol_version = self._recv_decoded(data_length)
            logger.info(f'Connected, protocol used: {protocol_version}')
            if self.get_status().code != 4:
                logger.error("Server is not ready yet.")
        except BrokenPipeError as ex:
            logger.error(ex)
            raise

    def loop(self):
        logger.info('Waiting for events...')
        while True:
            if self._events_queue.qsize():
                self._handle_buffered_events()
            self._handle_event(self._read_any_message())

    def server_message(self, msg):
        self.ChatSendServerMessage(f'${self.debug_data["color"]}~ $888{msg}')

    def disconnect(self):
        try:
            self.server_message('pyseco disconnected')
            self.sock.close()
            logger.info('Disconnected')
        except Exception as ex:
            logger.error(ex)

    def set_debug_data(self, data):
        self.debug_data = data


class Method:
    def __init__(self, send, name):
        self._send = send
        self._name = name

    def __getattr__(self, name):
        return Method(self._send, f'{self._name}.{name}')

    def __call__(self, *args):
        logger.debug(f'calling {self._name}')
        if 'noresponse.' in self._name:
            self._name = self._name.replace('noresponse.', '')
        return self._send(self._name, args)

    def set_send(self, send):
        self._send = send
