from pwn import *
binary = ELF('./a.out')
context.update(arch='amd64',os='linux')
print(binary.path)
print(binary.disasm(0x12da, 40))
binary.asm(0x12da,'''
mov eax, 0x265d1d23
mov edi, eax
call 0x1189
mov eax, 0x0
leave
ret
''')
patched = binary.path + '_patched'
print(patched)
print(binary.disasm(0x12da, 40))
binary.save(patched)
os.system('chmod +x ' + patched)
