
# Put your thang down flip it and reverse it

Ra-ta-ta-ta-ta-ta-ta-ta-ta-ta.

## What are we dealing with?

Start with the essential research:

https://www.youtube.com/watch?v=cjIvu7e6Wq8

```
kali@kali:~/Downloads$ file missyelliott 
missyelliott: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b9102dff60f031b84a190121ab6d167ab825c298, for GNU/Linux 3.2.0, stripped
```

The file is an executable, run it and see what happens:

```
kali@kali:~/Downloads$ ./missyelliott 
Let me search ya.

Wrong. You need to work it.
```

It just takes an input and tries to validate it.

## Analysis

Decompile with Ghidra. Here is the entry function:

```c
void entry(undefined8 param_1,undefined8 param_2,undefined8 param_3)
{
  undefined8 in_stack_00000000;
  undefined auStack8 [8];
  
  __libc_start_main(FUN_0010137d,in_stack_00000000,&stack0x00000008,&LAB_00101410,&DAT_00101470,
                    param_3,auStack8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

`entry()` calls this function:

```c
undefined8 FUN_0010137d(void)
{
  size_t sVar1;
  
  puts("Let me search ya.");
  fgets(&DAT_00104040,0x2c,stdin);
  sVar1 = strnlen(&DAT_00104040,0x2b);
  if (sVar1 != 0x2b) {
    FUN_00101195();
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  FUN_001012f2();
  FUN_001011f7();
  FUN_001011bb();
  return 0;
}
```

It's looking for exactly 43 chars (0x2b). Otherwise, it fails with:

```c
void FUN_00101195(void)
{
  puts("Wrong. You need to work it.");
  return;
}
```

```
kali@kali:~/Downloads$ perl -e 'print "A"x43' | ./missyelliott
Let me search ya.
Wrong. You need to work it.
```

Alright, now we make it past the first check and into this function:

```c
void FUN_001012f2(void)
{
  int local_c;
  
  local_c = 0;
  while (local_c < 0x2b) {
    (&DAT_00104040)[local_c] = ~(&DAT_00104040)[local_c];
    local_c = local_c + 1;
  }
  return;
}
```

That takes the complement of each char, similar to this:

```
kali@kali:~/Downloads$ perl -e 'printf("%x\n",~(65));'
ffffffffffffffbe
```

The next function after the complement is:

```c
void FUN_001011f7(void)
{
  undefined uVar1;
  byte local_1b;
  int local_18;
  uint local_14;
  int local_10;
  
  local_18 = 0;
  while (local_1b = 0, local_18 < 0x2b) {
    local_14 = 0;
    while (local_14 < 8) {
      if (((byte)(1 << ((byte)local_14 & 0x1f)) & (&DAT_00104040)[local_18]) != 0) {
        local_1b = local_1b | (byte)(1 << (7 - (byte)local_14 & 0x1f));
      }
      local_14 = local_14 + 1;
    }
    (&DAT_00104040)[local_18] = local_1b;
    local_18 = local_18 + 1;
  }
  local_10 = 0;
  while (local_10 < 0x15) {
    uVar1 = (&DAT_00104040)[local_10];
    (&DAT_00104040)[local_10] = (&DAT_00104040)[0x2a - local_10];
    (&DAT_00104040)[0x2a - local_10] = uVar1;
    local_10 = local_10 + 1;
  }
  return;
}
```

`FUN_001011f7()` iterates over the input string and does some bitwise operations on each char.
Lol, then it reverses the string at the end of the function.
We need to derive the right flag as input. This would be the flag format for a total of 43 chars:

```
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
```

After the transformation above is done, the validation function compares `DAT_00104040` to `PTR_DAT_00104010`:

```c
void FUN_001011bb(void)
{
  int iVar1;
  
  iVar1 = strncmp(&DAT_00104040,PTR_DAT_00104010,0x2c);
  if (iVar1 == 0) {
    FUN_001011a8();
  }
  else {
    FUN_00101195();
  }
  return;
}
```

We want to hit this function:

```c
void FUN_001011a8(void)
{
  puts("You did it!  Was it worth it?");
  return;
}
```

We already know `DAT_00104040` is the input + transformations. That has to match `PTR_DAT_00104010`, which is just a pointer to `DAT_00102008`.

```
                             PTR_DAT_00104010                                XREF[1]:     FUN_001011bb:001011bf(R)  
        00104010 08 20 10        addr       DAT_00102008                                     = 41h    A
                 00 00 00 
                 00 00
```

So our input should equal the following after the transformations are done:

```
                             DAT_00102008                                    XREF[2]:     FUN_001011bb:001011cb(*), 
                                                                                          00104010(*)  
        00102008 41              ??         41h    A
        00102009 f5              ??         F5h
        0010200a 51              ??         51h    Q
        0010200b d1              ??         D1h
        0010200c 4d              ??         4Dh    M
        0010200d 61              ??         61h    a
        0010200e d5              ??         D5h
        0010200f e9              ??         E9h
        00102010 69              ??         69h    i
        00102011 89              ??         89h
        00102012 19              ??         19h
        00102013 dd              ??         DDh
        00102014 09              ??         09h
        00102015 11              ??         11h
        00102016 89              ??         89h
        00102017 cb              ??         CBh
        00102018 9d              ??         9Dh
        00102019 c9              ??         C9h
        0010201a 69              ??         69h    i
        0010201b f1              ??         F1h
        0010201c 6d              ??         6Dh    m
        0010201d d1              ??         D1h
        0010201e 7d              ??         7Dh    }
        0010201f 89              ??         89h
        00102020 d9              ??         D9h
        00102021 b5              ??         B5h
        00102022 59              ??         59h    Y
        00102023 91              ??         91h
        00102024 59              ??         59h    Y
        00102025 b1              ??         B1h
        00102026 31              ??         31h    1
        00102027 59              ??         59h    Y
        00102028 6d              ??         6Dh    m
        00102029 d1              ??         D1h
        0010202a 8b              ??         8Bh
        0010202b 21              ??         21h    !
        0010202c 9d              ??         9Dh
        0010202d d5              ??         D5h
        0010202e 3d              ??         3Dh    =
        0010202f 19              ??         19h
        00102030 11              ??         11h
        00102031 79              ??         79h    y
        00102032 dd              ??         DDh
        00102033 00              ??         00h
