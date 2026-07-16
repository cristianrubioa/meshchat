from chatserver.ui.banner import BANNER
from chatserver.ui.formatter import Formatter, get_user_color


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


def test_formatter_ansi_user_list():
    formatter = Formatter(plain_text=False)
    users = ["Alice", "Bob"]
    user_list = formatter.format_user_list("Test", users, 10)

    assert "\033[" in user_list
    assert "Test" in user_list
    assert "Alice" in user_list


def test_formatter_ansi_welcome():
    formatter = Formatter(plain_text=False)
    welcome = formatter.format_welcome_message("Test", "Alice")

    assert "\033[" in welcome
    assert "Test" in welcome
    assert "Alice" in welcome


def test_formatter_ansi_help():
    formatter = Formatter(plain_text=False)
    help_msg = formatter.format_help()

    assert "\033[" in help_msg
    assert "/who" in help_msg


def test_formatter_banner_ansi():
    formatter = Formatter(plain_text=False)
    formatted = formatter.format_banner(BANNER)

    assert "\033[" in formatted
    assert BANNER in formatted or "Chat" in formatted


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


def test_banner_exists():
    assert BANNER is not None
    assert len(BANNER) > 0
    assert "╔" in BANNER


def test_banner_format():
    assert "╔" in BANNER
    assert "║" in BANNER
    assert "╚" in BANNER
