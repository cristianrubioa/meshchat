import asyncio
from datetime import datetime

import pytest

from chatserver.core.message import Message
from chatserver.core.room import Room


def test_room_initialization():
    room = Room(
        name="Test Room",
        max_users=10,
        enable_history=True,
        history_size=50,
        plain_text=False,
    )
    assert room.name == "Test Room"
    assert room.max_users == 10
    assert room.enable_history
    assert room.history_size == 50


def test_nickname_reservation():
    room = Room("Test", 10, False, 50, False)
    assert room.reserve_nickname("Alice")
    assert not room.reserve_nickname("Alice")


def test_room_history():
    room = Room("Test", 10, True, 5, False)

    msg1 = Message("Alice", "Hello", datetime.now())
    msg2 = Message("Bob", "Hi", datetime.now())

    room.history.append(msg1)
    room.history.append(msg2)

    history = room.get_history()
    assert len(history) == 2
    assert history[0] == msg1
    assert history[1] == msg2


def test_room_history_max_size():
    room = Room("Test", 10, True, 3, False)

    for i in range(5):
        msg = Message("Alice", f"Message {i}", datetime.now())
        room.history.append(msg)

    assert len(room.history) == 3

    history = room.get_history()
    assert "Message 2" in history[0].content
    assert "Message 4" in history[2].content


def test_room_no_history():
    room = Room("Test", 10, False, 50, False)

    msg = Message("Alice", "Hello", datetime.now())
    room.history.append(msg)

    assert not room.enable_history


def test_room_user_list():
    room = Room("Test", 10, False, 50, False)

    room.reserve_nickname("Alice")
    room.reserve_nickname("Bob")

    users = room.get_user_list()
    assert len(users) == 2
    assert "Alice" in users
    assert "Bob" in users


@pytest.mark.asyncio
async def test_room_start_stop():
    room = Room("Test", 10, False, 50, False)

    room.start()
    assert room._running

    await room.stop()
    assert not room._running


@pytest.mark.asyncio
async def test_room_broadcast():
    room = Room("Test", 10, True, 50, False)
    room.start()

    msg = Message("Alice", "Hello", datetime.now())
    await room.broadcast(msg)

    await asyncio.sleep(0.1)

    assert len(room.history) == 1
    assert room.history[0] == msg

    await room.stop()


@pytest.mark.asyncio
async def test_room_join_leave():
    room = Room("Test", 2, False, 50, False)
    room.start()

    class MockClient:
        def __init__(self, nickname):
            self.nickname = nickname
            self.full_room_rejection = False

    client1 = MockClient("Alice")
    await room.join(client1)

    assert "Alice" in room.clients
    assert room.clients["Alice"] == client1

    await room.leave(client1)
    assert "Alice" not in room.clients

    await room.stop()


@pytest.mark.asyncio
async def test_room_max_users():
    room = Room("Test", 2, False, 50, False)
    room.start()

    class MockClient:
        def __init__(self, nickname):
            self.nickname = nickname
            self.full_room_rejection = False

    client1 = MockClient("Alice")
    client2 = MockClient("Bob")
    client3 = MockClient("Charlie")

    await room.join(client1)
    await room.join(client2)
    await room.join(client3)

    assert client3.full_room_rejection

    await room.stop()
