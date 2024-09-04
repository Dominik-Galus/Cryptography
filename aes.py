import random

import numpy as np

from pure import inv_s_box, rcon, s_box
from symmetric import Symmetric


class AES(Symmetric):
    def __init__(self, bits: int, aes_key: np.ndarray | None = None) -> None:
        if bits not in [128, 192, 256]:
            raise ValueError("Wrong bits key length")
        self.key_columns: int = bits // 32
        self.rounds: int = {128: 10, 192: 12, 256: 14}[bits]
        if aes_key is not None:
            self._key = aes_key
        else:
            self._key = self.generate_key(bits)
        self.key_expansion()

    def rot_word(self, word: np.ndarray) -> np.ndarray:
        return np.roll(word, -1)

    def sub_word(self, word: np.ndarray) -> np.ndarray:
        return s_box[word // 16, word % 16]

    def generate_key(self, bits: int) -> np.ndarray:
        bytes_length: int = bits // 8
        if bits % 8 != 0:
            bytes_length += 1
        hex_key: str = "".join(
            random.choice("0123456789abcdef") for _ in range(bytes_length * 2)
        )
        byte_array = np.array(
            [int(hex_key[i : i + 2], 16) for i in range(0, len(hex_key), 2)]
        )
        matrix = np.array([byte_array[i : i + 4] for i in range(0, len(byte_array), 4)])
        return matrix.T

    def key_expansion(self) -> None:
        self.expanded_key: np.ndarray = np.zeros(
            (4 * (self.rounds + 1), 4), dtype=np.uint8
        )
        self.expanded_key[: self.key_columns] = self.key.T

        for i in range(self.key_columns, 4 * (self.rounds + 1)):
            temp: np.ndarray = self.expanded_key[i - 1].copy()

            if i % self.key_columns == 0:
                temp = self.sub_word(self.rot_word(temp))
                rcon_index = i // self.key_columns - 1
                rcon_value = rcon[rcon_index]
                rcon_value_array = np.array([rcon_value, 0, 0, 0], dtype=np.uint8)
                temp = temp ^ rcon_value_array
            elif self.key_columns > 6 and i % self.key_columns == 4:
                temp = self.sub_word(temp)

            self.expanded_key[i] = self.expanded_key[i - self.key_columns] ^ temp

    def aes_state(self, text: str) -> np.ndarray:
        byte_array = np.array([ord(char) for char in text.ljust(16)])
        state = byte_array.reshape(4, 4).T
        return state

    def int_matrix_to_hex_matrix(self, matrix) -> np.ndarray:
        hex_matrix = np.array([[f"{num:02x}" for num in row] for row in matrix])
        return hex_matrix
    

    def sub_bytes(self) -> None:
        self.state = s_box[self.state // 16, self.state % 16]

    def shift_rows(self):
        for i in range(4):
            self.state[i] = np.roll(self.state[i], -i)

    def galois_mult(self, a: int, b: int) -> int:
        p: int = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            carry = a & 0x80
            a <<= 1
            if carry:
                a ^= 0x1B
            b >>= 1
        return p & 0xFF

    def mix_columns(self):
        for i in range(4):
            col = self.state[:, i]
            self.state[:, i] = [
                self.galois_mult(col[0], 2)
                ^ self.galois_mult(col[1], 3)
                ^ self.galois_mult(col[2], 1)
                ^ self.galois_mult(col[3], 1),
                self.galois_mult(col[0], 1)
                ^ self.galois_mult(col[1], 2)
                ^ self.galois_mult(col[2], 3)
                ^ self.galois_mult(col[3], 1),
                self.galois_mult(col[0], 1)
                ^ self.galois_mult(col[1], 1)
                ^ self.galois_mult(col[2], 2)
                ^ self.galois_mult(col[3], 3),
                self.galois_mult(col[0], 3)
                ^ self.galois_mult(col[1], 1)
                ^ self.galois_mult(col[2], 1)
                ^ self.galois_mult(col[3], 2),
            ]

    def add_round_key(self, round: int) -> None:
        self.state ^= self.expanded_key[round * 4 : (round + 1) * 4].T

    def encrypt(self, message: str) -> str:
        self.state: np.ndarray = self.aes_state(message)
        self.add_round_key(0)

        for round in range(1, self.rounds):
            self.sub_bytes()
            self.shift_rows()
            self.mix_columns()
            self.add_round_key(round)

        self.sub_bytes()
        self.shift_rows()
        self.add_round_key(self.rounds)

        
        hex_string = ''.join([f"{num:02x}" for num in self.state.T.flatten()])

        return hex_string

    def inv_mix_columns(self) -> None:
        for i in range(4):
            col = self.state[:, i]
            self.state[:, i] = [
                self.galois_mult(col[0], 14)
                ^ self.galois_mult(col[1], 11)
                ^ self.galois_mult(col[2], 13)
                ^ self.galois_mult(col[3], 9),
                self.galois_mult(col[0], 9)
                ^ self.galois_mult(col[1], 14)
                ^ self.galois_mult(col[2], 11)
                ^ self.galois_mult(col[3], 13),
                self.galois_mult(col[0], 13)
                ^ self.galois_mult(col[1], 9)
                ^ self.galois_mult(col[2], 14)
                ^ self.galois_mult(col[3], 11),
                self.galois_mult(col[0], 11)
                ^ self.galois_mult(col[1], 13)
                ^ self.galois_mult(col[2], 9)
                ^ self.galois_mult(col[3], 14),
            ]

    def inv_shift_rows(self) -> None:
        for i in range(4):
            self.state[i] = np.roll(self.state[i], i)

    def inv_sub_bytes(self) -> None:
        self.state = inv_s_box[self.state // 16, self.state % 16]

    def decrypt(self, encrypted_message: str) -> str:
        byte_array = np.array([int(encrypted_message[i:i+2], 16) for i in range(0, len(encrypted_message), 2)], dtype=np.uint8)
        self.state = byte_array.reshape(4, 4).T

        self.add_round_key(self.rounds)

        for round in range(self.rounds - 1, 0, -1):
            self.inv_shift_rows()
            self.inv_sub_bytes()
            self.add_round_key(round)
            self.inv_mix_columns()

        self.inv_shift_rows()
        self.inv_sub_bytes()
        self.add_round_key(0)
        
        decrypted_text = ''.join([chr(byte) for byte in self.state.T.flatten()])
        decrypted_text = decrypted_text.rstrip()
        
        return decrypted_text
    
    @property
    def key(self):
        return self._key
    

if __name__ == "__main__":
    aes1 = AES(128)
    aes2 = AES(128, aes_key=aes1.key)
    encrypted = aes1.encrypt("Tajna wiadomosc")
    decrypted = aes2.decrypt(encrypted)
    
    assert decrypted == "Tajna wiadomosc"
