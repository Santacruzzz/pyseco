#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
from struct import unpack, pack
from utils import *
from xmlrpc.client import *

from APIs.trackmania_api import TrackmaniaAPI


class Client(TrackmaniaAPI):
    def __init__(self, ip, port, logging_mode, events_map):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.request_num = 2147483648
        self.logger = Logger('Pyseco', logging_mode)
        self._events_map = events_map
        self._events = []
        self.debug_data = None

    def __getattr__(self, name):
        msg = Method(self._request, name, self.logger)
        if name == 'noresponse':
            msg.set_send(self._no_response_request)
        self.logger.debug(f'current events queue size = {len(self._events)}')
        return msg

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

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
                self.logger.debug(f'waiting for next {bytes_left} byte(s)')
        return bytes_received.decode('utf-8')

    def _read_any_message(self):
        return self._read_message(None)

    def _read_message(self, wait_for_number):
        while True:
            size, request_number = self._read_message_info()
            self.logger.debug(f'<- READ LEN={size}, NUM={request_number}')
            msg = self._recv_decoded(size)

            if not wait_for_number:
                return msg

            if request_number == wait_for_number:
                return msg
            else:
                self.logger.debug(f'Putting event to queue, size before={len(self._events)}')
                self._events.append(msg)

    def _pack_message(self, msg):
        # server expects 8 bytes preamble, [4 bytes for msg size, 4 bytes for request number, *content]
        encoded_message = msg.encode('utf-8')
        preamble = pack('<LL', len(encoded_message), self.request_num)
        return b''.join([preamble, encoded_message])

    def connect(self):
        self.sock.connect((self.ip, self.port))
        data_length = self._read_init_resp_size()
        protocol_version = self._recv_decoded(data_length)
        self.logger.info(f'Connected, protocol used: {protocol_version}')
        if self.get_status().code != 4:
            self.logger.error("Server is not ready yet.")

    def loop(self):
        self._handle_buffered_events()
        self.logger.info('Waiting for events...')
        while True:
            self._handle_buffered_events()
            self._handle_event(self._read_any_message())

    def _handle_event(self, msg):
        try:
            event = EventData(*loads(msg))
            self.logger.debug(f'{event.name}: {event.data}')
        except UnicodeDecodeError as ex:
            self.logger.debug(f'Parsing xml failed. ({ex})')
            return
        except Exception as ex:
            self.logger.error(f'Error during handling event. ({ex})')
            return

        if event.name in self._events_map:
            for listener_method, event_type in self._events_map[event.name]:
                if event.data:
                    listener_method(event_type(*event.data))
                else:
                    listener_method()

    def server_message(self, msg):
        self.noresponse.ChatSendServerMessage(f'${self.debug_data["color"]}~ $888{msg}')

    def _no_response_request(self, methodname, params):
        request = dumps(params, methodname)
        self.request_num += 1
        self.logger.debug(f'-> sending {methodname}')
        self._send_request(request)

    def disconnect(self):
        self.server_message('pyseco disconnected')
        self.sock.close()
        self.logger.info('Disconnected')

    def _handle_buffered_events(self):
        self.logger.debug(f'Handling buffered {len(self._events)} event(s)')
        while self._events:
            event = self._events.pop(0)
            self.logger.debug('Pop event from queue')
            self._handle_event(event)

    def _request(self, methodname, params):
        request = dumps(params, methodname)
        try:
            self.request_num += 1
            self.logger.debug(f'-> sending request: {methodname}, num: {self.request_num}')
            self._send_request(request)
            resp = self._read_message(self.request_num)
            try:
                response = loads(resp)[0][0]
            except Fault as ex:
                self.logger.error(str(ex))
                response = False
            self.logger.debug(f'<- received response: {response}')
            return response
        except BrokenPipeError:
            self.logger.error('Connection lost')
            self.request_num -= 1
            raise

    def set_debug_data(self, data):
        self.debug_data = data


class Method:
    def __init__(self, send, name, logger):
        self._send = send
        self._name = name
        self.logger = Logger(f'Method.{name}', logger.get_logging_mode())

    def __getattr__(self, name):
        return Method(self._send, f'{self._name}.{name}', self.logger)

    def __call__(self, *args):
        self.logger.debug('calling')
        if 'noresponse.' in self._name:
            self._name = self._name.replace('noresponse.', '')
        return self._send(self._name, args)

    def set_send(self, send):
        self._send = send
