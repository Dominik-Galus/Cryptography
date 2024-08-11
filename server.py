from rsa import RSA
from session import Session
from aes import AES
import numpy as np
from typing import Self

class Server:
    def __init__(self) -> None:
        self.sessions: dict[int, "Session"] = {}
        self.generate_rsa_keys()
        
    def generate_rsa_keys(self) -> None:
        rsa = RSA(1024)
        self.rsa_public_key = rsa.public_key
        self.rsa_private_key = rsa.private_key
        
    def generate_aes_key(self) -> np.ndarray:
        aes = AES(128)
        return aes.key
    
    def add_session(self, session: "Session") -> None:
        self.sessions[session.id] = session
    
    def exchange_key(self, other_server: Self) -> list[int]:
        aes_key = self.generate_aes_key()
        rsa = RSA(1024)
        
        rsa.public_key = other_server.rsa_public_key
        encrypted_aes_key = [rsa.encrypt(str(byte)) for byte in aes_key.flatten()]
        
        session = Session(aes_key, self.rsa_public_key)
        self.add_session(session)
        
        return encrypted_aes_key
    
    def retrieve_key(self, encrypted_aes_key: list[int]) -> np.ndarray:
        rsa = RSA(1024)
        
        rsa.private_key = self.rsa_private_key
        decrypted_integers = rsa.decrypt(encrypted_aes_key)
        
        aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4,4)
        
        session = Session(aes_key, self.rsa_public_key)
        self.add_session(session)
        
        return aes_key


        
if __name__ == "__main__":
    serwer1 = Server()
    serwer2 = Server()

    encrypted_aes_key = serwer1.exchange_key(serwer2)
    decrypted_aes_key = serwer2.retrieve_key(encrypted_aes_key)
    
    sesja_serwer1 = list(serwer1.sessions.values())[0]
    sesja_serwer2 = list(serwer2.sessions.values())[0]
    

    zaszyfrowane = sesja_serwer1.encrypt_data("Tajna wiadomosc")
    print("Zaszyfrowane:", zaszyfrowane)

    odszyfrowane = sesja_serwer2.decrypt_data(zaszyfrowane)
    print("Odszyfrowane:", odszyfrowane)
    
    
    
    