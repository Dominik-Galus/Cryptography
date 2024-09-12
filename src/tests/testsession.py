import numpy as np
import pytest

from src.service.session import Session


class TestSession:

    @pytest.mark.parametrize(
        "symmetric_type, symmetric_key, bits, server_id, message",
        [
            (
                "AES",
                [
                    [122, 221, 5, 148, 135, 231],
                    [
                        8,
                        32,
                        87,
                        52,
                        166,
                        147,
                    ],
                    [122, 167, 173, 19, 58, 74],
                    [133, 238, 225, 211, 8, 150],
                ],
                192,
                "123",
                "Boulders lined the side of the road foretelling what could come next.",
            ),
            (
                "AES",
                [
                    [254, 241, 173, 73, 238, 54],
                    [0, 165, 212, 220, 152, 174],
                    [127, 17, 87, 115, 91, 203],
                    [244, 153, 83, 11, 240, 43],
                ],
                192,
                "234",
                "Flesh-colored yoga pants were far worse than even he feared.",
            ),
            (
                "AES",
                [
                    [84, 196, 160, 193],
                    [151, 227, 124, 190],
                    [204, 66, 66, 163],
                    [127, 75, 166, 165],
                ],
                128,
                "345",
                "The lyrics of the song sounded like fingernails on a chalkboard.",
            ),
            (
                "AES",
                [
                    ["42", "183", "23", "203", "167", "229", "49", "20"],
                    ["169", "74", "84", "209", "179", "8", "47", "110"],
                    ["118", "51", "242", "181", "10", "108", "183", "207"],
                    ["223", "109", "192", "202", "181", "243", "40", "193"],
                ],
                256,
                "456",
                "He turned in the research paper on Friday; otherwise, he would have not passed the class.",
            ),
        ],
    )
    def test_session(self, symmetric_type: str, symmetric_key: np.ndarray, bits: int, server_id: str, message: str) -> None:
        session = Session(symmetric_type, symmetric_key, bits, server_id)
        encrypted: str = session.encrypt_data(message)
        decrypted: str = session.decrypt_data(encrypted)
        assert decrypted == message
