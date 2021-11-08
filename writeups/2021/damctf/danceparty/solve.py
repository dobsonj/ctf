#!/usr/bin/env python3
import base64

b64in = [
    "WEtcTxJIRFtdT1hfQk5MEhNTUkkESUVH",
    "WEtcT04dSB0ZX0RSSRJQElBZBERPXg==",
    "WEtcT0BcGRJNU0RCHFAETk8=",
    "BEdakspil0BwWPgstow7jg==",
    "TktHUU4ZGVp1TFgbT051R09HGlhTdUwaWHVOHlNQVw==",
    "XkFYHRob"
]

for entry in b64in:
    x = base64.b64decode(entry)
    d = bytes([x[i] ^ 0x2a for i in range(len(x))])
    print(d)
