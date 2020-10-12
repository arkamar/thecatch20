#! /usr/bin/python

import binascii
import base64
import struct

def encode(prefix, msg):
    out = prefix + msg
    rev = prefix + binascii.hexlify(bytes(out, 'ascii')).decode('ascii')
    b64 = base64.b64encode(bytes(rev[::-1], 'ascii'))
    return struct.pack('>Q', len(b64)) + b64

def decode(msg):
    l = struct.unpack('>Q', msg[:8])[0]
    rev = base64.b64decode(msg[8:8 + l])[::-1]
    prefix, out = rev[:16].decode('ascii'), rev[16:]
    out = binascii.unhexlify(out).decode('ascii')
    return (prefix, out)

print(decode(encode('1nhxcp2saj4d685g', ';;ready;;Linux')))
