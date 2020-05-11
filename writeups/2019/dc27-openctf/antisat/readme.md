
# antisat.exe

Our cluster just locked up. Could you see why our sat solver isn't tearing through this? It's a standard Windows 64 binary.

## Analysis

Egan decompiled antisat.exe with Ghidra and pulled out main():

```
/* DISPLAY WARNING: Type casts are NOT being printed */

int main(int _Argc,char **_Argv,char **_Env)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  
  __main();
  if (_Argc < 2) {
    .text("Usage: ./antisat num");
    iVar2 = 1;
  }
  else {
    uVar1 = .text(_Argv[1]);
    uVar3 = 0;
    do {
      uVar4 = uVar3 + 1;
      uVar1 = uVar1 + uVar3 + (uVar3 ^ 0x189) + (uVar3 & 0xff11ff) ^
              (((uVar3 & 0xff11ff) * 0x189) % 0x33333) * (uVar1 + 0xff11ff & 0x257a0e1);
      .text("%i\n");
      uVar3 = uVar4;
    } while (uVar4 != 1000000);
    if (uVar1 == 0xa9daa95) {
      .text("Good job! flag{%s}\n",_Argv[1]);
      iVar2 = 0;
    }
    else {
      .text("See ya later.");
      iVar2 = 1;
    }
  }
  return iVar2;
}
```

Then we just tweaked it and recompiled it natively without the slow printf():

```
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[])

{
  unsigned int uVar1;
  int iVar2;
  unsigned int uVar3;
  unsigned int uVar4;

  if (argc < 2) {
    printf("Usage: ./antisat num\n");
    iVar2 = 1;
  }
  else {
    uVar1 = atoi(argv[1]);
    uVar3 = 0;
    do {
      uVar4 = uVar3 + 1;
      uVar1 = uVar1 + uVar3 + (uVar3 ^ 0x189) + (uVar3 & 0xff11ff) ^ (((uVar3 & 0xff11ff) * 0x189) % 0x33333) * (uVar1 + 0xff11ff & 0x257a0e1);
      //printf("%d\n",uVar1);
      uVar3 = uVar4;
    } while (uVar4 != 1000000);

    if (uVar1 == 0xa9daa95) {
      printf("Good job! flag{%s}\n",argv[1]);
      iVar2 = 0;
    }
    else {
      printf("See ya later.\n");
      iVar2 = 1;
    }
  }
  return iVar2;
}
```

That was tested by comparing with the results from running antisat.exe in a Windows VM.

## Get the flag

After that, it just took a few minutes to brute force it:

```
nulladdr:~$ gcc -o antisat antisat.c 
nulladdr@unknown:~$ for i in `seq 1 1000000`; do ./antisat $i | grep flag; done
Good job! flag{18772}
^C
```

