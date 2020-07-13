#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned char byte;

void encryptFlag(byte *param_1)
{ 
  byte *pbVar1;
  byte *pbVar2;
  uint uVar3;
  byte bVar4;
  uint uVar5;
  uint uVar6;

  bVar4 = *param_1;
  pbVar1 = param_1;
  if (bVar4 == 0) {
    return;
  }
  while( 1 ) {
    uVar5 = (uint)bVar4;
    uVar3 = uVar5 - 10 & 0xff;
    uVar6 = uVar5;
    if ((bVar4 < 0x50) && (uVar6 = uVar3, 0x50 < uVar3)) {
      uVar6 = uVar5 + 0x46 & 0xff;
    }
    uVar6 = (uVar6 - 7 ^ 0x43) & 0xff;
    pbVar2 = pbVar1 + 1;
    *pbVar1 = (byte)(uVar6 << 6) | (byte)(uVar6 >> 2);
    bVar4 = *pbVar2;
    if (bVar4 == 0) break;
    uVar6 = (int)(pbVar2 + -(int)param_1) % 5;
    bVar4 = bVar4 << (-uVar6 & 7) | bVar4 >> (uVar6 & 0xff);
    if (uVar6 == 2) {
      bVar4 = bVar4 - 1;
    }
    *pbVar2 = bVar4;
    bVar4 = *pbVar2;
    pbVar1 = pbVar2;
  }
  return;
}

int main()
{                                                                                                           char *printable_chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";                                                                            int npchars = strlen(printable_chars);                                                                                                                                                                  byte nums[35] = {0x0A, 0xFB, 0xF4, 0x88, 0xDD, 0x9D, 0x7D, 0x5F, 0x9E, 0xA3, 0xC6, 0xBA, 0xF5, 0x95, 0x5D, 0x88, 0x3B, 0xE1, 0x31, 0x50, 0xC7, 0xFA, 0xF5, 0x81, 0x99, 0xC9, 0x7C, 0x23, 0xA1, 0x91, 0x87, 0xB5, 0xB1, 0x95, 0xE4};
        byte flag[36] = {'r', 'g', 'b', 'C', 'T', 'F', '{', 0};

        for (int cur = 0; cur < sizeof(flag); cur++) {
                for (int x = 0; x < npchars; x++) {
                        char ch = printable_chars[x];
                        byte arr[36] = {0};
                        strcpy(arr,flag);
                        arr[cur] = ch;
                        encryptFlag(arr);
                        if (nums[cur] == arr[cur]) {
                                flag[cur] = ch;
                                printf("%s\n",flag);
                                break;
                        }
                }
        }

        printf("\n");
}
