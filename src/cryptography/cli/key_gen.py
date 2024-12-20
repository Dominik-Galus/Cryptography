from pathlib import Path
from typing import TYPE_CHECKING

import click

from cryptography.keys.factories.asymmetrickeyfactory import AsymmetricKeyFactory

if TYPE_CHECKING:
    from cryptography.keys.asymmetric.asymmetric import Asymmetric


@click.command()
@click.option("--key_type", type=click.Choice(AsymmetricKeyFactory.key_type_map.keys()),
              prompt="Enter the key type", help="The type of asymmetric key to be generated", required=True)
@click.option("-L", "--length", type=int, prompt="Enter the key length", help="The length of asymmetric key",
              required=True)
@click.option("-o", "--output", type=click.Path(exists=False),
              help="The path to the file that will be containing asymmetric key",
              required=False)
def generate_key_to_file(key_type: str, length: int, output: str) -> None:
    public_filename: str = (
        output + "public_key.txt" if output is not None else "src/cryptography/data/public_key.txt"
    )
    private_filename: str = (
        output + "private_key.txt" if output is not None else "src/cryptography/data/private_key.txt"
        )

    key: Asymmetric = AsymmetricKeyFactory.create_key(key_type, length)
    key_public: tuple[int, int] = key.public_key
    key_private: tuple[int, int] = key.private_key

    with Path.open(public_filename, "w+") as public_file:
        content: str = str(key_public[0]) + " " + str(key_public[1])
        public_file.write(content)

    with Path.open(private_filename, "w+") as private_file:
        content: str = str(key_private[0]) + " " + str(key_public[1])
        private_file.write(content)

if __name__ == "__main__":
    generate_key_to_file()
