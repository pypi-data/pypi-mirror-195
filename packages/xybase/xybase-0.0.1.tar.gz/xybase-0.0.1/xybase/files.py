from typing import Union


def write(f, content: Union[bytes, str]):
    mode = 'w' if isinstance(content, str) else 'wb'
    with open(f, mode=mode) as w:
        w.write(content)


def read_bytes(f) -> bytes:
    with open(f, mode='rb') as r:
        return r.read()


def read_lines(f) -> list[str]:
    with open(f, mode='r') as r:
        return r.read().splitlines()