```

Put your thang down flip it and reverse it:

```
"\xDD\x79\x11\x19\x3D\xD5\x9D\x21\x8B\xD1\x6D\x59\x31\xB1\x59\x91\x59\xB5\xD9\x89\x7D\xD1\x6D\xF1\x69\xC9\x9D\xCB\x89\x11\x09\xDD\x19\x89\x69\xE9\xD5\x61\x4D\xD1\x51\xF5\x41"
```

## Solution

We can use the decompiled C code to determine the input string one character at a time.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char byte;

char *DAT_00102008="\xDD\x79\x11\x19\x3D\xD5\x9D\x21\x8B\xD1\x6D\x59\x31\xB1\x59\x91\x59\xB5\xD9\x89\x7D\xD1\x6D\xF1\x69\xC9\x9D\xCB\x89\x11\x09\xDD\x19\x89\x69\xE9\xD5\x61\x4D\xD1\x51\xF5\x41";

char input_template[44] = "DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}";

char DAT_00104040[44] = {0};

char *printable_chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

void transform_char(int local_18, const char foo)
{
        byte local_1b;
        uint local_14;

        DAT_00104040[local_18] = ~foo;
        local_1b = 0;
        local_14 = 0;
        while (local_14 < 8) {
                if (((byte)(1 << ((byte)local_14 & 0x1f)) & DAT_00104040[local_18]) != 0) {
                        local_1b = local_1b | (byte)(1 << (7 - (byte)local_14 & 0x1f));
                }
                local_14 = local_14 + 1;
        }
        DAT_00104040[local_18] = local_1b;
        return;
}

int main() {
        int npchars = strlen(printable_chars);
        strcpy(DAT_00104040,input_template);

        printf("printable chars: %s\n",printable_chars);
        printf("num printable chars: %d\n",npchars);
        printf("input template: %s\n",DAT_00104040);

        for (int cur = 0; cur <= 42; cur++) {
                for (int x = 0; x < npchars; x++) {
                        char ch = printable_chars[x];
                        transform_char(cur, ch);
                        if (DAT_00104040[cur] == DAT_00102008[cur]) {
                                input_template[cur] = ch;
                                printf("%s\n",input_template);
                                break;
                        }
                }
        }

        return 0;
}
```

Compile and run it

```
kali@kali:~/Downloads$ gcc missyelliott_solver.c && time ./a.out
printable chars:  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
num printable chars: 95
input template: DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIeXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesrXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreXXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesrevXXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveXXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRXXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdXXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnXXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAXXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtXXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIXXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpXXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpiXXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilXXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilFXXXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,XXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nXXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwXXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoXXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDXXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgXXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnXXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgniXXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihXXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTXXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyXXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMXXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMtXX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMtuX}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMtuP}
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMtuP}

real    0m0.001s
user    0m0.001s
sys     0m0.000s
```

This is the flag that was accepted:

```
DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMtuP}
```

