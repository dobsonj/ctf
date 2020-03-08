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
