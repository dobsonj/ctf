# Simple

## Description
A really simple crackme to get started ;) Your goal is to find the correct input so that the program return 1. The correct input will be the flag.

Creator : Nofix

## What are we dealing with?

There was a single .asm file provided. Download the asm file:

```
kali@kali:~/Downloads/simple$ cat main.asm 
BITS 64

SECTION .rodata
        some_array db 10,2,30,15,3,7,4,2,1,24,5,11,24,4,14,13,5,6,19,20,23,9,10,2,30,15,3,7,4,2,1,24
        the_second_array db 0x57,0x40,0xa3,0x78,0x7d,0x67,0x55,0x40,0x1e,0xae,0x5b,0x11,0x5d,0x40,0xaa,0x17,0x58,0x4f,0x7e,0x4d,0x4e,0x42,0x5d,0x51,0x57,0x5f,0x5f,0x12,0x1d,0x5a,0x4f,0xbf
        len_second_array equ $ - the_second_array
SECTION .text
    GLOBAL main

main:
        mov rdx, [rsp]
        cmp rdx, 2
        jne exit
        mov rsi, [rsp+0x10]
        mov rdx, rsi
        mov rcx, 0
l1:
        cmp byte [rdx], 0
        je follow_the_label
        inc rcx
        inc rdx
        jmp l1
follow_the_label:
        mov al, byte [rsi+rcx-1]
        mov rdi,  some_array
        mov rdi, [rdi+rcx-1]
        add al, dil
        xor rax, 42
        mov r10, the_second_array
        add r10, rcx
        dec r10
        cmp al, byte [r10]
        jne exit
        dec rcx
        cmp rcx, 0
        jne follow_the_label
win:
        mov rdi, 1
        mov rax, 60
        syscall
exit:
        mov rdi, 0
        mov rax, 60
        syscall
```

Assemble, link, and run:

```
kali@kali:~/Downloads/simple$ nasm -f elf64 main.asm 
kali@kali:~/Downloads/simple$ ls
main.asm  main.o
kali@kali:~/Downloads/simple$ ld -s -o main main.o
ld: warning: cannot find entry symbol _start; defaulting to 0000000000401000
kali@kali:~/Downloads/simple$ file main
main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped
kali@kali:~/Downloads/simple$ ./main 
kali@kali:~/Downloads/simple$ echo $?
0
```

## Analysis

The assembly code is quite small, but the decompiled C code still might help our understanding:

```c
void entry(void)
{
  long lVar1;
  char *pcVar2;
  long local_res0;
  char *param_8;
  
  if (local_res0 == 2) {
    lVar1 = 0;
    pcVar2 = param_8;
    while (*pcVar2 != '\0') {
      lVar1 = lVar1 + 1;
      pcVar2 = pcVar2 + 1;
    }
    do {
      if ((byte)(param_8[lVar1 + -1] + (char)*(undefined8 *)(&DAT_00401fff + lVar1) ^ 0x2aU) !=
          (&DAT_0040201f)[lVar1]) goto LAB_00401068;
      lVar1 = lVar1 + -1;
    } while (lVar1 != 0);
    syscall();
  }
LAB_00401068:
  syscall();
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}
```

The first check is the number of arguments (argc). This would be the name of the executable and an input string:

```c
  if (local_res0 == 2) {
```

```
main:   
        mov rdx, [rsp]
        cmp rdx, 2
        jne exit
```

The first loop is calculating the length of the input string:

```c
    lVar1 = 0;
    pcVar2 = param_8;
    while (*pcVar2 != '\0') {
      lVar1 = lVar1 + 1;
      pcVar2 = pcVar2 + 1;
    }
```

```
l1:
        cmp byte [rdx], 0
        je follow_the_label
        inc rcx
        inc rdx
        jmp l1
```

The second loop interates over the string BACKWARDS. It starts at the last character and stops at the first character.

```c
    do {
      if ((byte)(param_8[lVar1 + -1] + (char)*(undefined8 *)(&DAT_00401fff + lVar1) ^ 0x2aU) !=
          (&DAT_0040201f)[lVar1]) goto LAB_00401068;
      lVar1 = lVar1 + -1;
    } while (lVar1 != 0);
```

```
follow_the_label:
        mov al, byte [rsi+rcx-1]
        mov rdi,  some_array
        mov rdi, [rdi+rcx-1]
        add al, dil
        xor rax, 42
        mov r10, the_second_array
        add r10, rcx
        dec r10
        cmp al, byte [r10]
        jne exit
        dec rcx
        cmp rcx, 0
        jne follow_the_label
```

To simplify, the condition that we want to be TRUE for each iteration is basically this:

```
flag[pos - 1] + some_array[pos] ^ 42 == the_second_array[pos]
```

The first time we enter that loop, we'll be pointing at the NULL terminator '\0' for the input string, which is why the loop references input[pos - 1].

some_array and the_second_array are exactly 32 bytes each:

```
        some_array db 10,2,30,15,3,7,4,2,1,24,5,11,24,4,14,13,5,6,19,20,23,9,10,2,30,15,3,7,4,2,1,24
        the_second_array db 0x57,0x40,0xa3,0x78,0x7d,0x67,0x55,0x40,0x1e,0xae,0x5b,0x11,0x5d,0x40,0xaa,0x17,0x58,0x4f,0x7e,0x4d,0x4e,0x42,0x5d,0x51,0x57,0x5f,0x5f,0x12,0x1d,0x5a,0x4f,0xbf
```

Which means our input string will be in the format of:

```
shkCTF{************************}
```

The formula is pretty simple to reverse. To get the flag:

```
flag[pos] = (the_second_array[pos] ^ 42) - some_array[pos]
```

## Solution

```python
#!/bin/env python

some_array=[10,2,30,15,3,7,4,2,1,24,5,11,24,4,14,13,5,6,19,20,23,9,10,2,30,15,3,7,4,2,1,24]
the_second_array=[0x57,0x40,0xa3,0x78,0x7d,0x67,0x55,0x40,0x1e,0xae,0x5b,0x11,0x5d,0x40,0xaa,0x17,0x58,0x4f,0x7e,0x4d,0x4e,0x42,0x5d,0x51,0x57,0x5f,0x5f,0x12,0x1d,0x5a,0x4f,0xbf]
flag=""

for i in range(0,32):
    flag += chr((the_second_array[i] ^ 42) - some_array[i])

print(flag)
```

```
kali@kali:~/Downloads/simple$ ./solve.py 
shkCTF{h3ll0_fr0m_ASM_my_fr13nd}
```

We can verify the flag by passing it back into the binary, and it should return 1.

```
kali@kali:~/Downloads/simple$ ./main shkCTF{h3ll0_fr0m_ASM_my_fr13nd}
kali@kali:~/Downloads/simple$ echo $?
1
```

