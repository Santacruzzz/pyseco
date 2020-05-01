import pytest
from src.pyseco import Pyseco
from typing import NamedTuple


class DefaultParams(NamedTuple):
    login: str
    password: str
    ip: str
    port: int


@pytest.fixture
def client(mocker):
    return mocker.patch('src.APIs.trackmania_api.Client')


@pytest.fixture
def no_listeners(mocker):
    mocker.patch('src.pyseco.Pyseco._register_listeners').return_value = None


@pytest.fixture
def default_params():
    return DefaultParams('login', 'password', 'ip', 1234)


def test_should_create_object(client, default_params, no_listeners):
    pyseco = Pyseco(*default_params)
    client.assert_called_once_with(default_params.ip, default_params.port, pyseco)


def test_should_disconnect_on_exit(client, default_params):
    with Pyseco(*default_params):
        client.return_value.disconnect.assert_not_called()
    client.return_value.disconnect.assert_called_once()


