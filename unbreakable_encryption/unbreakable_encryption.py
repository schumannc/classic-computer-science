from secrets import token_bytes
from typing import Tuple


def rando_key(lenght: int) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(lenght)
    # convert those bytes into a bit string and return it
    return int.from_bytes(tb, "big")


def encript(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = rando_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy # XOR
    return dummy, encrypted


def decript(key1: int, key2: int) -> str:
    decrypted: int = key1 ^ key2 # XOR
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()


if __name__ == '__main__':
    key1, key2 = encript("One time pad!")
    print(key1, key2)
    result: str = decript(key1, key2)
    print(result)