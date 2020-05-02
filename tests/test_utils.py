import pytest
from src.utils import CommandParser
from src.errors import WrongCommand


class DummyClassWithCommands:
    def kick(self):
        pass

    def ban(self):
        pass

    def kill(self):
        pass

    def ask_me(self):
        pass


class TestCommandParser:
    @pytest.mark.parametrize('_class,input_command,expected', [
        (DummyClassWithCommands, '  *kick user', ('kick', ('user',))),
        (DummyClassWithCommands, ' *ask_me about various params   ', ('ask_me', ('about', 'various', 'params'))),
        (DummyClassWithCommands, ' *kill     ', ('kill', ())),
        (DummyClassWithCommands, ' ****ban user_with_underscore_in_nickname',
         ('ban', ('user_with_underscore_in_nickname',)))
    ])
    def test_should_give_correct_params(self, _class, input_command, expected):
        assert CommandParser.parser_regex(_class, input_command) == expected

    @pytest.mark.parametrize('_class,input_command,expected', [
        (DummyClassWithCommands, '  *ask_me "about this message" param',
         ('ask_me', ('about this message', 'param',))),
        (DummyClassWithCommands, '*kick user "message in the middle" param next_param',
         ('kick', ('user', 'message in the middle', 'param', 'next_param')))
    ])
    def test_should_have_not_split_message(self, _class, input_command, expected):
        assert CommandParser.parser_regex(_class, input_command) == expected

    def test_should_raise_wrong_command(self):
        with pytest.raises(WrongCommand):
            CommandParser.parser_regex(DummyClassWithCommands, '*unexcpected_command')
