from random import seed, randint as w
from time import time


j = int
u = j.to_bytes
s = 73
t = 479105856333166071017569
_ = 1952540788
s = 7696249
o = 6648417
m = 29113321535923570
e = 199504783476
_ = 7827278
r = 435778514803
a = 6645876
n = 157708668092092650711139
d = 2191175
o = 2191175
m = 7956567
_ = 6648417
m = 7696249
e = 465675318387
s = 4568741745925383538
s = 2191175
a = 1936287828
g = 1953393000
e = 29545

g = b"rgbCTF{REDACTED}"


if __name__ == "__main__":
    seed(int(time()))
    print(f"Here's 10 numbers for you: ")
    for _ in range(10):
        print(w(5, 10000))

    b = bytearray([w(0, 255) for _ in range(40)])

    n = int.from_bytes(bytearray([l ^ p for l, p in zip(g, b)]), 'little')
    print("Here's another number I found: ", n)
