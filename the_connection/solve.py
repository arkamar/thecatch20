#! /usr/bin/python

import binascii
import base64
import struct
import socket
import hashlib
import random
import string
from time import sleep

def encode(prefix, msg):
    out = prefix + msg
    return struct.pack('>Q', len(out)) + out.encode('ascii')

def generate_id():
    return '{}'.format(''.join(random.sample(string.ascii_lowercase + string.digits, k=16)))

def generate_readymsg():
    return ';;ready'.format()


def decode(msg):
    l = struct.unpack('>Q', msg[:8])[0]
    rev = base64.b64decode(msg[8:8 + l])[::-1]
    prefix, out = rev[:16].decode('ascii'), rev[16:]
    out = binascii.unhexlify(out).decode('ascii')
    return (prefix, out)

TCP_IP = '78.128.216.92'
TCP_PORT = 20210
BUFFER_SIZE = 1024 * 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

cid = generate_id()
msg = generate_readymsg()

for i in range(20):
    data = encode(cid, msg)
#    print(data)
    s.send(data)
    data = s.recv(BUFFER_SIZE)
    print(decode(data))

s.close()

