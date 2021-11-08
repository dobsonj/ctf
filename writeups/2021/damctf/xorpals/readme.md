
# crypto/xorpals

Author: m0x

## Description

```
One of the 60-character strings in the provided file has been encrypted by single-character XOR. The challenge is to find it, as that is the flag.

Hint: Always operate on raw bytes, never on encoded strings. Flag must be submitted as UTF8 string.
```

Downloads: `flags.txt`

## Solution

There are 98 lines in flags.txt, and one of them is a flag that was xor'd with a single character. So this is just a brute-force exercise. For each line, xor it with a value between 0 and 255, until you find a string starting with `dam`:

```python3
#!/usr/bin/env python3

f = open(f"flags.txt", 'r')
lines = f.readlines()
for line in lines:
    b = bytes.fromhex(line)
    for k in range(255):
        d = bytes([b[i] ^ k for i in range(len(b))])
        if d[:3] == b'dam':
            print(d)
            break
```

```
$ ./solve.py
b'dam{antman_EXPANDS_inside_tHaNoS_never_sinGLE_cHaR_xOr_yeet}'
```

The flag is:

```
dam{antman_EXPANDS_inside_tHaNoS_never_sinGLE_cHaR_xOr_yeet}
```

