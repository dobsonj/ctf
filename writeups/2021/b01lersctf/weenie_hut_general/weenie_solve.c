#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int main() {
        srand(0x11c4);
        uint32_t uVar1 = rand();
        uint32_t uVar2 = rand();
        printf("uVar1 = %u\n", uVar1);
        printf("uVar2 = %u\n", uVar2);

        uint32_t x = uVar2 ^ uVar1 ^ 0x3597b741;
        printf("uVar2 ^ uVar1 ^ 0x3597b741 = %u\n", x);

        if ((x ^ uVar1 ^ 0x3597b741) == uVar2)
                printf("bctf{%u}\n", x);

        return 0;
}
