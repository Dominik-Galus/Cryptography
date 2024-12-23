# cryptography

Source Code: [cryptography](https://github.com/Dominik-Galus/Cryptography/)
- - -
This project is a server-session connection supported by asymmetric and symmetric keys used to encrypt the data that is exchanged between servers as well as between sessions where servers are the brokers for the exchanged information.

## Installation
Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) and navigate to the directory with pyproject.toml file in it, then:
```
$ pip install .
```


## How it works
First, the servers establish a connection to exchange public asymmetric keys. In this process, one server provides its public key, enabling the other server to encrypt a generated symmetric key and return it securely as an encrypted message. The receiving server then decrypts the symmetric key using its private key.

Once both servers have access to the symmetric key, they can distribute it to their respective sessions. This shared key allows sessions to encrypt data intended for another session. When transmitting data, a session encrypts its message and sends it to its server. This server forwards the encrypted message to the connected server, which then delivers the message to the intended session. The recipient session can then decrypt the message using the shared symmetric key.

## Example
Getting started, we first need to create and turn on the server, so create for example a file `server.py`:
```
from cryptography.src.service.server import Server

server = Server(
    address=("localhost", 55555),
    asymmetric_key_data=("RSA", 1024),
    symmetric_key_data=("AES, 128),
    path_to_key=None,
)

server.connection_handler(address=("localhost", 55556))
```
We should see something like that:

![Screenshot 2024-10-26 00 13 11](https://github.com/user-attachments/assets/23a1ecbf-1ebf-4f27-b106-ec9cac70a5c1)

When there is existing server before ours on address we provided, it should connect instantly with another server

> Note: To server work properly you need to call the method connection_handler for server to start search for another server to connect.

If you want to generate the asymmetric keys in advance and store them in the path you want you need to call in command line:
```
$ key-gen [--key_type] [-L KEY_LENGTH] [-o PATH_TO_DIRECTORY]
```
```
Usage: key-gen [OPTIONS]

Options:
  --key_type [RSA]      The type of asymmetric key to be generate  [required]
  -L, --length INTEGER  The length of asymmetric key  [required]
  -o, --output PATH     The path to the file that will be containing
                        asymmetric key
  --help                Show this message and exit.
```

If we dealt with that we can now instantiate the session in another .py file:
```
from cryptography.src.service.session import Session

session = Session(server_address=("localhost", 55555))
```
Assuming that there will be a second server that connects to ours, the session will wait until they finally exchange the necessary info:

![Screenshot 2024-10-26 00 20 21](https://github.com/user-attachments/assets/06f9c589-da82-4723-b5d6-f850edadcea0)

And now the sessions can safely exchange messages among themselves:

![Screenshot 2024-10-26 00 23 29](https://github.com/user-attachments/assets/8c55b89c-d7d4-449c-a293-f79fb244d7d0)
