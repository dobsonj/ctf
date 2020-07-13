# Advanced Reversing Mechanics 1

## Description

```
 Very very advanced trust me
 71, 66, 61, 42, 53, 45, 7A, 40, 51, 4C, 5E, 30, 79, 5E, 31, 5E, 64, 59, 5E, 38, 61, 36, 65, 37, 63, 7C,
```

Category: Reversing

## Analysis

We're looking at a tiny ARM object:

```
kali@kali:~/Downloads$ ls -l easy.o 
-rw-r--r-- 1 kali kali 1432 Jul 11 18:44 easy.o
kali@kali:~/Downloads$ file easy.o 
easy.o: ELF 32-bit LSB relocatable, ARM, EABI5 version 1 (SYSV), not stripped
```

### Decompile with Ghidra

There's only a couple of functions of interest. Let's take a look at `main()` first.

```c
undefined4 main(undefined4 param_1,int param_2)
{
  char *pcVar1;
  byte *pbVar2;
  byte *pbVar3;
  byte local_110 [256];
  
  pbVar2 = local_110;
  pcVar1 = stpcpy((char *)local_110,*(char **)(param_2 + 4));
  while (local_110[0] != 0) {
    *pbVar2 = local_110[0] - 1;
    pbVar2 = pbVar2 + 1;
    local_110[0] = *pbVar2;
  }
  if (pcVar1 + -(int)local_110 != (char *)0x0) {
    pbVar2 = local_110;
    do {
      pbVar3 = pbVar2 + 1;
      printf("%02X, ",(uint)*pbVar2);
      pbVar2 = pbVar3;
    } while (local_110 + (int)(pcVar1 + -(int)local_110) != pbVar3);
  }
  putchar(10);
  return 0;
}
```

That makes a copy of the input string, decrements each character, then prints out the string as a series of hex values (one per byte). The other function is `encryptFlag()` which basically does the same decrement on each character:

```c
void encryptFlag(char *param_1)
{
  char cVar1;
  
  cVar1 = *param_1;
  if (cVar1 == '\0') {
    return;
  }
  do {
    *param_1 = cVar1 + -1;
    param_1 = param_1 + 1;
    cVar1 = *param_1;
  } while (cVar1 != '\0');
  return;
}
```

And here's the disassembly:

```
                             //
                             // .text 
                             // SHT_PROGBITS  [0x0 - 0x23]
                             // ram: 00010000-00010023
                             //
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined encryptFlag()
             undefined         r0:1           <RETURN>
                             encryptFlag                                     XREF[2]:     Entry Point(*), 
                                                                                          _elfSectionHeaders::00000034(*)  
        00010000 00 30 d0 e5     ldrb       r3,[r0,#0x0]
        00010004 00 00 53 e3     cmp        r3,#0x0
        00010008 1e ff 2f 01     bxeq       lr
                             LAB_0001000c                                    XREF[1]:     0001001c(j)  
        0001000c 01 30 43 e2     sub        r3,r3,#0x1
        00010010 00 30 c0 e5     strb       r3,[r0,#0x0]
        00010014 01 30 f0 e5     ldrb       r3,[r0,#0x1]!
        00010018 00 00 53 e3     cmp        r3,#0x0
        0001001c fa ff ff 1a     bne        LAB_0001000c
        00010020 1e ff 2f e1     bx         lr
```

That's all there is to it--pretty simple. Since this just decrements each character, all we have to do is take the array of hex values from the description, increment each character, and print out the resulting string.

## Solution

```python
#!/usr/bin/python3
nums = bytearray([0x71, 0x66, 0x61, 0x42, 0x53, 0x45, 0x7A, 0x40, 0x51, 0x4C, 0x5E, 0x30, 0x79, 0x5E, 0x31, 0x5E, 0x64, 0x59, 0x5E, 0x38, 0x61, 0x36, 0x65, 0x37, 0x63, 0x7C])
for i in range(len(nums)):
    nums[i] += 1
print(nums.decode('ASCII'))
```

```
kali@kali:~/Downloads$ ./adv_rev_mech1.py 
rgbCTF{ARM_1z_2_eZ_9b7f8d}
```

