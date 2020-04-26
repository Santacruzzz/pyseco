#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
from struct import unpack, pack
from utils import *
from xmlrpc.client import *


class Client(BaseClient):
    def __init__(self, ip, port, logging_mode, listeners):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.request_num = 2147483648
        self.logger = Logger('Pyseco', logging_mode)
        self.__listeners = listeners
        self._events = []
        self.debug_data = None

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
                self.logger.debug('#### wait for {} bytes'.format(size - len(bytes_received)))
        return bytes_received.decode('utf-8')

    def _read_any_message(self):
        return self._read_message(None)

    def _read_message(self, wait_for_number):
        while True:
            size, request_number = self._read_message_info()
            self.logger.debug('<- READ LEN={}, NUM={}'.format(size, request_number))
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
        self.logger.info('Connected, protocol: {}'.format(protocol_version))
        if self.getStatus().code != 4:
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
            self.logger.debug(f'{event.event_name}: {event.data}')
            if event.event_name and '.' in event.event_name:
                event.event_name = event.event_name.split('.')[1]
                self.logger.debug('Event: {}'.format(event))
        except UnicodeDecodeError as ex:
            self.logger.debug('Parsing xml failed. ({})'.format(str(ex)))
        except Exception as ex:
            self.logger.error('Error during handling event. ({})'.format(str(ex)))
            return

        for listener in self.__listeners:
            # if listener has implemented method event.event_name
            if event.event_name in dir(listener):
                if len(event.data) > 0:
                    getattr(listener, event.event_name)(*event.data)
                else:
                    getattr(listener, event.event_name)()

    def serverMessage(self, msg):
        self.noresponse.ChatSendServerMessage(f'${self.debug_data["color"]}~ $888{msg}')

    def __no_response_request(self, methodname, params):
        request = dumps(params, methodname)
        self.request_num += 1
        self.logger.debug(f'-> sending {methodname}')
        self._send_request(request)

    def disconnect(self):
        self.serverMessage('pyseco disconnected')
        self.sock.close()
        self.logger.info('Disconnected')

    def __getattr__(self, name):
        msg = Method(self.__request, name, self.logger)
        if name == 'noresponse':
            msg.set_send(self.__no_response_request)
        events = len(self._events)
        self.logger.debug('events queue size = {}'.format(events))
        self._handle_buffered_events()
        return msg

    def _handle_buffered_events(self):
        self.logger.debug(f'Handling buffered {len(self._events)} event(s)')
        while self._events:
            event = self._events.pop(0)
            self.logger.debug('Pop event from queue')
            self._handle_event(event)

    def __request(self, methodname, params):
        request = dumps(params, methodname)
        try:
            self.request_num += 1
            self.logger.debug('-> sending request: {}, num: {}'.format(methodname, self.request_num))
            self._send_request(request)
            resp = self._read_message(self.request_num)
            try:
                response = loads(resp)[0][0]
            except Fault as ex:
                self.logger.error(str(ex))
                response = False
            self.logger.debug('<- received response: {}'.format(response))
            return response

        except BrokenPipeError:
            self.logger.error('Connection lost')
            self.request_num -= 1
            raise

    def set_debug_data(self, data):
        self.debug_data = data

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()


class Method:
    def __init__(self, send, name, logger):
        self.__send = send
        self.__name = name
        self.logger = Logger(f'Method.{name}', logger.get_logging_mode())

    def set_send(self, send):
        self.__send = send

    def __getattr__(self, name):
        return Method(self.__send, f'{self.__name}.{name}', self.logger)

    def __call__(self, *args):
        self.logger.debug('calling')
        if 'noresponse.' in self.__name:
            self.__name = self.__name.replace('noresponse.', '')
        return self.__send(self.__name, args)
