from cryptography.src.service.server import Server
if __name__ == "__main__":
    server = Server(
        address=("0.0.0.0", 55560),
        asymmetric_key_type="RSA",
        asymmetric_bits=1024,
        symmetric_key_type="AES",
        symmetric_bits=128,
        path_to_key=None
    )
    server.connection_handler(("localhost", 55561))