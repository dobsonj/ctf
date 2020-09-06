
# Actual ASLR 1

## Description

```
Category: Crypto
Difficulty: Easy
Author: LiveOverflow
First Blood: Cybernatural

Prove that you can win 0xf times against the house. Then go to Vegas.

Challenge Files: aaslr.zip
```

## Analysis

What happens when we just run `aaslr`?

```
kali@kali:~/Downloads/allesctf/aslr1$ ./aaslr
Welcome To The Actual-ASLR (AASLR) Demo
  1. throw dice
  2. create entry
  3. read entry
  4. take a guess

Select menu Item:
1
[>] Threw dice: 3
Welcome To The Actual-ASLR (AASLR) Demo
  1. throw dice
  2. create entry
  3. read entry
  4. take a guess

Select menu Item:
4
(1/16) guess next dice roll:
1
(2/16) guess next dice roll:
2
(3/16) guess next dice roll:
3
(4/16) guess next dice roll:
4
(5/16) guess next dice roll:
^C
```

You can throw dice, guess upcoming dice rolls, and create / read entries. This was a 2 part problem, and I only worked on the first part that was centered around the dice rolls.

Decompile `aaslr` with Ghidra and walk through the functions.

```c
void main(void)

{
  int iVar1;
  uint uVar2;
  code **ppcVar3;
  long in_FS_OFFSET;
  char local_118 [264];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  init_buffering();
  init_signal();
  ppcVar3 = (code **)aaslr_malloc(8);
  *ppcVar3 = throw_dice;
  ppcVar3[1] = create_entry;
  ppcVar3[2] = read_entry;
  ppcVar3[3] = take_guess;
  ppcVar3[4] = error_case;
  ENTRY = aaslr_malloc(0x7f8);
  do {
    while( true ) {
      while( true ) {
        print_menu();
        memset(local_118,0,0xff);
        read_input(0,local_118,0xff);
        iVar1 = strcmp(local_118,"1");
        if (iVar1 != 0) break;
        uVar2 = (**ppcVar3)();
        printf("[>] Threw dice: %d\n",(ulong)uVar2);
      }
      iVar1 = strcmp(local_118,"2");
      if (iVar1 != 0) break;
      uVar2 = (*ppcVar3[1])();
      printf("[>] Created new entry at index %d\n",(ulong)uVar2);
    }
    iVar1 = strcmp(local_118,"3");
    if (iVar1 == 0) {
      (*ppcVar3[2])();
    }
    else {
      iVar1 = strcmp(local_118,"4");
      if (iVar1 == 0) {
        (*ppcVar3[3])();
      }
      else {
        (*ppcVar3[4])(local_118);
      }
    }
  } while( true );
}
```

`take_guess` will give you a flag if you get all the guesses correct:

```c
void take_guess(void)

{
  int iVar1;
  int iVar2;
  long in_FS_OFFSET;
  int local_128;
  int local_124;
  char local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_128 = 0;
  local_124 = 0;
  while (local_124 < 0xf) {
    printf("(%d/16) guess next dice roll:\n",(ulong)(local_124 + 1));
    memset(local_118,0,0xff);
    read_input(0,local_118,0xff);
    iVar1 = atoi(local_118);
    iVar2 = throw_dice();
    if (iVar1 == iVar2) {
      local_128 = local_128 + 1;
    }
    local_124 = local_124 + 1;
  }
  if (local_128 == 0xf) {
    puts("[>] CORRECT! You should go to Vegas.");
    system("cat flag2");
  }
  else {
    puts("[!] WRONG!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

`throw_dice` is pretty self explanatory:

```c
ulong throw_dice(void)

{
  ulong uVar1;
  
  uVar1 = ranval();
  return (ulong)((int)uVar1 + (int)(uVar1 / 6) * -6 + 1);
}
```

`ranval` does some mathy stuff:

```c
long ranval(void)

{
  long lVar1;
  long lVar2;
  
  lVar1 = RANCTX._0_8_ - (RANCTX._8_8_ >> 5 | RANCTX._8_8_ << 0x1b);
  RANCTX._0_8_ = RANCTX._8_8_ ^ (RANCTX._16_8_ >> 0xf | RANCTX._16_8_ << 0x11);
  lVar2 = RANCTX._0_8_ + lVar1;
  RANCTX._8_8_ = RANCTX._16_8_ + RANCTX._24_8_;
  RANCTX._16_8_ = RANCTX._24_8_ + lVar1;
  RANCTX._24_8_ = lVar2;
  return lVar2;
}
```

How does this thing get seeded though?

`aaslr_malloc` calls `init_heap`:

```c
long aaslr_malloc(long param_1)

{
  long lVar1;
  ulong uVar2;
  
  if (HEAP == 0) {
    init_heap();
  }
  lVar1 = HEAP;
  if (HEAP != 0) {
    uVar2 = ranval();
    return uVar2 % (0x10000U - param_1) + lVar1;
  }
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

And `init_heap` gets the time in seconds since the epoch and passes the value into `raninit`:

```c
void init_heap(void)

{
  time_t tVar1;
  
  HEAP = mmap((void *)0x0,0x10000,3,0x22,-1,0);
  tVar1 = time((time_t *)0x0);
  raninit(tVar1);
  return;
}
```

And this is where it gets seeded:

```c
void raninit(undefined8 param_1)

{
  ulong local_18;
  
  RANCTX._0_8_ = 0xf1ea5eed;
  local_18 = 0;
  RANCTX._8_8_ = param_1;
  RANCTX._16_8_ = param_1;
  RANCTX._24_8_ = param_1;
  while (local_18 < 0x14) {
    ranval(RANCTX);
    local_18 = local_18 + 1;
  }
  return;
}
```

## Solution

Since the granularity is in seconds, we can start a local process at the same time as we create a connection to the remote host, and if they start within the same second (assuming no major clock skew) then the seed will be the same and we can feed the dice rolls from the local process into the guesses for the remote process.

```python
#!/usr/bin/python3
from pwn import *

#context.log_level='DEBUG'
p = process(['./aaslr'])
#r = process(['./aaslr'])
r = process(['ncat', '--ssl', '7b000000f298cf5bdd7b82ed.challenges.broker2.allesctf.net', '1337'])

p.recvuntil('Select menu Item:\n')
r.recvuntil('Select menu Item:\n')
r.sendline('4')

for i in range(15):
    p.sendline('1')
    p.recvuntil('[>] Threw dice: ')
    roll = p.recvline().rstrip()
    print(roll)
    #r.recvuntil('guess next dice roll:\n')
    r.sendline(roll)

r.recvuntil('[>] CORRECT! You should go to Vegas.\n')
flag = r.recvline()
print(flag)
```

Run it and we get the flag:

```
kali@kali:~/Downloads/allesctf/aslr1$ ./solve.py 
[+] Starting local process './aaslr': pid 13523
[+] Starting local process '/usr/bin/ncat': pid 13525
b'2'
b'4'
b'1'
b'1'
b'6'
b'5'
b'2'
b'5'
b'2'
b'2'
b'2'
b'2'
b'6'
b'4'
b'3'
b'ALLES{ILLEGAL_CARD_COUNTING!_BANNED}\n'
```

