import pytest

from cryptography.src.keys.asymmetric.rsa import RSA


class TestRSA:

    @pytest.mark.parametrize(
        "message, key_length",
        [
            (
                "He set out for a short walk, but now all he could see were mangroves and water were for miles.",
                1024,
            ),
            (
                "It's not possible to convince a monkey to give you a banana by promising it infinite bananas when they die.",
                2048,
            ),
            (
                "The elderly neighborhood became enraged over the coyotes who had been blamed for the poodles disappearance.",
                2048,
            ),
            (
                "He fumbled in the darkness looking for the light switch, but when he finally found it there was someone already there.",
                1024,
            ),
            (
                "It's not possible to convince a monkey to give you a banana by promising it infinite bananas when they die.",
                2048,
            ),
            (
                "You should never take advice from someone who thinks red paint dries quicker than blue paint.",
                2048,
            ),
            (
                "Although it wasn't a pot of gold, Nancy was still enthralled at what she found at the end of the rainbow.",
                1024,
            ),
            (
                "Jason didnt understand why his parents wouldnt let him sell his little sister at the garage sale.",
                1024,
            ),
        ],
    )
    def test_algorithm(self, message: str, key_length: int) -> None:
        rsa = RSA(key_length)
        encrypted: str = rsa.encrypt(message)
        decrypted: str = rsa.decrypt(encrypted)
        assert decrypted == message

        encrypted: str = RSA.encrypt_with_known_key(message, rsa._public_key)
        decrypted: str = RSA.decrypt_with_known_key(encrypted, rsa._private_key)
        assert decrypted == message
