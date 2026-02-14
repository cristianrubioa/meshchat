import pytest
import asyncio
from datetime import datetime
from chatserver.core.message import Message
from chatserver.core.room import Room
from chatserver.core.exceptions import (
    NicknameTakenError,
    MessageTooLongError,
    RateLimitError,
    RoomFullError,
)


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


def test_exception_with_parameters():
    error = NicknameTakenError("Alice")
    assert "Alice" in str(error)


def test_message_too_long_error():
    error = MessageTooLongError()
    assert "long" in str(error).lower()


def test_rate_limit_error():
    error = RateLimitError()
    assert "quickly" in str(error).lower() or "rate" in str(error).lower()


def test_room_full_error():
    error = RoomFullError()
    assert "full" in str(error).lower()


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


def test_formatter_ansi_user_list():
    from chatserver.ui.formatter import Formatter
    
    formatter = Formatter(plain_text=False)
    users = ["Alice", "Bob"]
    user_list = formatter.format_user_list("Test", users, 10)
    
    assert "\033[" in user_list
    assert "Test" in user_list
    assert "Alice" in user_list


def test_formatter_ansi_welcome():
    from chatserver.ui.formatter import Formatter
    
    formatter = Formatter(plain_text=False)
    welcome = formatter.format_welcome_message("Test", "Alice")
    
    assert "\033[" in welcome
    assert "Test" in welcome
    assert "Alice" in welcome


def test_formatter_ansi_help():
    from chatserver.ui.formatter import Formatter
    
    formatter = Formatter(plain_text=False)
    help_msg = formatter.format_help()
    
    assert "\033[" in help_msg
    assert "/who" in help_msg
