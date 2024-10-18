import pytest
from unittest.mock import MagicMock, patch

from src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory
from src.service.session import Session


class TestSession:
    @patch("socket.socket")
    def test_connect_to_server(self, mock_socket: MagicMock) -> None:
        mock_socket_instance = mock_socket.return_value
        session = Session(("localhost", 55556))

        mock_socket_instance.connect.assert_called_once_with(("localhost", 55556))
        assert session.session_socket is not None

    @patch("socket.socket")
    def test_retrive_key(self, mock_socket: MagicMock) -> None:
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.recv.return_value = b"mockkey-AES-256"
        session = Session(("localhost", 55556))

        session.retrieve_key()

        assert session.symmetric_key == ["mockkey"]
        assert session.symmetric_type == "AES"
        assert session.bits == 256

    @patch("socket.socket")
    def test_encrypt_data(self, mock_socket: MagicMock) -> None:
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.recv.return_value = b"mockkey-AES-256"
        session = Session(("localhost", 55556))

        with patch.object(SymmetricKeyFactory, "create_key") as mock_create_key:
            mock_symmetric_instance = MagicMock()
            mock_create_key.return_value = mock_symmetric_instance
            mock_symmetric_instance.encrypt.return_value = "encrypted_data"

            encrypted: str = session.encrypt_data("test_message")

            mock_create_key.assert_called_with(
                key_type="AES",
                bits=256,
                key=["mockkey"],
            )
            mock_symmetric_instance.encrypt.assert_called_with("test_message")
            assert encrypted == "encrypted_data"

    @patch("socket.socket")
    def test_decrypt_data(self, mock_socket: MagicMock) -> None:
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.recv.return_value = b"mockkey-AES-256"
        session = Session(("localhost", 55556))

        with patch.object(SymmetricKeyFactory, "create_key") as mock_create_key:
            mock_symmetric_instance = MagicMock()
            mock_create_key.return_value = mock_symmetric_instance
            mock_symmetric_instance.decrypt.return_value = "decrypted_data"

            decrypted: str = session.decrypt_data("encrypted_data")

            mock_create_key.assert_called_with(
                key_type="AES",
                bits=256,
                key=["mockkey"],
            )
            mock_symmetric_instance.decrypt.assert_called_with("encrypted_data")
            assert decrypted == "decrypted_data"

    @patch("socket.socket")
    def test_write_message(self, mock_socket: MagicMock) -> None:
        mock_socket_instance = mock_socket.return_value
        session = Session(("localhost", 55556))

        with patch("builtins.input", side_effect=["test message"]), \
            patch.object(session, "encrypt_data", return_value="encrypted message"):

            session.write_message()

            session.encrypt_data.assert_called_once_with("test message")

            mock_socket_instance.send.assert_called_with(b"encrypted message")
            
    @patch("socket.socket")
    def test_receive_message(self, mock_socket: MagicMock) -> None:
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.recv.return_value = b"mockkey-AES-256"
        session = Session(("localhost", 55556))
        mock_socket_instance.recv.return_value = b"encrypted message"
        
        with patch.object(session, "decrypt_data", side_effect=["Decrypted message"]) as mock_decrypt:
            with patch("builtins.print") as mock_print:
                session.receive_message()
                
                mock_decrypt.assert_called_with("encrypted message")
                mock_socket_instance.recv.assert_called_with(20000)
                mock_print.assert_any_call("Guest: Decrypted message")
        

