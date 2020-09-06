#!/usr/bin/env python3
from pwn import *

# Generate a hash collision using chosen prefixes:
"""
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
Found collision!
[*] Step 10 completed
[*] Number of backtracks until now: 3
[*] Collision generated: file1.txt.coll file2.txt.coll
08172ba29c07c72c055d4f58c786434a  file1.txt.coll
08172ba29c07c72c055d4f58c786434a  file2.txt.coll
[*] Process completed in 214 minutes (3 backtracks).
"""

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

