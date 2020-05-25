from unittest.mock import call

import pytest

from src.api.tm_requests import XmlRpc, RpcMulticall
from src.api.tm_types import Status


@pytest.fixture
def transport(mocker):
    return mocker.patch('src.api.tm_requests.Transport')


@pytest.fixture
def rpc_multicall(mocker):
    return mocker.patch('src.api.tm_requests.RpcMulticall')


@pytest.fixture
def multicall(mocker):
    return mocker.patch('src.api.tm_requests.MultiCall')


@pytest.fixture
def method(mocker):
    return mocker.patch('src.api.tm_requests.Method')


def test_should_create_rpc_object(transport, rpc_multicall):
    XmlRpc(transport.return_value)
    rpc_multicall.assert_not_called()


def test_should_create_rpc_as_multicall(transport, rpc_multicall):
    rpc = XmlRpc(transport.return_value, True)
    rpc_multicall.assert_called_once_with(rpc)


def test_should_getattr_from_method_on_default_rpc_call(method, transport):
    rpc = XmlRpc(transport.return_value)
    rpc.get_status()

    method.assert_called_once_with(transport.return_value, 'GetStatus')
    method.return_value.assert_called_once()


def test_should_getattr_from_multicall_when_multicall_requested(method, transport, rpc_multicall):
    rpc = XmlRpc(transport.return_value, True)
    rpc.get_status()

    method.assert_not_called()
    rpc_multicall.assert_called_once_with(rpc)
    rpc_multicall.return_value.GetStatus.assert_called_once()


def test_should_exec_multicall_when_multicall_requested_only(transport, multicall):
    rpc = XmlRpc(transport.return_value, True)
    rpc.get_status()

    multicall.return_value.return_value = []
    dummy_param = None
    rpc.exec_multicall(dummy_param)

    multicall.assert_called_once_with(rpc)
    multicall.return_value.GetStatus.assert_called_once()
    multicall.return_value.assert_called_once()


@pytest.mark.parametrize('types, methods, return_values, expected', [
    (
            (Status, Status, Status),                       # types
            ['get_status', 'get_status', 'get_status'],     # methods
            [                                               # return_values
                {'Code': 1, 'Name': 'name1'},
                {'Code': 2, 'Name': 'name2'},
                {'Code': 3, 'Name': 'name3'}
            ],
            [                                               # expected
                Status({'Code': 1, 'Name': 'name1'}),
                Status({'Code': 2, 'Name': 'name2'}),
                Status({'Code': 3, 'Name': 'name3'})
            ]
    ),
    (
            (Status, bool, int),                                        # types
            ['get_status', 'start_server_lan', 'get_referee_mode'],     # methods
            [{'Code': 1, 'Name': 'name1'}, True, 1337],                 # return_values
            [Status({'Code': 1, 'Name': 'name1'}), True, 1337]          # expected
    )
])
def test_exec_multicall_should_return_expected_types(types, methods, return_values, expected, transport, multicall):
    rpc = XmlRpc(transport.return_value, True)
    [getattr(rpc, method)() for method in methods]
    multicall.return_value.return_value = return_values

    results = rpc.exec_multicall(*types)

    for expectation, result in zip(expected, results):
        assert expectation == result

