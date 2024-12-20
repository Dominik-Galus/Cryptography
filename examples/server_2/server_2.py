import time

from cryptography.service.server import Server

if __name__ == "__main__":
    server = Server(
        address=("0.0.0.0", 55561),
        asymmetric_key_type="RSA",
        asymmetric_bits=1024,
        symmetric_key_type="AES",
        symmetric_bits=128,
        path_to_key=None
    )
    time.sleep(5)
    server.connection_handler(("server1", 55560))
