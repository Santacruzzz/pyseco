import abc
import pytest
from collections import namedtuple
from unittest.mock import Mock, call, MagicMock
from random import randint
from src.errors import NotAnEvent, EventDiscarded
from src.listener import Listener
from src.pyseco import Pyseco


DummyEventData = namedtuple('DummyEventData', ['name', 'data'])
DummyEvent = namedtuple('DummyEvent', ['name'])
DefaultParams = namedtuple('DefaultParams', ['login', 'password', 'ip', 'port'])
DEFAULT_PARAMS = DefaultParams('login', 'password', 'ip', 1234)
CallAssert = namedtuple('CallAssert', ['call', 'params'])
TM_FOREVER = 1


class Events:
    EVENT1 = DummyEvent('EVENT1')
    EVENT2 = DummyEvent('EVENT2')
    EVENT3 = DummyEvent('EVENT3')
    EVENT4 = DummyEvent('EVENT4')
    EVENT5 = DummyEvent('EVENT5')


class DummyListener(Listener):
    def __init__(self, mocker):
        super().__init__('dummy_listener', Mock())
        self.on_dummy_event1 = mocker.stub(name='on_dummy_event1_stub')
        self.on_dummy_event2 = mocker.stub(name='on_dummy_event2_stub')
        self.on_dummy_event3 = mocker.stub(name='on_dummy_event3_stub')
        self.on_dummy_event4 = mocker.stub(name='on_dummy_event4_stub')
        self.on_dummy_event5 = mocker.stub(name='on_dummy_event5_stub')


def request_call(name, *params):
    return call(name, params)


# .assert_called_with(Any(str, int))
def Any(*cls):
    class AnyComparator(metaclass=abc.ABCMeta):
        def __eq__(self, other):
            return isinstance(other, cls)
    for c in cls:
        AnyComparator.register(c)
    return AnyComparator()


def random_data():
    return randint(0, 500), randint(0, 500)


def make_event(ev):
    return DummyEventData(name=ev.name, data=random_data())


def make_empty_event(ev):
    return DummyEventData(name=ev.name, data=None)


@pytest.fixture(autouse=True)
def client(mocker):
    return mocker.patch('src.APIs.trackmania_api.Client').return_value


@pytest.fixture(autouse=True)
def no_listeners(mocker):
    mocker.patch('src.pyseco.Pyseco._register_listeners')


@pytest.fixture
def pyseco(mocker):
    mocker.patch('src.pyseco.is_bound').return_value = True
    pyseco = Pyseco(*DEFAULT_PARAMS)
    pyseco.debug_data = {'color': '$fff'}
    return pyseco


def test_should_create_object(mocker):
    client_mock = mocker.patch('src.APIs.trackmania_api.Client')
    pyseco = Pyseco(*DEFAULT_PARAMS)
    client_mock.assert_called_once_with(DEFAULT_PARAMS.ip, DEFAULT_PARAMS.port, pyseco)


def test_should_disconnect_on_exit(client):
    with Pyseco(*DEFAULT_PARAMS):
        client.return_value.disconnect.assert_not_called()
    client.disconnect.assert_called_once()


def test_events_map_should_be_empty_when_no_listeners_registered():
    pyseco = Pyseco(*DEFAULT_PARAMS)
    assert len(pyseco.events_map) == 0


def test_should_sync_data_on_run(client, pyseco):
    pyseco.run()
    client.connect.assert_called_once()

    assert client.request.call_args_list == [
        request_call('Authenticate', DEFAULT_PARAMS.login, DEFAULT_PARAMS.password),
        request_call('ChatSendServerMessage', Any(str)),
        request_call('EnableCallbacks', True),
        request_call('GetVersion'),
        request_call('GetServerOptions', TM_FOREVER),
        request_call('GetSystemInfo'),
        request_call('GetDetailedPlayerInfo', Any(str)),
        request_call('GetLadderServerLimits'),
        request_call('GetGameInfos', TM_FOREVER),
        request_call('GetPlayerList', Any(int), Any(int), TM_FOREVER),
        request_call('GetCurrentChallengeInfo'),
        request_call('ChatSendServerMessage', Any(str)),
        request_call('GetNextChallengeInfo')
    ]

    client.loop.assert_called_once()


def test_an_exception_other_than_keyboardinterrupt_should_be_passed_further(client, pyseco):
    client.request.side_effect = [True, True, Exception]
    with pytest.raises(Exception):
        pyseco.run()


