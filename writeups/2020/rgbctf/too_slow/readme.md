
# Too Slow

## Description

```
 I've made this flag decryptor! It's super secure, but it runs a little slow.
```

Category: Reversing

## Analysis

We're looking at an amd64 executable:

```
kali@kali:~/Downloads$ ls -l a.out
-rwxr-xr-x 1 kali kali 16856 Jul 11 15:07 a.out
kali@kali:~/Downloads$ file a.out
a.out: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=462dfe207acdfe1da2133cac6b69b45de5169ee2, for GNU/Linux 3.2.0, not stripped
```

Try running it, and it seems to be computing... "something" for a really long time.

```
kali@kali:~/Downloads$ ./a.out
Flag Decryptor v1.0
Generating key...
^C
```

### Decompile with Ghidra

`main()` is pretty simple, it just calls `getKey()` and then passes that value into `win()`

```c
undefined8 main(void)
{
  uint uVar1;
  
  puts("Flag Decryptor v1.0");
  puts("Generating key...");
  uVar1 = getKey();
  win((ulong)uVar1);
  return 0;
}
```

`getKey()` has a nested `while` loop, before returning `local_10`:

```c
ulong getKey(void)
{
  uint local_10;
  uint local_c;
  
  local_10 = 0;
  while (local_10 < 0x265d1d23) {
    local_c = local_10;
    while (local_c != 1) {
      if ((local_c & 1) == 0) {
        local_c = (int)local_c / 2;
      }
      else {
        local_c = local_c * 3 + 1;
      }
    }
    local_10 = local_10 + 1;
  }
  return (ulong)local_10;
}
```

I'm not sure what the purpose of `local_c` is since it's never returned. Maybe it's just there to take up time. But `local_10` should always be returned as `0x265d1d23`.

And what about `win()`? That just takes the key and does an xor against a hardcoded set of hex values, then prints the resulting string as a flag.

```c
void win(uint param_1)
{
  long in_FS_OFFSET;
  uint local_3c;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  undefined4 local_18;
  undefined local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_38 = 0x12297e12426e6f53;
  local_30 = 0x79242e48796e7141;
  local_28 = 0x49334216426e2e4d;
  local_20 = 0x473e425717696a7c;
  local_18 = 0x42642a41;
  local_14 = 0;
  local_3c = 0;
  while (local_3c < 9) {
    *(uint *)((long)&local_38 + (ulong)local_3c * 4) =
         *(uint *)((long)&local_38 + (ulong)local_3c * 4) ^ param_1;
    local_3c = local_3c + 1;
  }
  printf("Your flag: rgbCTF{%36s}\n",&local_38);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

The first thing I tried was to recompile `win()` and `main()` along with a simpler `getKey()` function that just returns `0x265d1d23`:

```c
ulong getKey(void)
{
  uint local_10 = 0x265d1d23;
  return (ulong)local_10;
}
```

But that just got me:

```
Your flag: rgbCTF{pr3d1ct4#]&b79d_w41t_can33d5_nobl3_H.$y}
```

That flag wasn't accepted, and it doesn't look right anyway. I tried a few other things too, including experimenting with the original `getKey()` function to confirm that there is no weird integer overflow going on and that `local_c` is just there to take up time (and the inner loop never finishes).

I reached out to the author of this challenge on discord and they provided a hint:

```
ungato  Today at 3:19 PM
I'm guessing that in decompilation/recompilation, win was somehow messed up
Because that is the correct key (good job!)
If you find a way to use it with the original win() it should work
```

So I guess we're talking about binary patching now, cool, I've been wanting to try that :)

Here's the disassembly for `main()`:

```
kali@kali:~/Downloads$ objdump -d a.out
...
00000000000012af <main>:
    12af:       f3 0f 1e fa             endbr64 
    12b3:       55                      push   %rbp
    12b4:       48 89 e5                mov    %rsp,%rbp
    12b7:       48 83 ec 10             sub    $0x10,%rsp
    12bb:       89 7d fc                mov    %edi,-0x4(%rbp)
    12be:       48 89 75 f0             mov    %rsi,-0x10(%rbp)
    12c2:       48 8d 3d 54 0d 00 00    lea    0xd54(%rip),%rdi        # 201d <_IO_stdin_used+0x1d>
    12c9:       e8 a2 fd ff ff          callq  1070 <puts@plt>
    12ce:       48 8d 3d 5c 0d 00 00    lea    0xd5c(%rip),%rdi        # 2031 <_IO_stdin_used+0x31>
    12d5:       e8 96 fd ff ff          callq  1070 <puts@plt>
    12da:       b8 00 00 00 00          mov    $0x0,%eax
    12df:       e8 73 ff ff ff          callq  1257 <getKey>
    12e4:       89 c7                   mov    %eax,%edi
    12e6:       e8 9e fe ff ff          callq  1189 <win>
    12eb:       b8 00 00 00 00          mov    $0x0,%eax
    12f0:       c9                      leaveq 
    12f1:       c3                      retq   
    12f2:       66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
    12f9:       00 00 00 
    12fc:       0f 1f 40 00             nopl   0x0(%rax)
```

We should be able to patch `0x12da` to set `eax` to `0x265d1d23` and then call `win()` instead of `getKey()`.

## Solution

This is the first time I've done this, so it took a little trial-and-error, but this is the final version:

```python
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
```

I probably could have just `nop`d away the call to `getKey()` instead of copying all the instructions to call and return from `win()`. Or for that matter, probably could have `nop`d out the inner loop in `getKey()`. In any case, this approach worked fine.

Run it and we get our flag:

```
kali@kali:~/Downloads$ python3 too_slow.py && ./a.out_patched 
[*] '/home/kali/Downloads/a.out'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
/home/kali/Downloads/a.out
    12da:       b8 00 00 00 00          mov    eax, 0x0
    12df:       e8 73 ff ff ff          call   0x1257
    12e4:       89 c7                   mov    edi, eax
    12e6:       e8 9e fe ff ff          call   0x1189
    12eb:       b8 00 00 00 00          mov    eax, 0x0
    12f0:       c9                      leave  
    12f1:       c3                      ret    
    12f2:       66 2e 0f 1f 84 00 00    nop    WORD PTR cs:[rax+rax*1+0x0]
    12f9:       00 00 00 
    12fc:       0f 1f 40 00             nop    DWORD PTR [rax+0x0]
    1300:       f3                      repz
    1301:       0f                      .byte 0xf
/home/kali/Downloads/a.out_patched
    12da:       b8 23 1d 5d 26          mov    eax, 0x265d1d23
    12df:       89 c7                   mov    edi, eax
    12e1:       e8 a3 fe ff ff          call   0x1189
    12e6:       b8 00 00 00 00          mov    eax, 0x0
    12eb:       c9                      leave  
    12ec:       c3                      ret    
    12ed:       00 00                   add    BYTE PTR [rax], al
    12ef:       00 c9                   add    cl, cl
    12f1:       c3                      ret    
    12f2:       66 2e 0f 1f 84 00 00    nop    WORD PTR cs:[rax+rax*1+0x0]
    12f9:       00 00 00 
    12fc:       0f 1f 40 00             nop    DWORD PTR [rax+0x0]
    1300:       f3                      repz
    1301:       0f                      .byte 0xf
Flag Decryptor v1.0
Generating key...
Your flag: rgbCTF{pr3d1ct4bl3_k3y_n33d5_no_w41t_cab79d}
```

The flag is:

```
rgbCTF{pr3d1ct4bl3_k3y_n33d5_no_w41t_cab79d}
```

