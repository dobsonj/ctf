#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

typedef struct customer{
        char cardId[9];
        int state;
        char name[21];
        char pin[7];
        long long balance;
        char telNumber[16];
        char address[41];
        struct customer * next;
} Customer;

int main() {
        char *filename1="customer.dat";
        char *alphabet="0123456789abcdef";
        char *prefix="flag{";
        FILE *fptr;

        fptr = fopen(filename1,"ab+");
        if (fptr == NULL) {
                printf("failed to open %s\n", filename1);
                exit(1);
        }

        for (int i = 0; i < strlen(alphabet); i++) {
                for (int j = 0; j < strlen(alphabet); j++) {
                        for (int k = 0; k < strlen(alphabet); k++) {
                                Customer cust = {0};
                                strcpy(cust.cardId, prefix);
                                cust.cardId[5] = alphabet[i];
                                cust.cardId[6] = alphabet[j];
                                cust.cardId[7] = alphabet[k];
                                strcpy(cust.name, cust.cardId);
                                strcpy(cust.pin, "111111");
                                strcpy(cust.telNumber, "1800hackers");
                                strcpy(cust.address, "localhost");

                                fseek(fptr, 0L, SEEK_END);
                                fwrite(&cust,sizeof(Customer),1,fptr);
                        }
                }
        }

        fclose(fptr);
        return 0;
}

