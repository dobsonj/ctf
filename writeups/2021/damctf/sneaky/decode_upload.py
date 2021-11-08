#!/usr/bin/env python3
import base64
f = open(f"upload.b64", 'r')
b64in = f.readlines()
p = base64.b64decode(b64in[0])
k = b'8675309'
d = bytes([p[i] ^ k[(i % len(k))] for i in range(len(p))])
print(d.decode())

