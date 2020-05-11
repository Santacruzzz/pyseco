import logging
from colorama import init
from termcolor import colored

init()
COLORS = {
    'WARNING': ('yellow',),
    'INFO': ('white', 'on_blue'),
    'DEBUG': ('blue',),
    'CRITICAL': ('white', 'on_red'),
    'ERROR': ('red',)
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        # call format method to fill record object
        logging.Formatter.format(self, record)

        date_time = record.asctime
        func_name = colored(record.funcName, 'white', attrs=['bold'])
        message = record.message
        file_name = f'{record.filename}:{str(record.lineno)}'
        levelname = record.levelname

        if self.use_color and levelname in COLORS:
            levelname = colored(levelname, *COLORS[levelname])
            date_time = colored(date_time, 'magenta', attrs=['dark'])
            message = message.replace('<-', colored('<-', 'green')).replace('->', colored('->', 'red'))
            file_name = colored(file_name, 'green', attrs=['dark'])

        return '{} {:35}{}: {} ({})'.format(date_time, func_name, levelname, message, file_name)


class ColoredLogger(logging.Logger):
    FORMAT = "%(asctime)s:$BOLD%(funcName)-18s$RESET%(levelname)s %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"

    def __init__(self, name, level, use_color=True):
        logging.Logger.__init__(self, name, level)
        color_formatter = ColoredFormatter(self.FORMAT, use_color)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
