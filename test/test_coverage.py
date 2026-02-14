import pytest
from datetime import datetime
from chatserver.core.message import Message
from chatserver.core.room import Room
from chatserver.ui.formatter import Formatter, get_user_color
from chatserver.core.validators import validate_nickname
from chatserver.core.exceptions import (
    NicknameEmptyError,
    NicknameTooShortError,
    NicknameTooLongError,
    NicknameReservedError,
    NicknameInvalidCharsError,
)
from chatserver.config import get_settings


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


def test_action_message():
    msg = Message(
        from_user="Alice",
        content="waves",
        timestamp=datetime.now(),
        is_action=True
    )
    assert msg.is_action
    assert not msg.is_system


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


def test_room_user_list():
    room = Room("Test", 10, False, 50, False)
    
    room.reserve_nickname("Alice")
    room.reserve_nickname("Bob")
    
    users = room.get_user_list()
    assert len(users) == 2
    assert "Alice" in users
    assert "Bob" in users


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


def test_formatter_action():
    formatter = Formatter(plain_text=True)
    action = formatter.format_action_message("Alice", "waves")
    assert action == "* Alice waves"
    
    formatter_ansi = Formatter(plain_text=False)
    action_ansi = formatter_ansi.format_action_message("Alice", "waves")
    assert "Alice" in action_ansi
    assert "waves" in action_ansi


def test_formatter_title():
    formatter = Formatter(plain_text=True)
    title = formatter.format_title("Welcome")
    assert title == "=== Welcome ==="
    
    formatter_ansi = Formatter(plain_text=False)
    title_ansi = formatter_ansi.format_title("Welcome")
    assert "Welcome" in title_ansi


def test_formatter_banner():
    formatter = Formatter(plain_text=True)
    banner = formatter.format_banner("TEST")
    assert banner == "TEST"


def test_formatter_help():
    formatter = Formatter(plain_text=True)
    help_msg = formatter.format_help()
    assert "/who" in help_msg
    assert "/me" in help_msg
    assert "/help" in help_msg
    assert "/quit" in help_msg


def test_formatter_user_list():
    formatter = Formatter(plain_text=True)
    users = ["Alice", "Bob", "Charlie"]
    user_list = formatter.format_user_list("Test Room", users, 10)
    assert "Test Room" in user_list
    assert "(3/10)" in user_list
    assert "Alice" in user_list
    assert "Bob" in user_list
    assert "Charlie" in user_list


def test_formatter_welcome():
    formatter = Formatter(plain_text=True)
    welcome = formatter.format_welcome_message("Test Room", "Alice")
    assert "Test Room" in welcome
    assert "Alice" in welcome


def test_user_color_consistency():
    color1 = get_user_color("Alice")
    color2 = get_user_color("Alice")
    color3 = get_user_color("Bob")
    
    assert color1 == color2
    assert color1 != color3


def test_user_color_different_users():
    colors = set()
    names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace", "Henry"]
    
    for name in names:
        colors.add(get_user_color(name))
    
    assert len(colors) > 3


def test_validate_nickname_empty():
    with pytest.raises(NicknameEmptyError):
        validate_nickname("")


def test_validate_nickname_too_short():
    with pytest.raises(NicknameTooShortError):
        validate_nickname("a")


def test_validate_nickname_too_long():
    with pytest.raises(NicknameTooLongError):
        validate_nickname("a" * 25)


def test_validate_nickname_reserved():
    with pytest.raises(NicknameReservedError):
        validate_nickname("system")
    
    with pytest.raises(NicknameReservedError):
        validate_nickname("System")
    
    with pytest.raises(NicknameReservedError):
        validate_nickname("SYSTEM")


def test_validate_nickname_invalid_chars():
    with pytest.raises(NicknameInvalidCharsError):
        validate_nickname("alice!")
    
    with pytest.raises(NicknameInvalidCharsError):
        validate_nickname("alice@bob")
    
    with pytest.raises(NicknameInvalidCharsError):
        validate_nickname("alice bob")


def test_validate_nickname_valid():
    validate_nickname("alice")
    validate_nickname("alice123")
    validate_nickname("alice_bob")
    validate_nickname("alice-bob")
    validate_nickname("Alice")
    validate_nickname("Alice123")


def test_config_settings():
    settings = get_settings()
    
    assert settings.host == "0.0.0.0"
    assert settings.port == 2323
    assert settings.room_name == "Chat Room"
    assert settings.max_users == 10
    assert settings.max_message_length == 1000
    assert settings.rate_limit_max_messages == 5
    assert settings.rate_limit_window_seconds == 5
    assert settings.max_nickname_len == 20
    assert settings.min_nickname_len == 2


def test_exception_messages():
    assert "empty" in str(NicknameEmptyError()).lower()
    assert "least" in str(NicknameTooShortError()).lower()
    assert "most" in str(NicknameTooLongError()).lower()
    assert "reserved" in str(NicknameReservedError()).lower()
    assert "only contain" in str(NicknameInvalidCharsError()).lower()
