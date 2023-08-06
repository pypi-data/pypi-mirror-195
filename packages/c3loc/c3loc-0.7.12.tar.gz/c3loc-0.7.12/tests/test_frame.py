import struct

import lzo
import pytest

from c3loc.config import CONFIG
from c3loc.ingest.frame import Frame, InvalidFrame
from c3loc.ingest.protocol import PacketType


def frame_message(packet_type, data, compress=False):
    flags = (1 << 7) if compress else 0
    flags |= packet_type & 0b01111111
    data = lzo.compress(data, 6, False) if compress else data
    header = struct.pack("!IB", len(data), flags)
    return b''.join([header, data])


@pytest.fixture
def frame():
    return Frame()


def test_frame_too_big(frame):
    msg = frame_message(PacketType.RAW,
                        b'0' * (CONFIG['MAX_FRAME_SIZE'] + 1),
                        False)
    with pytest.raises(InvalidFrame):
        frame.add_bytes(msg)


def test_bad_compressed_data(frame):
    data = b'0' * 50
    header = struct.pack("!IB", len(data), 1 << 7)  # first bit signals lzo
    msg = b''.join([header, data])
    with pytest.raises(InvalidFrame):
        frame.add_bytes(msg)


def test_multipacket_msg(frame):
    msg = frame_message(PacketType.RAW, b'\x00'*10, False)
    frame.add_bytes(msg[:2])
    assert len(frame.get_messages()) == 0
    frame.add_bytes(msg[2:])
    assert len(frame.get_messages()) == 1


def test_overflow_of_lzo_decompress_buf(frame):
    data = b'0' * (CONFIG['MAX_FRAME_SIZE'] + 500)
    assert len(data) > CONFIG['MAX_FRAME_SIZE']
    msg = frame_message(PacketType.RAW,
                        data,
                        True)
    assert len(msg) < CONFIG['MAX_FRAME_SIZE']
    with pytest.raises(InvalidFrame):
        frame.add_bytes(msg)
