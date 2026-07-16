import pytest

from chatserver.core.exceptions import (
    NicknameEmptyError,
    NicknameInvalidCharsError,
    NicknameReservedError,
    NicknameTooLongError,
    NicknameTooShortError,
)
from chatserver.core.validators import validate_nickname


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
