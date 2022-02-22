import socket
import base64
import pickle
from datetime import datetime
import importlib.metadata

import nacl.secret
import nacl.utils

__version__ = importlib.metadata.version("MLOps-BalancePredictor-demo")

with open("secrets/secret.key", "rb") as secret_file:
    secret_key = secret_file.read()

secret_box = nacl.secret.SecretBox(secret_key)


def pickle_deserialize(serialized_obj: str):
    return pickle.loads(
        base64.b64decode(secret_box.decrypt(bytes.fromhex(serialized_obj)))
    )


def pickle_serialize(obj: object):
    return secret_box.encrypt(base64.b64encode(pickle.dumps(obj))).hex()


def add_metadata(content: dict):
    return {
        "out": content,
        "datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "version": __version__,
        "author": socket.gethostname(),
    }
