
# Doors of Durin

## Description

```
Category: Crypto
Difficulty: Easy
Author: 0x4d5a

Can you pass the guard who watches over the Doors of Durin?

Challenge Files: door.c gatekeeper.py
```

## Analysis

Let's start by looking at `gatekeeper.py`:

```python
#!/usr/bin/python3
  
import string
import hashlib
import base64
import socket
import time

goodHashes = {}

print("Welcome to the \"Doors of Durin\"")
print("I'm the gatekeeper of this ancient place")
print("A long time ago those doors weren't in need of a gatekeeper. But in recent time, especially after the big success of J.R.R. Tolkien, everyone knows the secret words. The passphrase to open the door to the precious flag!")
print("The flag had a lot of visitors and wants to be kept alone. So its my job to keep anyout out")
print("Only real skilled hackers are allowed here. Once you have proven yourself worthy, the flag is yours")

def generateSecretHash(byteInput):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha384()

    blake2b = hashlib.blake2b()

    md5.update(byteInput)
    sha1.update(md5.digest())
    md5.update(sha1.digest())

    for i in range(0, 2938):
        sha256.update(md5.digest())

    for k in range(-8222, 1827, 2):
        sha1.update(sha256.digest())
        sha256.update(sha1.digest())

    for j in range(20, 384):
        blake2b.update(sha256.digest())

    return blake2b.hexdigest()

def passToGate(byteInput):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("doorsofdurin_door", 1024))
        s.settimeout(1)
        s.sendall(byteInput + b"\n")
        time.sleep(1)
        data = s.recv(1024)
    return data

while True:
    try:
        currentInput = input("Give me your input:")

        bytesInput = base64.b64decode(currentInput)
        print("Doing magic, stand by")
        hashed = generateSecretHash(bytesInput)

        if hashed in goodHashes:
            print(passToGate(bytesInput))
        else:
            if b"sp3akfr1end4nd3nt3r" in bytesInput:
                print("Everybody knows the magic words. I can't hear it anymore! Go away! *smash*")
                exit(0)
            else:
                goodHashes[hashed] = bytesInput
                print(passToGate(bytesInput))

    except Exception as e:
        print(e)
```

It accepts base64 input, decodes it, and it will pass the decoded input through a socket to `door.c`. But notice that if you pass the magic word directly, it throws an error:

```python
        if hashed in goodHashes:
            print(passToGate(bytesInput))
        else:
            if b"sp3akfr1end4nd3nt3r" in bytesInput:
                print("Everybody knows the magic words. I can't hear it anymore! Go away! *smash*")
                exit(0)
            else:
                goodHashes[hashed] = bytesInput
                print(passToGate(bytesInput))
```

```
kali@kali:~/Downloads/allesctf/doors$ echo sp3akfr1end4nd3nt3r | base64 | python3 gatekeeper.py Welcome to the "Doors of Durin"
I'm the gatekeeper of this ancient place
A long time ago those doors weren't in need of a gatekeeper. But in recent time, especially after the big success of J.R.R. Tolkien, everyone knows the secret words. The passphrase to open the door to the precious flag!
The flag had a lot of visitors and wants to be kept alone. So its my job to keep anyout out
Only real skilled hackers are allowed here. Once you have proven yourself worthy, the flag is yours
Give me your input:Doing magic, stand by
Everybody knows the magic words. I can't hear it anymore! Go away! *smash*
```

`generateSecretHash` starts with an MD5 hash of our input, and then piles on a bunch of other hashes on top of that:

```python
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha384()

    blake2b = hashlib.blake2b()

    md5.update(byteInput)
    sha1.update(md5.digest())
    md5.update(sha1.digest())
...
```

This is important, because MD5 is weak and this looks like a hash collision thing.

Now look at `door.c`:

