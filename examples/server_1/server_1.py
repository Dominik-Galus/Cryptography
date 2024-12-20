from cryptography.service.server import Server

if __name__ == "__main__":
    server = Server(
        address=("0.0.0.0", 55560),
        asymmetric_key_data=("RSA", 1024),
        symmetric_key_data=("AES", 128),
        path_to_key=None,
    )
    server.connection_handler(("localhost", 55561))
