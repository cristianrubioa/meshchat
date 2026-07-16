from chatserver.core.exceptions import (
    MessageTooLongError,
    NicknameEmptyError,
    NicknameInvalidCharsError,
    NicknameReservedError,
    NicknameTakenError,
    NicknameTooLongError,
    NicknameTooShortError,
    RateLimitError,
    RoomFullError,
)


def test_exception_messages():
    assert "empty" in str(NicknameEmptyError()).lower()
    assert "least" in str(NicknameTooShortError()).lower()
    assert "most" in str(NicknameTooLongError()).lower()
    assert "reserved" in str(NicknameReservedError()).lower()
    assert "only contain" in str(NicknameInvalidCharsError()).lower()


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
