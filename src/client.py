import time
from queue import Queue
from xmlrpc.client import loads, dumps, Fault
from src.includes.log import setup_logger
from src.transport import Transport

logger = setup_logger(__name__)


class Client:
    def __init__(self, ip, port, pyseco):
        self.events_queue = Queue()
        self.pyseco = pyseco
        self.transport = Transport(ip, port, self.events_queue)

    def _handle_buffered_events(self):
        logger.debug(f'Handling buffered {self.events_queue.qsize()} event(s)')
        while self.events_queue.qsize():
            self.pyseco.handle_event(self.events_queue.get())

    def no_response_request(self, method_name, params):
        request = dumps(params, method_name)
        logger.debug(f'-> sending {method_name}')
        self.transport.send_request(request)

    def request(self, method_name, params):
        request = dumps(params, method_name)
        try:
            time_start = time.time()
            request_num = self.transport.send_request(request)
            logger.debug(f'-> request sent: {method_name}, num: {request_num}')
            resp = self.transport.get_response()
            time_end = time.time()
            try:
                response = loads(resp)[0][0]
            except Fault as ex:
                logger.error(str(ex))
                response = False
            logger.debug('<- received response: {}, took: {:.2f} ms'.format(response, (time_end - time_start) * 1000))
            return response
        except BrokenPipeError as ex:
            logger.error(ex)
            raise

    def connect(self):
        try:
            self.transport.connect()
            status = self.pyseco.get_status()
            while status.code != 4:
                logger.info(f'Server is not ready: {status.name}')
                time.sleep(5)
                status = self.pyseco.get_status()
        except BrokenPipeError as ex:
            logger.error(ex)
            raise

    def loop(self):
        logger.info('Waiting for events...')
        while True:
            if self.events_queue.qsize():
                self._handle_buffered_events()
            self.pyseco.handle_event(self.transport.get_any_message())

    def disconnect(self):
        try:
            self.transport.disconnect()
            logger.info('Disconnected')
        except Exception as ex:
            logger.error(ex)
