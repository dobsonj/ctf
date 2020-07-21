#!/usr/bin/env python3
from pwn import *

context.log_level='DEBUG'
#p = process('./RickNMorty')
p = remote('chall.csivit.com', 30827)

def fun1(param_1, param_2):
    local_c = 0
    local_10 = 1
    while (local_10 <= param_1) or (local_10 <= param_2):
        if (param_1 % local_10 == 0) and (param_2 % local_10 == 0):
            local_c = local_10
        local_10 += 1
    return local_c

def fun2(param_1):
    lvar1 = 0
    if param_1 == 0:
        lvar1 = 1
    else:
        lvar1 = fun2(param_1 - 1)
        lvar1 = lvar1 * param_1
    return lvar1

while True:
    line = p.recvline()
    if not line or line.decode().startswith('fun() took'):
        break

    nums = line.decode().rstrip().split(' ')
    ans = fun1(int(nums[0]), int(nums[1]))
    ans = fun2(ans + 3)
    p.sendline(str(ans))

p.stream()
