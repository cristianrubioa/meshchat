from datetime import datetime
from chatserver.core.message import Message
from chatserver.core.room import Room
from chatserver.ui.formatter import Formatter, get_user_color


def test_message_creation():
    msg = Message(
        from_user="Alice",
        content="Hello",
        timestamp=datetime.now()
    )
    assert msg.from_user == "Alice"
    assert msg.content == "Hello"
    assert not msg.is_system
    assert not msg.is_action


def test_system_message():
    msg = Message(
        from_user="System",
        content="User joined",
        timestamp=datetime.now(),
        is_system=True
    )
    assert msg.is_system


def test_room_initialization():
    room = Room(
        name="Test Room",
        max_users=10,
        enable_history=True,
        history_size=50,
        plain_text=False
    )
    assert room.name == "Test Room"
    assert room.max_users == 10
    assert room.enable_history
    assert room.history_size == 50


def test_nickname_reservation():
    room = Room("Test", 10, False, 50, False)
    
    assert room.reserve_nickname("Alice")
    
    assert not room.reserve_nickname("Alice")


def test_formatter_plain_text():
    formatter = Formatter(plain_text=True)
    
    msg = formatter.format_system_message("Test")
    assert msg == "[System] Test"
    
    user_msg = formatter.format_user_message("Alice", "Hello", "12:00:00")
    assert user_msg == "[12:00:00] Alice: Hello"


def test_formatter_ansi():
    formatter = Formatter(plain_text=False)
    
    msg = formatter.format_system_message("Test")
    assert "[System]" in msg
    assert "\033[" in msg
    
    user_msg = formatter.format_user_message("Alice", "Hello", "12:00:00")
    assert "Alice" in user_msg
    assert "\033[" in user_msg


def test_user_color_consistency():
    color1 = get_user_color("Alice")
    color2 = get_user_color("Alice")
    color3 = get_user_color("Bob")
    
    assert color1 == color2
    assert color1 != color3
