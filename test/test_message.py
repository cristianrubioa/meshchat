from datetime import datetime

from chatserver.core.message import Message


def test_message_creation():
    msg = Message(from_user="Alice", content="Hello", timestamp=datetime.now())
    assert msg.from_user == "Alice"
    assert msg.content == "Hello"
    assert not msg.is_system
    assert not msg.is_action


def test_system_message():
    msg = Message(
        from_user="System",
        content="User joined",
        timestamp=datetime.now(),
        is_system=True,
    )
    assert msg.is_system


def test_action_message():
    msg = Message(
        from_user="Alice",
        content="waves",
        timestamp=datetime.now(),
        is_action=True,
    )
    assert msg.is_action
    assert not msg.is_system
