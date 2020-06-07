
# Teleport

## Description

```
Challenge instance ready at 88.198.219.20:54778.

One of our admins plays a strange game which can be accessed over TCP. He's been playing for a while but can't get the flag! See if you can help him out.
```

Category: Miscellaneous

## Analysis

Let's check out the code first:

```python
import math

x = 0.0
z = 0.0
flag_x = 10000000000000.0
flag_z = 10000000000000.0
print("Your player is at 0,0")
print("The flag is at 10000000000000, 10000000000000")
print("Enter your next position in the form x,y")
print("You can move a maximum of 10 metres at a time")
for _ in range(100):
    print(f"Current position: {x}, {z}")
    try:
        move = input("Enter next position(maximum distance of 10): ").split(",")
        new_x = float(move[0])
        new_z = float(move[1])
    except Exception:
        continue
    diff_x = new_x - x
    diff_z = new_z - z
    dist = math.sqrt(diff_x ** 2 + diff_z ** 2)
    if dist > 10:
        print("You moved too far")
    else:
        x = new_x
        z = new_z
    if x == 10000000000000 and z == 10000000000000:
        print("ractf{#####################}")
        break
```

The goal is to print the flag, so we need to get down to this block:

```python
    if x == 10000000000000 and z == 10000000000000:
        print("ractf{#####################}")
        break
```

But we get a max distance of 10 each move.

```bash
kali@kali:~/Downloads/ractf$ python3 teleport.py 
Your player is at 0,0
The flag is at 10000000000000, 10000000000000
Enter your next position in the form x,y
You can move a maximum of 10 metres at a time
Current position: 0.0, 0.0
Enter next position(maximum distance of 10): 10,10
You moved too far
Current position: 0.0, 0.0
Enter next position(maximum distance of 10): 4,6
Current position: 4.0, 6.0
Enter next position(maximum distance of 10): 6,4
Current position: 6.0, 4.0
Enter next position(maximum distance of 10): 10,10
Current position: 10.0, 10.0
Enter next position(maximum distance of 10): 14,16
Current position: 14.0, 16.0
Enter next position(maximum distance of 10): 20,20
Current position: 20.0, 20.0
```

This limit is a problem, because we only get 100 moves.

```python
for _ in range(100):
    print(f"Current position: {x}, {z}")
```

Look where it takes the input though:

```python
        move = input("Enter next position(maximum distance of 10): ").split(",")
        new_x = float(move[0])
        new_z = float(move[1])
```

Floats do have some weird corner cases. We need to look up the documentation for `float()` to find out what special values it accepts.

* <https://docs.python.org/3/library/functions.html#float>

What happens with `inf` and `nan`?

```
Enter next position(maximum distance of 10): inf,inf
You moved too far
Current position: 20.0, 20.0
Enter next position(maximum distance of 10): nan,nan
Current position: nan, nan
Enter next position(maximum distance of 10): 1000,1000
Current position: 1000.0, 1000.0
```

Bingo! `nan` lets us move wherever we want. Apparently anything involving `nan` is always `nan`, and comparisons to actual numbers are always `False`:

```python.console
>>> float('nan') - 1000
nan
>>> math.sqrt(float('nan') ** 2)
nan
>>> float('nan') > 10
False
>>> float('nan') < 10
False
```

## Solution

Now we just have to use this trick on the challenge server to get the flag.

```
$ nc 88.198.219.20 54778
Your player is at 0,0
The flag is at 10000000000000, 10000000000000
Enter your next position in the form x,y
You can move a maximum of 10 metres at a time
Current position: 0.0, 0.0
Enter next position(maximum distance of 10): nan,nan
Current position: nan, nan
Enter next position(maximum distance of 10): 10000000000000,10000000000000
ractf{fl0at1ng_p01nt_15_h4rd}
```

The flag is:

```
ractf{fl0at1ng_p01nt_15_h4rd}
```

