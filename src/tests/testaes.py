import pytest

from src.keys.symmetric.aes import AES


class TestAES:

    @pytest.mark.parametrize(
        "message, key_length",
        [
            ("Secret message", 128),
            (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                256,
            ),
            ("asfhwehjg23432", 192),
            ("entertainment", 192),
            ("disappointment", 128),
            ("identification", 256),
            ("Dont mess with my family or there will be consequences", 192),
            ("asfhsdj42323", 256),
        ],
    )
    def test_algorithm(self, message, key_length):
        aes = AES(key_length)
        encrypted: str = aes.encrypt(message)
        decrypted: str = aes.decrypt(encrypted)
        assert decrypted == message

        aes2 = AES(key_length, aes._key)
        decrypted = aes2.decrypt(encrypted)
        assert decrypted == message

        encrypted = aes2.encrypt(message)
        decrypted = aes2.decrypt(encrypted)
        assert decrypted == message
