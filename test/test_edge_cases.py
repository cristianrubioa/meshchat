import pytest
from chatserver.ui.banner import BANNER


def test_banner_exists():
    assert BANNER is not None
    assert len(BANNER) > 0
    assert "╔" in BANNER


def test_banner_format():
    assert "╔" in BANNER
    assert "║" in BANNER
    assert "╚" in BANNER


def test_formatter_banner_ansi():
    from chatserver.ui.formatter import Formatter
    
    formatter = Formatter(plain_text=False)
    formatted = formatter.format_banner(BANNER)
    
    assert "\033[" in formatted
    assert BANNER in formatted or "Chat" in formatted


def test_room_operations():
    from chatserver.core.room import Room
    
    room = Room("Test", 5, True, 10, False)
    
    room.reserve_nickname("Alice")
    users = room.get_user_list()
    assert "Alice" in users
    
    assert not room.reserve_nickname("Alice")
    
    assert room.reserve_nickname("Bob")


def test_multiple_color_users():
    from chatserver.ui.formatter import get_user_color
    
    users = ["alice", "bob", "charlie", "dan", "eve"]
    colors = [get_user_color(u) for u in users]
    
    unique_colors = set(colors)
    assert len(unique_colors) >= 3


def test_edge_case_nicknames():
    from chatserver.core.validators import validate_nickname
    from chatserver.core.exceptions import NicknameInvalidCharsError
    
    validate_nickname("ab")
    validate_nickname("a" * 20)
    validate_nickname("user123")
    validate_nickname("user_name")
    validate_nickname("user-name")
    
    with pytest.raises(NicknameInvalidCharsError):
        validate_nickname("user name")
    
    with pytest.raises(NicknameInvalidCharsError):
        validate_nickname("user@name")


def test_config_immutable():
    from chatserver.config import get_settings
    
    settings1 = get_settings()
    settings2 = get_settings()
    
    assert settings1 is settings2