```c
#include<stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <unistd.h>

#define MAGIC_WORD "sp3akfr1end4nd3nt3r"
int main() {
    char input[255];
    char flag[255];

    scanf("%254s", input);
        printf("You said: %s\n", input);

    if (strcmp(input, MAGIC_WORD) == 0)
    {   
        int fd = open("./flag", O_RDONLY);
        if (fd == -1)
        {   
            printf("Something went wrong! Thats a bug, please report!\n");
            return 1;
        }

        read(fd, flag, 254);
        printf("Flag: %s\n", flag);
    }
    else
    {   
        printf("Nope :/\n");
    }   

        return 0;
}
```

Once we get past the gatekeeper, the door will give us the flag if the `strcmp` matches `sp3akfr1end4nd3nt3r`.

In order to get past the gatekeeper, our first input needs to be something that does _not_ contain `sp3akfr1end4nd3nt3r` but still has the same md5 hash as a second input which _does_ contain `sp3akfr1end4nd3nt3r` and will pass the `strcmp` check in `door.c`. The first input will cause `gatekeeper.py` to add the hash to `goodHashes`, allowing our second input with the matching hash to be passed on to the door.

We need a chosen-prefix collision, which is much more expensive than an identical-prefix collision:

<https://github.com/corkami/collisions#chosen-prefix-collisions>

And after digging around and playing with a few tools, hashclash seemed to have everything we need:

<https://github.com/cr-marcstevens/hashclash>

You can compile this with CUDA enabled and it would be _way_ faster to run on a GPU, but unfortunately I didn't have quick access to an Nvidia GPU for this exercise. Need to get my AWS account setup with a GPU quota for next time.

So I ran this on my kali VM using 8 vcpu's of my Ryzen 2700X and it finished after ~5 hours:

```
kali@kali:~/Downloads/hashclash/doors$ ../scripts/cpc.sh input.txt input2.txt 
...
Block 1: workdir6/coll1_1758829728
cd 2f d6 b8 fb 7b 92 ce 37 84 2a 14 07 e5 bd 45 
32 97 88 12 d7 ec e7 68 08 81 32 57 e5 28 25 9d 
29 64 17 9f 02 6d bd d9 be e8 62 9e 18 b5 fe 25 
0e 98 d1 c7 d7 7e c8 30 2f bd ae dd ad be 9d 00 
Block 2: workdir6/coll2_1758829728
cd 2f d6 b8 fb 7b 92 ce 37 84 2a 14 07 e5 bd 45 
32 97 88 12 d7 ec e7 68 08 81 32 57 e5 28 25 9d 
29 64 17 9f 02 6d bd d9 be e8 62 9e 18 b5 02 26 
0e 98 d1 c7 d7 7e c8 30 2f bd ae dd ad be 9d 00 
Found collision!
[*] Step 6 completed
[*] Number of backtracks until now: 1
[*] Collision generated: input.txt.coll input2.txt.coll
bbfb0268fa9c508de491736353a7a0f9  input.txt.coll
bbfb0268fa9c508de491736353a7a0f9  input2.txt.coll
[*] Process completed in 308 minutes (1 backtracks).
```

Only one problem: *I forgot the freakin' null char!*

```
kali@kali:~/Downloads/hashclash/doors$ cat input.txt.coll | ./door
You said: sp3akfr1end4nd3nt3r=b�u�M뀓�1��0E�q�
Nope :/
```

![](mundane_detail.jpg)

Let's clean up and try that again:

```
kali@kali:~/Downloads/hashclash/doors$ rm *.coll *.bin step*.log
kali@kali:~/Downloads/hashclash/doors$ rm -r workdir* upper_1_640000/ logs/ data/
kali@kali:~/Downloads/hashclash/doors$ perl -e 'print "sp3akfr1end4nd3nt3r\0"' > input.txt
kali@kali:~/Downloads/hashclash/doors$ perl -e 'print "\0"' > input2.txt
kali@kali:~/Downloads/hashclash/doors$ ../scripts/cpc.sh input.txt input2.txt
...
```

And at this point I'm worried if this will finish before the CTF is over, so I quickly spun up a 32x64 instance on digitalocean and ran the same thing there:

