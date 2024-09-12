import pytest

from src.service.server import Server


class TestServer:

    @pytest.mark.parametrize(
        "asymmetric_type, asymmetric_key_length, symmetric_type, symmetric_key_length, file_index1, file_index2, message",
        [
            ("RSA", 1024, "AES", 128, "1", "2", "Lorem ipsum dolor sit amet"),
            (
                "RSA",
                1024,
                "AES",
                192,
                "1",
                None,
                "Despite what your teacher may have told you, there is a wrong way to wield a lasso",
            ),
            (
                "RSA",
                2048,
                "AES",
                256,
                None,
                None,
                "The snow-covered path was no help in finding his way out of the back-country",
            ),
        ],
    )
    def test_server(
        self,
        asymmetric_type: str,
        asymmetric_key_length: int,
        symmetric_type: str,
        symmetric_key_length: int,
        file_index1: str,
        file_index2: str,
        message: str,
    ) -> None:
        server1 = Server(
            asymmetric_key_type=asymmetric_type,
            asymmetric_bits=asymmetric_key_length,
            symmetric_key_type=symmetric_type,
            symmetric_bits=symmetric_key_length,
            key_file_index=file_index1,
        )
        server2 = Server(
            asymmetric_key_type=asymmetric_type,
            asymmetric_bits=asymmetric_key_length,
            symmetric_key_type=symmetric_type,
            symmetric_bits=symmetric_key_length,
            key_file_index=file_index2,
        )

        encrypted_symmetric_key: list[str] = server1.exchange_key(server2)
        decrypted_symmetric_key: list[str] = server2.retrieve_key(encrypted_symmetric_key)

        session_server1 = list(server1.sessions.values())[0]
        session_server2 = list(server2.sessions.values())[0]

        encrypted: str = session_server1.encrypt_data(message)
        decrypted: str = session_server2.decrypt_data(encrypted)

        assert decrypted == message
