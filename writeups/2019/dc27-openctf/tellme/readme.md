# tellme

OK, do you think you know my secret? See if you can guess what I'm expecting to hear.

## Analysis

Decompile it with Ghidra and there are two important functions:

```
undefined8 FUN_0010141a(void)
{
  int iVar1;
  size_t local_20;
  char *local_18;
  char *local_10;
  
  local_18 = 0x0;
  local_20 = 0;
  puts("Do you know?");
  printf("Tell me: ");
  getline(&local_18,&local_20,stdin);
  strtok(local_18,"\n");
  local_10 = FUN_00101215(s_xzyu{hfkxcbhmloaoftay}_001040b0,s_SOYOULYKECATS_001040a0);
  iVar1 = strcmp(local_18,local_10);
  if (iVar1 == 0) {
    puts("You got it!");
  }
  else {
    puts("You don\'t know, huh?");
  }
  free(local_10);
  return 0;
}
```

```
void * FUN_00101215(char *pcParm1,char *pcParm2)
{
  char cVar1;
  int iVar2;
  size_t __size;
  void *pvVar3;
  ushort **ppuVar4;
  uint local_1c;
  
  __size = strlen(pcParm1);
  pvVar3 = malloc(__size);
  local_1c = 0;
  while( true ) {
    __size = strlen(pcParm1);
    if (__size <= local_1c) break;
    __size = strlen(pcParm2);
    iVar2 = toupper(pcParm2[local_1c % __size]);
    ppuVar4 = __ctype_b_loc();
    if (((*ppuVar4)[pcParm1[local_1c]] & 0x100) == 0) {
      ppuVar4 = __ctype_b_loc();
      if (((*ppuVar4)[pcParm1[local_1c]] & 0x200) == 0) {
        cVar1 = pcParm1[local_1c];
      }
      else {
        iVar2 = (pcParm1[local_1c] + -0x47) - (iVar2 + -0x41);
        cVar1 = iVar2 + (iVar2 / 0x1a) * -0x1a + 'a';
      }
    }
    else {
      iVar2 = (pcParm1[local_1c] + -0x27) - (iVar2 + -0x41);
      cVar1 = iVar2 + (iVar2 / 0x1a) * -0x1a + 'A';
    }
    *(pvVar3 + local_1c) = cVar1;
    local_1c = local_1c + 1;
  }
  return pvVar3;
}
```

Notice that `FUN_0010141a()` is passing 2 string constants into `FUN_00101215()`:

```
  xzyu{hfkxcbhmloaoftay}
  SOYOULYKECATS
```

And if the result of `FUN_00101215()` is the same as our input, we win.

```
  local_10 = FUN_00101215(s_xzyu{hfkxcbhmloaoftay}_001040b0,s_SOYOULYKECATS_001040a0);
  iVar1 = strcmp(local_18,local_10);
  if (iVar1 == 0) {
    puts("You got it!");
  }
```

## Solution

Just recompile that function in a separate program, pass in those 2 static strings, and print the output.

```
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void * decode(char *pcParm1,char *pcParm2)
{
  char cVar1;
  int iVar2;
  size_t __size;
  void *pvVar3;
  uint local_1c;

  __size = strlen(pcParm1);
  pvVar3 = malloc(__size);
  local_1c = 0;
  while( 1 ) {
    __size = strlen(pcParm1);
    if (__size <= (ulong)local_1c) break;
    __size = strlen(pcParm2);
    iVar2 = toupper((int)pcParm2[(ulong)local_1c % __size]);
    const ushort **ppuVar4 = __ctype_b_loc();
    if (((*ppuVar4)[(long)pcParm1[(ulong)local_1c]] & 0x100) == 0) {
      const ushort **ppuVar4 = __ctype_b_loc();
      if (((*ppuVar4)[(long)pcParm1[(ulong)local_1c]] & 0x200) == 0) {
        cVar1 = pcParm1[(ulong)local_1c];
      }
      else {
        iVar2 = ((int)pcParm1[(ulong)local_1c] + -0x47) - (iVar2 + -0x41);
        cVar1 = (char)iVar2 + (char)(iVar2 / 0x1a) * -0x1a + 'a';
      }
    }
    else {
      iVar2 = ((int)pcParm1[(ulong)local_1c] + -0x27) - (iVar2 + -0x41);
      cVar1 = (char)iVar2 + (char)(iVar2 / 0x1a) * -0x1a + 'A';
    }
    *(char *)((long)pvVar3 + (ulong)local_1c) = cVar1;
    local_1c = local_1c + 1;
  }
  return pvVar3;
}

int main() {
        char *str1 = "xzyu{hfkxcbhmloaoftay}";
        char *str2 = "SOYOULYKECATS";

        printf("%s\n",str1);
        printf("%s\n",str2);
        printf(decode(str1, str2));
}
```

The output of this program is what we need to pass into tellme to confirm the flag.

```
root@kali:~/Downloads# ./a.out 
xzyu{hfkxcbhmloaoftay}
SOYOULYKECATS
flag{whataboutacalico}
root@kali:~/Downloads# echo 'flag{whataboutacalico}' | ./tellme
Do you know?
Tell me: You got it!
```