```
root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# perl -e 'print "sp3akfr1end4nd3nt3r\0"' > file1.txt
root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# perl -e 'print "\0"' > file2.txt
root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# hexdump -C file1.txt
00000000  73 70 33 61 6b 66 72 31  65 6e 64 34 6e 64 33 6e  |sp3akfr1end4nd3n|
00000010  74 33 72 00                                       |t3r.|
00000014
root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# hexdump -C file2.txt
00000000  00                                                |.|
00000001
root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# ../scripts/cpc.sh file1.txt file2.txt
...
```

The 32 vcpu run finished first, in about 3 hours.

```
Found collision!
[*] Step 10 completed
[*] Number of backtracks until now: 3
[*] Collision generated: file1.txt.coll file2.txt.coll
08172ba29c07c72c055d4f58c786434a  file1.txt.coll
08172ba29c07c72c055d4f58c786434a  file2.txt.coll
[*] Process completed in 214 minutes (3 backtracks).
```

So this was the input I used in my solution:

```
root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# cat file1.txt.coll | base64 --wrap=0
c3AzYWtmcjFlbmQ0bmQzbnQzcgA9YoQRAXXTTeuAk94xwdkwRfu+HnHwCmN1qDCqmBfK4wAAAAAL5sFBbqmL2SuFVqJ+/Wv3Icp+sViaoSk5sDHeoJ7pdwFQKAyoxlRj17aDLUQdmRpuOPIXGZPEDE9Pt7UBVdD5qQOm/OMxCJH6SXdU5wUGU6LwWNe3+BuV07DNa9X3rlB60gWRlFnQqSzEvvfLpWUSiL7QXoLn1CBP6LwHNdW2gWRSdG5802D7S00Gzig+MwyLLJLJCc7rPYgEISekGjsk00M5SGFho05Sf9ufwBiCIT0r8Re1mgHCRbnhmmmueTWWSLyX6+TpQxUd+b29mKPc62RoloV5EDagO+iSfuvtML3pPKUyWNIk2e79sn7D8xU6aOwXo57qUjFF0GkkR3kFg8WEdP9lWUrnK02nwn9ygpbfNJUvEXoZ/iaHmyaZMz42h70mg1UQbTBBNR+6sgfsNplzzHrkOHwna5ybyAPHlIsB2P/XcgzR50EUFlLXi8QZkHvkZY4/yTuM6SujWmdl4PukRWoLKzNAvdQ5EzDrARXd1UrdR5/AVUPebRYA3aLXB4oRDf12ugwayKapfgzjDz0gjheqdOk306c1C1W4vdW0RgLm7L87SifAR2gzbMV2jex6NvjFACrgRF2OrSQTUhkTP1SMwEzP0gI5j5wingNDw0clCn0shaItsnqrwmMP+fUCGjU5F7W+y3LwQ6VLTBPS+sVehDGMD+sJPAZ9eAW2n7yS6Grw9/6D2GswDSgDe42BgPRXhv+Odsrnd7s3bvEPHfATAkl5aCgtFhBq3nmOg0kq32bDW0F0NwHEAx/FCfx0CGX73IwzhMH11v/Mk7+8GGD5NJNhcvrG12rSrSAoSD0pAGW7kOOeyVmpm8URLKMUPU78oExKARkH7O/oP1qobvlbkeOiz/Ldgp3gv4OC/7qwtPsnFsBzaUZj5arm5mNrB4/+kWaA1l6OWtu9LBQV3i3QICfgGkcYojjskBKuQfhKV499

root@ubuntu-c-32-64gib-sfo2-01:~/hashclash/doors# cat file2.txt.coll | base64 --wrap=0
AJclpvsXKBrTUmLLx1XXzYblX9CDAZtNVQZhq4gRivpNNLN1WUZWl+9sSgeQzP4Z189vkgAAAACu5SNcWp0NRyuFVqJ+/Wv3Icp+sViaoSk5sDHeoJ7pdwFQKAyoxlRj17aDLUQdmRpuOPIXGZPEFE9Pt7UBVdD5qQOm/OMxCJH6SXdU5wUGU6LwWNe3+BuV07DNa9X3rlB60gWRlFnQqSzEvvfLpWUSiL7QXoLf1CBP6LwHNdW2gWRSdG5802D7S00Gzig+MwyLLJLJCc7rPYgEISekGjsk00M5SGFho05Sf9ufwBiCIT0r8Re12gHCRbnhmmmueTWWSLyX6+TpQxUd+b29mKPc62RoloV5EDagO+iSfuvtML3pPKUyWNIk2e79sn7D8xU6aOwXo17qUjFF0GkkR3kFg8WEdP9lWUrnK02nwn9ygpbfNJUvEXoZ/iaHmyaZMz42h70mg1UQbTBBNR+6sgfsNplzzFrkOHwna5ybyAPHlIsB2P/XcgzR50EUFlLXi8QZkHvkZY4/yTuM6SujWmdl4PukRWoLKzNAvdQ5EzDrARXd1UrdP5/AVUPebRYA3aLXB4oRDf12ugwayKapfgzjDz0gjheqdOk306c1C1W4vdW0RgLm7L87SifAR2gzbMV2jex6NvnFACrgRF2OrSQTUhkTP1SMwEzP0gI5j5wingNDw0clCn0shaItsnqrwmMP+fUCGjU5F7W+y3LwQ6VLTBPS+sVegjGMD+sJPAZ9eAW2n7yS6Grw9/6D2GswDSgDe42BgPRXhv+Odsrnd7s3bvEPHfATAkl5aCgtFhBq3nmOg0kq3+bDW0F0NwHEAx/FCfx0CGX73IwzhMH11v/Mk7+8GGD5NJNhcvrG12rSrSAoSD0pAGW7kOOeyVmpm8URLKMUPU4EoUxKARkH7O/oP1qobvlbkeOiz/Ldgp3gv4OC/7qwtPsnFsBzaUZj5arm5mNrB4/+kWaA1l6OWtu9LBQV3jHQICfgGkcYojjskBKuQfhKV499
```

