import os
from datetime import datetime

import inspect

# globals
DEBUG = 0
INFO = 1
NONE = 9


# classes
class EventData(object):
    def __init__(self, data, event_name: str):
        self.data = data
        self.event_name = event_name

    def __str__(self):
        return self.event_name


def _get_parent_function_name():
    # TODO sometimes throws an exception out of range blah blah
    return inspect.stack()[3][3]


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def red(txt):
        return f'\033[91m{txt}\033[0m'

    @staticmethod
    def green(txt):
        return f'\033[92m{txt}\033[0m'

    @staticmethod
    def blue(txt):
        return f'\033[94m{txt}\033[0m'


class Logger(object):
    CALLER_FUNCTION_DEPTH = 3


    def __init__(self, name: str = None, logging_mode: int = 0):
        self._name = name
        self._mode = logging_mode

    def __call__(self, msg):
        self.info(msg)

    def get_logging_mode(self):
        return self._mode

    def set_logging_mode(self, logging_mode):
        self._mode = logging_mode

    def set_name(self, name):
        self._name = name

    def _show(self, tag, msg):
        trace = self._get_trace()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        try:
            if self._name:
                print(f'{current_time} {tag}/{self._name}/{trace}: {msg}')
            else:
                print(f'{current_time} {tag}/{trace}: {msg}')
        except Exception as ex:
            self.error(str(ex))

    def set_mode(self, mode):
        self._mode = mode

    def info(self, msg):
        if self._mode <= INFO:
            self._show(Colors.green('INF'), msg)

    def debug(self, msg):
        if self._mode <= DEBUG:
            self._show(Colors.blue('DBG'), msg)

    def error(self, msg):
        if self._mode != NONE:
            self._show(Colors.red('ERR'), msg)

    def _get_trace(self):
        try:
            caller_function = inspect.stack()[self.CALLER_FUNCTION_DEPTH]
            file_name = os.path.basename(caller_function.filename)
            return f'{file_name}:{caller_function.lineno}/{caller_function.function}'
        except IndexError:
            return 'unknown_function'


def strip_size(text):
    return text.replace('$o', '').replace('$w', '')
