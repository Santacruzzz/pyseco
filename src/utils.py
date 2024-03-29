import inspect
import re
import shlex

from src.errors import WrongCommand


class CommandParser:
    @staticmethod
    def get_defined_methods_names(_class):
        return "|".join(name for name, value in inspect.getmembers(_class, predicate=inspect.isfunction)
                        if not name.startswith('_'))

    @staticmethod
    def parser_regex(_class, user_command):
        command_regex = fr'[\*]({CommandParser.get_defined_methods_names(_class)})([\"\w\s]*)'
        hit_string = re.search(command_regex, user_command)
        if hit_string:
            command, params = hit_string.group(1), hit_string.group(2)
            return command, tuple(shlex.split(params))
        else:
            raise WrongCommand("Used wrong command")


def strip_size(text):
    return re.sub(r'(?<!\$)\$[iwosn]|(?<!\$)\$l\[\S*\]', '', text)


def strip_nickname(nickname):
    return re.sub(r'(?<!\$)\$[0-9a-fA-F]{3}', '', strip_size(nickname))


def is_bound(m):
    return hasattr(m, '__self__')
