import logging
import sys
from datetime import datetime, timezone
from glob import glob
from pathlib import Path

import typer
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

cli = typer.Typer()


@cli.command()
def create_fernet_key():
    key = Fernet.generate_key()

    keyfile = str(Path(__file__).parent.joinpath("keys", f"{int(datetime.now(timezone.utc).timestamp())}.key"))

    with open(keyfile, "wb") as filekey:
        filekey.write(key)

    logger.info(f"Created keyfile: {keyfile}")


@cli.command()
def encrypt_file(
    input_file: Path = typer.Argument(default=..., exists=True),
    output_file: Path = typer.Argument(default=None),
):
    keyfiles = sorted(glob(str(Path(__file__).parent.joinpath("keys", "*.key"))), reverse=True)
    if len(keyfiles) == 0:
        raise Exception("No keyfiles found. Run 'create_fernet_key' first.")

    keyfile = keyfiles[0]

    logging.info(f"Encrypting with latest keyfile: {keyfile}")
    with open(keyfile, "rb") as file:
        key = file.read()

    f = Fernet(key)

    with open(input_file, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    if output_file is not None:
        with open(output_file, "wb") as file:
            file.write(encrypted_data)

        logger.info(f"Encrypted file: {input_file} -> {output_file}")
    else:
        logger.info(f"Encrypted file: {input_file}:\n{encrypted_data.decode('utf-8')}")


@cli.command()
def decrypt_file(
    input_file: Path = typer.Argument(default=..., exists=True),
    output_file: Path = typer.Argument(default=None),
):
    keyfiles = sorted(glob(str(Path(__file__).parent.joinpath("keys", "*.key"))))
    if len(keyfiles) == 0:
        raise Exception("No keyfiles found. Run 'create_fernet_key' first.")

    for keyfile in keyfiles:
        logging.info(f"Decrypting with keyfile: {keyfile}")

        with open(keyfile, "rb") as file:
            key = file.read()

        f = Fernet(key)

        with open(input_file, "rb") as file:
            file_data = file.read()

        try:
            decrypted_data = f.decrypt(file_data)
        except Exception:
            logger.info(f"Failed to decrypt with keyfile: {keyfile}")
            continue

        if output_file is not None:
            with open(output_file, "wb") as file:
                file.write(decrypted_data)

            logger.info(f"Decrypted file: {input_file} -> {output_file}")
        else:
            logger.info(f"Decrypted file: {input_file}:\n{decrypted_data.decode('utf-8')}")

        sys.exit(0)

    logger.info(f"Unable to decrypt {input_file} with existing keys.")
    sys.exit(1)
