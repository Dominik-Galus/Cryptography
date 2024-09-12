import pytest

from src.keys.factories.asymmetrickeyfactory import AsymmetricKeyFactory


class TestAsymmetricFactory:

    @pytest.mark.parametrize(
        "asymmetric_key, key_length, message",
        [
            ("RSA", 1024, "Secret message"), 
            ("RSA", 2048, "Lorem ipsum dolor sit amet"),
            ("RSA", 1024, "Dont mess with my family or there will be consequences")
        ],
    )
    def test_factory(self, asymmetric_key, key_length, message):
        asymmetric = AsymmetricKeyFactory.create_key(asymmetric_key, key_length)
        encrypted = asymmetric.encrypt(message)
        decrypted = asymmetric.decrypt(encrypted)
        assert decrypted == message
        
        assert type(asymmetric) is AsymmetricKeyFactory.get_key(asymmetric_key)
