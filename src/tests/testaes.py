import pytest

from src.keys.symmetric.aes import AES

class TestAES:
    
    @pytest.mark.parametrize(
        "message, key_length",
        [
            ("Secret message", 128),
            ("communication", 256),
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