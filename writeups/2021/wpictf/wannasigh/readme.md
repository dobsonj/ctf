
# WannaSigh++

## Description

```
The WannaSigh devs have returned - and their new ransomware has encrypted the flag! We first noticed that flag.txt was missing late last Friday night. One of our analysts was able to find this sample, but the evolved ransware has a new way of encrypting files that we have been unable to reverse. The malware is not only more sophisticated, but it appears to be tempermental and resists analysis. As per usual, the WannaSigh++ sample has been zipped with the password "infected".

challenge creator: Abjuri5t (John F)

*The BTC address in the ransom is for the EFF- you will not actually get the flag if you give them $500 (You should never pay the ransom!). Also the ransomware (it feels weird writing ransomware) should only target files named "flag.txt" - but as always you should be careful.

Points: 400
```

## Solution

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
        int iVar1;
        int iVar2;
        FILE *flag = fopen("flag.txt","w");
        FILE *enc = fopen("your-flag.ransomed","r");
        srand(1618617746);
        do {
                iVar1 = fgetc(enc);
                iVar2 = rand();
                fputc((iVar1 ^ iVar2),flag);
        } while (iVar1);
        fclose(flag);
        fclose(enc);
        return 0;
}
```

