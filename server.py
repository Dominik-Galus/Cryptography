from rsa import RSA
from session import Session
from aes import AES
import numpy as np
from typing import Self

class Server:
    def __init__(self, key_file_index: str | None = None) -> None:
        self.sessions: dict[int, "Session"] = {}
        if key_file_index is None:
            self.generate_rsa_keys()
        else:
            self.load_keys(key_file_index)    
        
    def generate_rsa_keys(self) -> None:
        rsa = RSA(1024)
        self.rsa_public_key: tuple[int, int] = rsa.public_key
        self.rsa_private_key: tuple[int, int] = rsa.private_key
        
    def generate_aes_key(self) -> np.ndarray:
        aes = AES(128)
        return aes.key
    
    def add_session(self, session: "Session") -> None:
        self.sessions[session.id] = session
    
    def exchange_key(self, other_server: Self) -> list[int]:
        aes_key: np.ndarray = self.generate_aes_key()
        
        encrypted_aes_key: list[int] = [
            RSA.encrypt_with_known_key(str(byte), other_server.rsa_public_key) for byte in aes_key.flatten()
            ]
        
        session = Session(aes_key, self.rsa_public_key)
        self.add_session(session)
        
        return encrypted_aes_key
    
    def load_keys(self, key_file_number: str) -> None:
        with open(f"rsa_public_key_{key_file_number}.txt", "r") as key_file:
            keys: list[str] = key_file.read().split()
            e: int = int(keys[0])
            n: int = int(keys[1])
            self.rsa_public_key: tuple[int, int] = (e, n)
        
        with open(f"rsa_private_key_{key_file_number}.txt", "r") as key_file:
            keys: list[str] = key_file.read().split()
            d: int = int(keys[0])
            n: int = int(keys[1])
            self.rsa_private_key: tuple[int, int] = (d, n)
        
        
    
    def retrieve_key(self, encrypted_aes_key: list[int]) -> np.ndarray:
        if self.rsa_private_key == None:
            self.generate_rsa_keys()
            
        decrypted_integers: list[int] = RSA.decrypt_with_known_key(encrypted_aes_key, self.rsa_private_key)
        
        aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4,4)
        
        session = Session(aes_key, self.rsa_public_key)
        self.add_session(session)
        
        return aes_key


        
if __name__ == "__main__":
    server1 = Server("1")
    server2 = Server("2")

    encrypted_aes_key = server1.exchange_key(server2)
    decrypted_aes_key = server2.retrieve_key(encrypted_aes_key)
    
    session_server1 = list(server1.sessions.values())[0]
    session_server2 = list(server2.sessions.values())[0]
    

    encrypted = session_server1.encrypt_data("Secret message")
    decrypted = session_server2.decrypt_data(encrypted)
    
    assert decrypted == "Secret message"
    
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print("******************************************************************")

    
    
    
    