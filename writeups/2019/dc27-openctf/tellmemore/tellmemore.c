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
  size_t sVar4;
  
  __size = strlen(pcParm1);
  pvVar3 = malloc(__size);
  local_1c = 0;
  while( local_1c < __size ) {
    sVar4 = strlen(pcParm2);
    iVar2 = toupper((int)pcParm2[(ulong)local_1c % sVar4]);
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
	char *str1 = "xzyu{h3v0xev4ln}";
	char *str2 = "SOYOULYKECATS";

	printf("%s\n",str1);
	printf("%s\n",str2);
	printf(decode(str1, str2));
}

