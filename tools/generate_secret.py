import sys

import nacl.secret
import nacl.utils

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Expected file location as argument")
        exit(1)

    file_location = sys.argv[1]
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

    with open(file_location, "wb") as secret_key_file:
        secret_key_file.write(key)
