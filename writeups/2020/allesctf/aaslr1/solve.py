#!/usr/bin/python3
from pwn import *

#context.log_level='DEBUG'
p = process(['./aaslr'])
#r = process(['./aaslr'])
r = process(['ncat', '--ssl', '7b000000f298cf5bdd7b82ed.challenges.broker2.allesctf.net', '1337'])

p.recvuntil('Select menu Item:\n')
r.recvuntil('Select menu Item:\n')
r.sendline('4')

for i in range(15):
    p.sendline('1')
    p.recvuntil('[>] Threw dice: ')
    roll = p.recvline().rstrip()
    print(roll)
    r.sendline(roll)

r.recvuntil('[>] CORRECT! You should go to Vegas.\n')
flag = r.recvline()
print(flag)

