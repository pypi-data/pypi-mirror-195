#!/usr/bin/env python3


from abc import abstractmethod
import struct
from typing import Any, List, Optional

NITEMS = 100_000

class BinaryDecoder:
    @abstractmethod
    def decode(self, server_endian: str, data: memoryview) -> List[Any]:
        """Interpret the given bytes as a list of Python objects"""
        pass


class BlobDecoder(BinaryDecoder):
    def decode(self, server_endian: str, data: memoryview) -> List[Any]:
        result: List[Optional[bytes]] = []
        pos = 0

        assert server_endian in ['big', 'little']
        struct_letter = '>q' if server_endian == 'big' else '<q'

        while data:
            try:
                end = 8 + struct.unpack(struct_letter, data[pos:pos + 8])[0]
            except struct.error:
                raise Exception(f"incomplete blob header after {len(result)} blobs")
            if 8 <= end <= len(data):
                result.append(bytes(data[8:end]))
                data = data[end:]
            elif end == 7: # 8 + -1
                result.append(None)
                data = data[8:]
            else:
                raise Exception(f"invalid blob (len={end - 8}) after {len(result)} blobs")

        return result


def gen_data() -> bytes:
    template = b'ABCDEFGHIJKLMNOP'
    blobs = [
        gen_blob(template[:i] if i != 3 else None)
        for i in range(NITEMS)
    ]
    return b''.join(blobs)


def gen_blob(bs: bytes) -> bytes:
    if bs is None:
        header = -1
        payload = b''
    else:
        header = len(bs)
        payload = bs
    return struct.pack('<q', header) + payload

print(len(gen_data()))

data = gen_data()

def run():
    decoder = BlobDecoder()
    for i in range(50):
        blobs = decoder.decode('little', memoryview(data))
        assert len(blobs) == NITEMS, f"len(blobs) == {len(blobs)}"


import cProfile
cProfile.run('run()', sort='cumulative')
