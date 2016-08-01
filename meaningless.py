import base64
import struct

class Meaningless(object):
    def __init__(self, key_64):
        self._upper = key_64 >> 32
        self._lower = key_64 & 0xFFFFFFFF

    def encode(self, plain_64):
        lower_plain = plain_64 & 0xFFFFFFFF
        upper_coded = \
            (plain_64 >> 32) ^ \
            (self._upper * lower_plain & 0xFFFFFFFF)

        lower_coded = (upper_coded * self._lower & 0xFFFFFFFF ^ lower_plain)

        return upper_coded << 32 | lower_coded

    def decode(self, coded_64):
        lower_coded = coded_64 & 0xFFFFFFFF
        upper_coded = coded_64 >> 32

        lower_plain = upper_coded * self._lower & 0xFFFFFFFF ^ lower_coded
        upper_plain = upper_coded ^ (self._upper * lower_plain & 0xFFFFFFFF)

        return upper_plain << 32 | lower_plain

    def encode_hex(self, plain_64):
        return '%016x' % self.encode(plain_64)

    def decode_hex(self, cstr):
        return self.decode(int(cstr, 16))

    def encode_base64(self, plain_64):
        n = self.encode(plain_64)
        data = struct.pack('<Q', n).rstrip('\x00')
        if len(data)==0:
            data = '\x00'
        s = base64.urlsafe_b64encode(data).rstrip('=')
        return s

    def decode_base64(self, s):
        data = base64.urlsafe_b64decode(s + '==')
        n = struct.unpack('<Q', data + '\x00'* (8-len(data)) )
        return self.decode(n[0])
