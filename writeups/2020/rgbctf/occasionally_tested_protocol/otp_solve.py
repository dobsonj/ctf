#!/usr/bin/python3
from pwn import *
from time import time
from random import seed, randint

context.log_level='DEBUG'
start = int(time())
#p = process(['/usr/bin/python3', './otp.py'])
p = remote('167.172.123.213', 12345)
p.recvline() # Here's 10 numbers for you:
nums = [] 
for i in range(10):
    line = p.recvline().rstrip()
    nums.append(int(line))
    
p.recvuntil("Here's another number I found:  ")
another_num = int(p.recvline().rstrip())
p.stream()
end = int(time())

print("start=%u end=%u" % (start, end))
print(nums)  
print(another_num)

s = start
while s <= end:
    seed(s)
    found = True
    for i in range(10):
        r = randint(5, 10000)
        if r != nums[i]:
            found = False
    if found:
        print("FOUND SEED: %u" % s)
        break
    s += 1
    
g = another_num.to_bytes(40, 'little')
b = bytearray([randint(0, 255) for _ in range(40)])
n = bytearray([l ^ p for l, p in zip(g, b)]), 'little'
print(n)