For comparison, the 8 vcpu run on my Ryzen 2700X finally finished after about 8 hours. It probably would have taken a matter of minutes on a good GPU.

## Solution

We have a pair of files now with different prefixes but the same MD5 hash, and we know how to use that to get past the gatekeeper. Pass in file2, then file1:

```python
#!/usr/bin/env python3
from pwn import *

# base64 encoded file1.txt.coll
file1="c3AzYWtmcjFlbmQ0bmQzbnQzcgA9YoQRAXXTTeuAk94xwdkwRfu+HnHwCmN1qDCqmBfK4wAAAAAL5sFBbqmL2SuFVqJ+/Wv3Icp+sViaoSk5sDHeoJ7pdwFQKAyoxlRj17aDLUQdmRpuOPIXGZPEDE9Pt7UBVdD5qQOm/OMxCJH6SXdU5wUGU6LwWNe3+BuV07DNa9X3rlB60gWRlFnQqSzEvvfLpWUSiL7QXoLn1CBP6LwHNdW2gWRSdG5802D7S00Gzig+MwyLLJLJCc7rPYgEISekGjsk00M5SGFho05Sf9ufwBiCIT0r8Re1mgHCRbnhmmmueTWWSLyX6+TpQxUd+b29mKPc62RoloV5EDagO+iSfuvtML3pPKUyWNIk2e79sn7D8xU6aOwXo57qUjFF0GkkR3kFg8WEdP9lWUrnK02nwn9ygpbfNJUvEXoZ/iaHmyaZMz42h70mg1UQbTBBNR+6sgfsNplzzHrkOHwna5ybyAPHlIsB2P/XcgzR50EUFlLXi8QZkHvkZY4/yTuM6SujWmdl4PukRWoLKzNAvdQ5EzDrARXd1UrdR5/AVUPebRYA3aLXB4oRDf12ugwayKapfgzjDz0gjheqdOk306c1C1W4vdW0RgLm7L87SifAR2gzbMV2jex6NvjFACrgRF2OrSQTUhkTP1SMwEzP0gI5j5wingNDw0clCn0shaItsnqrwmMP+fUCGjU5F7W+y3LwQ6VLTBPS+sVehDGMD+sJPAZ9eAW2n7yS6Grw9/6D2GswDSgDe42BgPRXhv+Odsrnd7s3bvEPHfATAkl5aCgtFhBq3nmOg0kq32bDW0F0NwHEAx/FCfx0CGX73IwzhMH11v/Mk7+8GGD5NJNhcvrG12rSrSAoSD0pAGW7kOOeyVmpm8URLKMUPU78oExKARkH7O/oP1qobvlbkeOiz/Ldgp3gv4OC/7qwtPsnFsBzaUZj5arm5mNrB4/+kWaA1l6OWtu9LBQV3i3QICfgGkcYojjskBKuQfhKV499"

# base64 encoded file2.txt.coll
file2="AJclpvsXKBrTUmLLx1XXzYblX9CDAZtNVQZhq4gRivpNNLN1WUZWl+9sSgeQzP4Z189vkgAAAACu5SNcWp0NRyuFVqJ+/Wv3Icp+sViaoSk5sDHeoJ7pdwFQKAyoxlRj17aDLUQdmRpuOPIXGZPEFE9Pt7UBVdD5qQOm/OMxCJH6SXdU5wUGU6LwWNe3+BuV07DNa9X3rlB60gWRlFnQqSzEvvfLpWUSiL7QXoLf1CBP6LwHNdW2gWRSdG5802D7S00Gzig+MwyLLJLJCc7rPYgEISekGjsk00M5SGFho05Sf9ufwBiCIT0r8Re12gHCRbnhmmmueTWWSLyX6+TpQxUd+b29mKPc62RoloV5EDagO+iSfuvtML3pPKUyWNIk2e79sn7D8xU6aOwXo17qUjFF0GkkR3kFg8WEdP9lWUrnK02nwn9ygpbfNJUvEXoZ/iaHmyaZMz42h70mg1UQbTBBNR+6sgfsNplzzFrkOHwna5ybyAPHlIsB2P/XcgzR50EUFlLXi8QZkHvkZY4/yTuM6SujWmdl4PukRWoLKzNAvdQ5EzDrARXd1UrdP5/AVUPebRYA3aLXB4oRDf12ugwayKapfgzjDz0gjheqdOk306c1C1W4vdW0RgLm7L87SifAR2gzbMV2jex6NvnFACrgRF2OrSQTUhkTP1SMwEzP0gI5j5wingNDw0clCn0shaItsnqrwmMP+fUCGjU5F7W+y3LwQ6VLTBPS+sVegjGMD+sJPAZ9eAW2n7yS6Grw9/6D2GswDSgDe42BgPRXhv+Odsrnd7s3bvEPHfATAkl5aCgtFhBq3nmOg0kq3+bDW0F0NwHEAx/FCfx0CGX73IwzhMH11v/Mk7+8GGD5NJNhcvrG12rSrSAoSD0pAGW7kOOeyVmpm8URLKMUPU4EoUxKARkH7O/oP1qobvlbkeOiz/Ldgp3gv4OC/7qwtPsnFsBzaUZj5arm5mNrB4/+kWaA1l6OWtu9LBQV3jHQICfgGkcYojjskBKuQfhKV499"

context.log_level='DEBUG'
p = process(['ncat','--ssl','7b00000094b6a46399d93bdb.challenges.broker4.allesctf.net','1337'])

# Our local copy of gatekeeper.py prompts for "Give me your input:"
# But the remote service instead prompts for "Speak friend and enter: "
p.recvuntil('Speak friend and enter: ')
p.sendline(file2)
p.recvuntil('Speak friend and enter: ')
p.sendline(file1)
p.recvall()
```

