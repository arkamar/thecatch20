#! /usr/bin/python

import base64
import sys

f = open(sys.argv[1], 'rb')

for i in range(31):
    l = int.from_bytes(f.read(2), byteorder='big')
    b64 = base64.b64decode(f.read(l)).decode()
    print(l, b64)

f.close()
