#!/usr/bin/env python3

f = open(f"flags.txt", 'r')
lines = f.readlines()
for line in lines:
    b = bytes.fromhex(line)
    for k in range(255):
        d = bytes([b[i] ^ k for i in range(len(b))])
        if d[:3] == b'dam':
            print(d)
            break