Run it and we get our flag:

```
[+] Starting local process '/usr/bin/ncat' argv=[b'ncat', b'--ssl', b'7b00000094b6a46399d93bdb.challenges.broker4.allesctf.net', b'1337'] : pid 15477
[DEBUG] Received 0x1fd bytes:
    b'Welcome to the "Doors of Durin"\n'
    b"I'm the gatekeeper of this ancient place\n"
    b"A long time ago those doors weren't in need of a gatekeeper. But in recent time, especially after the big success of J.R.R. Tolkien, everyone knows the secret words. The passphrase to open the door to the precious flag!\n"
    b'The flag had a lot of visitors and wants to be kept alone. So its my job to keep anyone out\n'
    b'Only real skilled hackers are allowed here. Once you have proven yourself worthy, the flag is yours\n'
    b'Speak friend and enter: '
[DEBUG] Sent 0x401 bytes:
    b'AJclpvsXKBrTUmLLx1XXzYblX9CDAZtNVQZhq4gRivpNNLN1WUZWl+9sSgeQzP4Z189vkgAAAACu5SNcWp0NRyuFVqJ+/Wv3Icp+sViaoSk5sDHeoJ7pdwFQKAyoxlRj17aDLUQdmRpuOPIXGZPEFE9Pt7UBVdD5qQOm/OMxCJH6SXdU5wUGU6LwWNe3+BuV07DNa9X3rlB60gWRlFnQqSzEvvfLpWUSiL7QXoLf1CBP6LwHNdW2gWRSdG5802D7S00Gzig+MwyLLJLJCc7rPYgEISekGjsk00M5SGFho05Sf9ufwBiCIT0r8Re12gHCRbnhmmmueTWWSLyX6+TpQxUd+b29mKPc62RoloV5EDagO+iSfuvtML3pPKUyWNIk2e79sn7D8xU6aOwXo17qUjFF0GkkR3kFg8WEdP9lWUrnK02nwn9ygpbfNJUvEXoZ/iaHmyaZMz42h70mg1UQbTBBNR+6sgfsNplzzFrkOHwna5ybyAPHlIsB2P/XcgzR50EUFlLXi8QZkHvkZY4/yTuM6SujWmdl4PukRWoLKzNAvdQ5EzDrARXd1UrdP5/AVUPebRYA3aLXB4oRDf12ugwayKapfgzjDz0gjheqdOk306c1C1W4vdW0RgLm7L87SifAR2gzbMV2jex6NvnFACrgRF2OrSQTUhkTP1SMwEzP0gI5j5wingNDw0clCn0shaItsnqrwmMP+fUCGjU5F7W+y3LwQ6VLTBPS+sVegjGMD+sJPAZ9eAW2n7yS6Grw9/6D2GswDSgDe42BgPRXhv+Odsrnd7s3bvEPHfATAkl5aCgtFhBq3nmOg0kq3+bDW0F0NwHEAx/FCfx0CGX73IwzhMH11v/Mk7+8GGD5NJNhcvrG12rSrSAoSD0pAGW7kOOeyVmpm8URLKMUPU4EoUxKARkH7O/oP1qobvlbkeOiz/Ldgp3gv4OC/7qwtPsnFsBzaUZj5arm5mNrB4/+kWaA1l6OWtu9LBQV3jHQICfgGkcYojjskBKuQfhKV499\n'
[DEBUG] Received 0x16 bytes:
    b'Doing magic, stand by\n'
[DEBUG] Received 0x31 bytes:
    b"b'You said: \\nNope :/\\n'\n"
    b'Speak friend and enter: '
[DEBUG] Sent 0x401 bytes:
    b'c3AzYWtmcjFlbmQ0bmQzbnQzcgA9YoQRAXXTTeuAk94xwdkwRfu+HnHwCmN1qDCqmBfK4wAAAAAL5sFBbqmL2SuFVqJ+/Wv3Icp+sViaoSk5sDHeoJ7pdwFQKAyoxlRj17aDLUQdmRpuOPIXGZPEDE9Pt7UBVdD5qQOm/OMxCJH6SXdU5wUGU6LwWNe3+BuV07DNa9X3rlB60gWRlFnQqSzEvvfLpWUSiL7QXoLn1CBP6LwHNdW2gWRSdG5802D7S00Gzig+MwyLLJLJCc7rPYgEISekGjsk00M5SGFho05Sf9ufwBiCIT0r8Re1mgHCRbnhmmmueTWWSLyX6+TpQxUd+b29mKPc62RoloV5EDagO+iSfuvtML3pPKUyWNIk2e79sn7D8xU6aOwXo57qUjFF0GkkR3kFg8WEdP9lWUrnK02nwn9ygpbfNJUvEXoZ/iaHmyaZMz42h70mg1UQbTBBNR+6sgfsNplzzHrkOHwna5ybyAPHlIsB2P/XcgzR50EUFlLXi8QZkHvkZY4/yTuM6SujWmdl4PukRWoLKzNAvdQ5EzDrARXd1UrdR5/AVUPebRYA3aLXB4oRDf12ugwayKapfgzjDz0gjheqdOk306c1C1W4vdW0RgLm7L87SifAR2gzbMV2jex6NvjFACrgRF2OrSQTUhkTP1SMwEzP0gI5j5wingNDw0clCn0shaItsnqrwmMP+fUCGjU5F7W+y3LwQ6VLTBPS+sVehDGMD+sJPAZ9eAW2n7yS6Grw9/6D2GswDSgDe42BgPRXhv+Odsrnd7s3bvEPHfATAkl5aCgtFhBq3nmOg0kq32bDW0F0NwHEAx/FCfx0CGX73IwzhMH11v/Mk7+8GGD5NJNhcvrG12rSrSAoSD0pAGW7kOOeyVmpm8URLKMUPU78oExKARkH7O/oP1qobvlbkeOiz/Ldgp3gv4OC/7qwtPsnFsBzaUZj5arm5mNrB4/+kWaA1l6OWtu9LBQV3i3QICfgGkcYojjskBKuQfhKV499\n'
[-] Receiving all data: Failed
[DEBUG] Received 0x16 bytes:
    b'Doing magic, stand by\n'
[DEBUG] Received 0x75 bytes:
    b"b'You said: sp3akfr1end4nd3nt3r\\nFlag: ALLES{st0p_us1ng_md5_alr34dy_BabyRage_1836d}\\n\\x7f\\n'\n"
    b'Speak friend and enter: '
```