def test_should_send_disconnect_message_on_keyboardinterrupt(client, pyseco):
    client.request.side_effect = [True, KeyboardInterrupt]
    pyseco.run()
    assert client.request.call_args_list == [
        request_call('Authenticate', DEFAULT_PARAMS.login, DEFAULT_PARAMS.password),
        request_call('ChatSendServerMessage', Any(str)),
    ]


def test_should_add_registered_listener_to_events_map(mocker, pyseco):
    mocker.patch('src.pyseco.is_bound').return_value = True
    listener = DummyListener(mocker)
    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    assert listener.on_dummy_event1 in pyseco.events_map[Events.EVENT1.name]


def test_only_registered_listener_method_should_be_called_on_event(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    event = make_event(Events.EVENT1)
    prepare_event.return_value = event
    pyseco.handle_event(None)
    listener.on_dummy_event1.assert_called_with(event.data)
    listener.on_dummy_event2.assert_not_called()
    listener.on_dummy_event3.assert_not_called()
    listener.on_dummy_event4.assert_not_called()
    listener.on_dummy_event5.assert_not_called()


def test_registered_method_should_be_without_params_on_empty_event(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    event = make_empty_event(Events.EVENT1)
    prepare_event.return_value = event
    pyseco.handle_event(None)
    listener.on_dummy_event1.assert_called_with()


def test_method_registered_multiple_times_should_be_called_once(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)

    event = make_event(Events.EVENT1)
    prepare_event.return_value = event
    pyseco.handle_event(None)

    listener.on_dummy_event1.assert_called_once()
    listener.on_dummy_event1.assert_called_with(event.data)


def test_listener_should_be_called_multiple_times_on_multiple_events(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    events_queue = [make_event(Events.EVENT1), make_event(Events.EVENT1), make_event(Events.EVENT1)]
    prepare_event.side_effect = events_queue
    [pyseco.handle_event(None) for _ in events_queue]

    listener.on_dummy_event1.assert_has_calls([call(event.data) for event in events_queue])


def test_multiple_listeners_registered_for_one_event(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener1 = DummyListener(mocker)
    listener2 = DummyListener(mocker)
    listener3 = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener1.on_dummy_event1)
    pyseco.register(Events.EVENT1.name, listener2.on_dummy_event1)
    pyseco.register(Events.EVENT1.name, listener3.on_dummy_event1)

    event = make_event(Events.EVENT1)
    prepare_event.return_value = event
    pyseco.handle_event(None)

    listener1.on_dummy_event1.assert_called_with(event.data)
    listener2.on_dummy_event1.assert_called_with(event.data)
    listener3.on_dummy_event1.assert_called_with(event.data)


def test_multiple_methods_registered_for_one_event(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    pyseco.register(Events.EVENT2.name, listener.on_dummy_event2)
    pyseco.register(Events.EVENT3.name, listener.on_dummy_event3)

    events_queue = [make_event(Events.EVENT1), make_event(Events.EVENT2), make_event(Events.EVENT3)]
    prepare_event.side_effect = events_queue
    [pyseco.handle_event(None) for _ in events_queue]

    listener.on_dummy_event1.assert_called_with(events_queue[0].data)
    listener.on_dummy_event2.assert_called_with(events_queue[1].data)
    listener.on_dummy_event3.assert_called_with(events_queue[2].data)


def test_should_not_call_method_on_exception_raised(mocker, pyseco):
    prepare_event = mocker.patch.object(pyseco, '_prepare_event')
    listener = DummyListener(mocker)

    pyseco.register(Events.EVENT1.name, listener.on_dummy_event1)
    pyseco.register(Events.EVENT2.name, listener.on_dummy_event2)
    pyseco.register(Events.EVENT3.name, listener.on_dummy_event3)
    pyseco.register(Events.EVENT4.name, listener.on_dummy_event4)
    pyseco.register(Events.EVENT5.name, listener.on_dummy_event5)

    events_queue = [make_event(Events.EVENT1),
                    NotAnEvent,
                    EventDiscarded,
                    make_empty_event(Events.EVENT4),
                    make_event(Events.EVENT5)]
    prepare_event.side_effect = events_queue
    [pyseco.handle_event(None) for _ in events_queue]

    listener.on_dummy_event1.assert_called_with(events_queue[0].data)
    listener.on_dummy_event2.assert_not_called()
    listener.on_dummy_event3.assert_not_called()
    listener.on_dummy_event4.assert_called_with()
    listener.on_dummy_event5.assert_called_with(events_queue[4].data)
