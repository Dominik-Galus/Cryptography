from unittest.mock import MagicMock, mock_open, patch

import numpy as np
import pytest

from cryptography.src.keys.factories.asymmetrickeyfactory import AsymmetricKeyFactory
from cryptography.src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory
from cryptography.src.service.server import Server


class TestServer:
    @pytest.fixture
    def server_instance(self) -> Server:
        server = Server(
            address=("localhost", 55556),
            asymmetric_key_type="RSA",
            asymmetric_bits=1024,
            symmetric_key_type="AES",
            symmetric_bits=128,
            path_to_key=None,
        )
        return server

    @patch("socket.socket")
    def test_start_server(self, mock_sock: MagicMock, server_instance: Server) -> None:
        mock_sock_instance = mock_sock.return_value
        server_instance.start_server()

        mock_sock_instance.bind.assert_called_with(("localhost", 55556))
        mock_sock_instance.listen.assert_called_once()

    @patch.object(AsymmetricKeyFactory, "create_key")
    def test_generate_asymmetric_key(
        self,
        mock_key: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_key_instance = mock_key.return_value
        mock_key_instance.public_key = (65537, 123456789)
        mock_key_instance.private_key = (3, 123456789)
        server_instance.generate_asymmetric_keys()

        assert server_instance.asymmetric_public_key == mock_key_instance.public_key
        assert server_instance.asymmetric_private_key == mock_key_instance.private_key

    @patch.object(SymmetricKeyFactory, "create_key")
    def test_generate_symmetric_key(
        self,
        mock_key: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_key_instance = mock_key.return_value
        mock_key_instance.key = ["mockkey"]
        symmetric_key = server_instance.generate_symmetric_key()
        assert symmetric_key == mock_key_instance.key

    def test_load_keys(self) -> None:
        with patch.object(AsymmetricKeyFactory, "create_key") as mock_key:
            mock_key_instance = mock_key.return_value
            mock_key_instance.load_from_file.side_effect = [
                (65537, 123456789),
                (3, 123456789),
            ]
            mock_public_key_content = "65537 123456789"
            mock_private_key_content = "3 123456789"

            mock_open_file = mock_open()
            mock_open_file.side_effect = [
                mock_open(read_data=mock_public_key_content).return_value,
                mock_open(read_data=mock_private_key_content).return_value,
            ]

            with (
                patch("pathlib.Path.exists", return_value=True),
                patch("builtins.open", mock_open_file),
            ):
                server = Server(
                    address=("localhost", 55556),
                    asymmetric_key_type="RSA",
                    asymmetric_bits=1024,
                    symmetric_key_type="AES",
                    symmetric_bits=128,
                    path_to_key="13",
                )

                assert server.asymmetric_public_key == (65537, 123456789)
                assert server.asymmetric_private_key == (3, 123456789)

    @patch("socket.socket")
    def test_connect_to_server(
        self,
        mock_socket: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_server_conn_instance = mock_socket.return_value
        mock_server_conn_instance.sendall.return_value = f"{server_instance.port}-"
        with patch.object(
            server_instance,
            "send_asymmetric_public_key_to_server",
        ) as mock_send_key:
            mock_send_key.return_value = b"123456789 987654321 RSA"
            mock_server_conn_instance.recv.return_value = b"1"

            server_instance.server_connection = mock_server_conn_instance

            mock_session_socket = MagicMock()
            mock_session_socket.recv.return_value = b"Session"

            mock_server_socket = MagicMock()
            mock_server_socket.accept.side_effect = [
                (mock_session_socket, ("localhost", 50000)),
                StopIteration("End loop"),
            ]

            server_instance.server_socket = mock_server_socket

            with patch.object(
                server_instance,
                "send_asymmetric_public_key_to_server",
            ) as mock_send_key:
                mock_send_key.return_value = b"123456789 987654321 RSA"

                with patch("threading.Thread") as mock_thread:
                    try:
                        server_instance.connection_handler(("localhost", 55555))
                    except StopIteration:
                        pass

                    mock_server_conn_instance.sendall.assert_called_with(
                        f"{server_instance.port}-".encode(),
                    )

                    mock_session_socket.recv.assert_called_once_with(1024)

    @patch("socket.socket")
    def test_send_asymmetric_key_to_server(
        self,
        mock_server_connection: MagicMock,
        server_instance: Server,
    ) -> None:
        server_instance.server_connection = mock_server_connection

        server_instance.asymmetric_public_key = (123456789, 987654321)
        server_instance.asymmetric_key_type = "RSA"

        server_instance.send_asymmetric_public_key_to_server()

        expected_key = b"123456789 987654321 RSA"
        mock_server_connection.sendall.assert_called_once_with(expected_key)

    @patch("socket.socket")
    def test_send_encrypted_symmetric_key_to_server(
        self,
        mock_socket: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_socket_instance = mock_socket.return_value

        with patch.object(
            server_instance,
            "encrypt_symmetric_key",
        ) as mock_encrypt_symmetric_key:
            mock_encrypted_key = "encrypted_symmetric_key"
            mock_encrypt_symmetric_key.return_value = mock_encrypted_key

            with patch.object(
                AsymmetricKeyFactory,
                "create_key",
            ) as mock_asymmetric_key_factory:
                mock_asymmetric_key = MagicMock()
                mock_asymmetric_key_factory.return_value = mock_asymmetric_key

                symmetric_key = MagicMock()
                asymmetric_public_key = "123456789 987654321 RSA"

                server_instance.server_connection = mock_socket_instance
                server_instance.send_encrypted_symmetric_key_to_server(
                    symmetric_key=symmetric_key,
                    asymmetric_public_key=asymmetric_public_key,
                )

                mock_socket_instance.sendall.assert_called_once_with(
                    mock_encrypted_key.encode(),
                )

    @patch.object(AsymmetricKeyFactory, "get_key")
    def test_encrypt_symmetric_key(
        self,
        mock_asymmetric_key_factory: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_asymmetric_key = MagicMock()
        mock_asymmetric_key.encrypt_with_known_key.return_value = "encrypted"

        mock_asymmetric_key_factory.return_value = mock_asymmetric_key

        symmetric_key = MagicMock()
        symmetric_key.flatten.return_value = [1, 2, 3, 4]

        asymmetric_public_key = (123456789, 987654321)

        encrypted_symmetric_key = server_instance.encrypt_symmetric_key(
            symmetric_key=symmetric_key,
            asymmetric_public_key=asymmetric_public_key,
            asymmetric_key_type="RSA",
        )

        expected_encrypted_key = "encrypted encrypted encrypted encrypted"

        assert encrypted_symmetric_key == expected_encrypted_key

        mock_asymmetric_key.encrypt_with_known_key.assert_any_call(
            "1",
            asymmetric_public_key,
        )
        mock_asymmetric_key.encrypt_with_known_key.assert_any_call(
            "2",
            asymmetric_public_key,
        )
        mock_asymmetric_key.encrypt_with_known_key.assert_any_call(
            "3",
            asymmetric_public_key,
        )
        mock_asymmetric_key.encrypt_with_known_key.assert_any_call(
            "4",
            asymmetric_public_key,
        )

    @patch("socket.socket")
    def test_receive_data_from_session(
        self,
        mock_socket: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_session = mock_socket.return_value
        mock_session.recv.side_effect = [b"test_message", b""]

        server_instance.sessions.append(mock_session)
        mock_server_conn = MagicMock()
        server_instance.server_connection = mock_server_conn

        server_instance.receive_data_from_session(mock_session)

        mock_server_conn.send.assert_called_with(b"test_message")
        assert mock_session not in server_instance.sessions
        mock_session.close.assert_called_once()

    @patch("socket.socket")
    def test_send_decrypted_symmetric_data_to_session(
        self,
        mock_session: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_session_instance = mock_session.return_value
        with patch.object(AsymmetricKeyFactory, "get_key") as mock_asymmetric_factory:
            mock_asymmetric_key = MagicMock()
            mock_asymmetric_key.decrypt_with_known_key.return_value = "decrypted"

            mock_asymmetric_factory.return_value = mock_asymmetric_key

            encrypted_symmetric_key = "10 20 30"
            expected_decrypted_key = "decrypted decrypted decrypted"
            expected_symmetric_data = f"{expected_decrypted_key}-{server_instance.symmetric_key_type}-{server_instance.symmetric_bits}".encode()

            server_instance.send_decrypted_symmetric_data_to_session(
                encrypted_symmetric_key,
                mock_session_instance,
            )

            mock_session_instance.send.assert_called_once_with(expected_symmetric_data)

    @patch("socket.socket")
    def test_symmetric_data_to_session(
        self,
        mock_session: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_session_instance = mock_session.return_value

        symmetric_key = np.array([[10, 20], [30, 40]])
        flattened_key: str = " ".join(str(byte) for byte in symmetric_key.flatten())
        expected_symmetric_data: str = (
            f"{flattened_key}-{server_instance.symmetric_key_type}-{server_instance.symmetric_bits}".encode()
        )

        server_instance.send_symmetric_data_to_session(
            symmetric_key,
            mock_session_instance,
        )

        mock_session_instance.send.assert_called_once_with(expected_symmetric_data)

    @patch("socket.socket")
    def test_forward_data_to_server(
        self,
        mock_server_conn: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_server_conn_instance = mock_server_conn.return_value
        mock_server_conn_instance.send.return_value("message")
        server_instance.server_connection = mock_server_conn_instance

        server_instance.forward_data_to_server("message")

        mock_server_conn_instance.send.assert_called_once()

    @patch("socket.socket")
    def test_receive_data_from_server(
        self,
        mock_server_conn: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_server_conn_instance = mock_server_conn.return_value
        mock_server_conn_instance.recv.side_effect = (b"given data", b"")
        server_instance.server_connection = mock_server_conn_instance

        with patch.object(server_instance, "broadcast_to_sessions") as mock_broadcast:
            server_instance.receive_data_from_server()

            assert mock_server_conn_instance.recv.call_count == 3
            mock_broadcast.assert_called_once_with("given data", sender_session=None)

    @patch("socket.socket")
    def test_broadcast_to_sessions(
        self,
        mock_session: MagicMock,
        server_instance: Server,
    ) -> None:
        mock_session_instance_1 = mock_session.return_value
        mock_session_instance_2 = MagicMock()

        server_instance.sessions = [mock_session_instance_1, mock_session_instance_2]

        server_instance.broadcast_to_sessions("message", mock_session_instance_1)

        mock_session_instance_2.send.assert_called_once_with(b"message")
        mock_session_instance_1.send.assert_not_called()
