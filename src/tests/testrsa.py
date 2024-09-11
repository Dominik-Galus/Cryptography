import pytest

from src.keys.asymmetric.rsa import RSA


class TestRSA:

    @pytest.mark.parametrize(
        "message, key_length",
        [
            ("Secret message", 1024),
            ("communication", 2048),
            ("asfhwehjg23432", 2048),
            ("entertainment", 1024),
            ("disappointment", 2048),
            ("identification", 2048),
            ("Dont mess with my family", 1024),
            ("asfhsdj42323", 1024),
        ],
    )
    def test_algorithm(self, message, key_length):
        rsa = RSA(key_length)
        encrypted = rsa.encrypt(message)
        decrypted = rsa.decrypt(encrypted)
        assert decrypted == message
        
        encrypted = RSA.encrypt_with_known_key(message, rsa._public_key)
        decrypted = RSA.decrypt_with_known_key(encrypted, rsa._private_key)
        assert decrypted == message
