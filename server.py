from cryptography.src.service.server import Server

server = Server(
    ("localhost", 55556),
    asymmetric_key_type="RSA",
    asymmetric_bits=1024,
    symmetric_key_type="AES",
    symmetric_bits=128,
    path_to_key="cryptography/src/data/"
)

server.connection_handler(("localhost", 55555))