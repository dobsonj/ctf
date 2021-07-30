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