The flag is:

```
ALLES{st0p_us1ng_md5_alr34dy_BabyRage_1836d}
```

## Benchmarking and Post-analysis

09/07/2020 update: After the CTF ended, I got my quota sorted out on AWS and spun up a `g4dn.xlarge` instance and tried the hashclash run again to see how it performs with a GPU:

```
ubuntu@ip-172-31-7-120:/mnt/nvme/hashclash/doors$ ../scripts/cpc.sh file1.txt file2.txt
...
Found 1 CUDA devices.
Thread 1 created (AVX256).
Thread 2 created (AVX256).
Thread 3 created (AVX256).
Thread 4 created (CUDA).
CUDA device 0: Tesla T4 (40 MPs)
Using 40 blocks with 1024 threads each: total 40960 threads.
...
```

This was a just a 4x16 VM, because I expected the GPU to do the heavy lifting. But the GPU was only used for the first stage (and it did have a significant impact there). After that, I continued monitoring the system, and the GPU was idle while the 4 vcpus were pegged at 100%. So it didn't have the impact I was hoping for. I ended up killing this experiment after letting it run for 6 hours with the GPU sitting idle. This code primarily benefits from a large number of CPU cores.

Separate from that, I came across another writeup for this challenge, and there is a MUCH cheaper algorithm I could have used:

<https://github.com/CTF-STeam/ctf-writeups/tree/master/2020/ALLES!%20CTF/Doors%20of%20Durin>

I tried that on my kali VM, and it finished in just over 4 minutes:

```
kali@kali:~/Downloads/hashclash/doors$ time ../scripts/poc_no.sh file1.txt 
...
Found collision!
b4b9786d1092cfd82494f1f3ea9bd38f  collision1.bin
b4b9786d1092cfd82494f1f3ea9bd38f  collision2.bin
a9a44bb0484cb7c3de5be3b2b8a6cd5b910ea45a  collision1.bin
bc416c48e4c074712db8a98f4e990fce19fa715f  collision2.bin
4 -rw-r--r-- 1 kali kali 128 Sep  7 10:48 collision1.bin
4 -rw-r--r-- 1 kali kali 128 Sep  7 10:48 collision2.bin

real    4m15.494s
user    17m27.514s
sys     0m18.655s
kali@kali:~/Downloads/hashclash/doors$ hexdump -C collision1.bin
00000000  73 70 33 61 6b 66 72 31  65 6e 64 34 6e 64 33 6e  |sp3akfr1end4nd3n|
00000010  74 33 72 00 09 02 dc 19  55 90 d2 df 0e 8c b6 61  |t3r.....U......a|
00000020  61 18 77 71 c1 cf eb ad  d5 b8 8c 04 d6 47 99 08  |a.wq.........G..|
00000030  fa 9b cc fd 39 ca 5d 84  af 52 d6 0c e2 c3 82 bb  |....9.]..R......|
00000040  eb 0c e3 26 bc 48 13 2b  ad ee 70 c2 cd 95 f5 79  |...&.H.+..p....y|
00000050  80 28 96 6a e1 81 39 ea  79 47 c7 6f b3 33 79 22  |.(.j..9.yG.o.3y"|
00000060  17 7c 33 5c e6 83 c1 9f  d4 55 b0 a5 34 21 a6 a3  |.|3\.....U..4!..|
00000070  3f 71 71 50 dd 43 f0 08  93 8a b3 05 9a ae b7 a8  |?qqP.C..........|
00000080
kali@kali:~/Downloads/hashclash/doors$ hexdump -C collision2.bin
00000000  73 70 33 61 6b 66 72 31  65 6f 64 34 6e 64 33 6e  |sp3akfr1eod4nd3n|
00000010  74 33 72 00 09 02 dc 19  55 90 d2 df 0e 8c b6 61  |t3r.....U......a|
00000020  61 18 77 71 c1 cf eb ad  d5 b8 8c 04 d6 47 99 08  |a.wq.........G..|
00000030  fa 9b cc fd 39 ca 5d 84  af 52 d6 0c e2 c3 82 bb  |....9.]..R......|
00000040  eb 0c e3 26 bc 48 13 2b  ad ed 70 c2 cd 95 f5 79  |...&.H.+..p....y|
00000050  80 28 96 6a e1 81 39 ea  79 47 c7 6f b3 33 79 22  |.(.j..9.yG.o.3y"|
00000060  17 7c 33 5c e6 83 c1 9f  d4 55 b0 a5 34 21 a6 a3  |.|3\.....U..4!..|
00000070  3f 71 71 50 dd 43 f0 08  93 8a b3 05 9a ae b7 a8  |?qqP.C..........|
00000080
```

I remember seeing an example for `poc_no.sh` while I was looking for options during the CTF, but it was listed as an identical-prefix collision, so I didn't expect it to work for this problem. Turns out the 9th byte is different, which makes it perfect for this challenge!

| Host         | Size  | CPU         | GPU      | OS                    | Script    | Runtime    |
| ------------ | ----- | ----------- | -------- | --------------------- | --------- | ---------- |
| VirtualBox   | 8x16  | Ryzen 2700X | None     | Kali 2020             | cpc.sh    | ~8 hours   |
| DigitalOcean | 32x64 | Xeon 6140   | None     | Ubuntu 20.04          | cpc.sh    | ~3 hours   |
| AWS          | 4x16  | Xeon 8259CL | Tesla T4 | DL AMI (Ubuntu 18.04) | cpc.sh    | >6 hours (incomplete) |
| VirtualBox   | 8x16  | Ryzen 2700X | None     | Kali 2020             | poc_no.sh | ~4 min     |

Lessons learned:

* Use `poc_no.sh` if you can! I assumed this would only generate true identical-prefix collisions.
* Throw as many CPU cores as you can afford at `cpc.sh`. A GPU is a bonus, but you still need a lot of CPU power.

