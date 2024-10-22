import pytest

from cryptography.src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory
from cryptography.src.keys.symmetric.symmetric import Symmetric


class TestSymmetricFactory:

    @pytest.mark.parametrize(
        "symmetric_key, key_length, message",
        [
            ("AES", 128, "Lorem ipsum dolor sit amet"),
            ("AES", 192, "Carol drank the blood as if she were a vampire."),
            ("AES", 256, "She always speaks to him in a loud voice."),
        ],
    )
    def test_factory(
        self, symmetric_key: Symmetric, key_length: int, message: str
    ) -> None:
        symmetric = SymmetricKeyFactory.create_key(symmetric_key, key_length, None)
        encrypted: str = symmetric.encrypt(message)
        decrypted: str = symmetric.decrypt(encrypted)
        assert decrypted == message

        assert type(symmetric) is SymmetricKeyFactory.get_key(symmetric_key)
