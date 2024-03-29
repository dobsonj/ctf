# CTF

Write-ups for various capture the flag events. These challenges are a great way to learn about reverse engineering, cryptography, vulnerability discovery, and exploit development. Most of the CTF events I join are with [burner_herz0g](https://ctftime.org/team/63292) and I typically focus on binary challenges (RE / pwn).

## Reverse Engineering

* [writeups/2020/dawgctf/Put_your_thang_down](writeups/2020/dawgctf/Put_your_thang_down/) (ghidra, c)
* [writeups/2020/wpictf/danger-Live-and-Malicious-Code](writeups/2020/wpictf/danger-Live-and-Malicious-Code/) (malware, js)
* [writeups/2020/wpictf/NotWannasigh](writeups/2020/wpictf/NotWannasigh/) (malware, ghidra, xor, tcpdump, c)
* [writeups/2020/sharkyctf/simple](writeups/2020/sharkyctf/simple/) (asm, xor, python)
* [writeups/2020/sharkyctf/secure_db](writeups/2020/sharkyctf/secure_db/) (ghidra, angr.io, password, sqlite)
* [writeups/2020/castorsctf/ransom](writeups/2020/castorsctf/ransom/) (malware, ghidra, xor, wireshark, gdb, flask)
* [writeups/2020/ractf/snakes_and_ladders](writeups/2020/ractf/snakes_and_ladders/) (python, rot, xor)
* [writeups/2020/rgbctf/too_slow](writeups/2020/rgbctf/too_slow/) (binary patching, xor, ghidra, c, asm, pwntools)
* [writeups/2020/rgbctf/advanced_reversing_mechanics_1](writeups/2020/rgbctf/advanced_reversing_mechanics_1/) (arm, ghidra, c, python)
* [writeups/2020/rgbctf/advanced_reversing_mechanics_2](writeups/2020/rgbctf/advanced_reversing_mechanics_2/) (arm, ghidra, c)
* [writeups/2020/csictf/ricknmorty](writeups/2020/csictf/ricknmorty/) (ghidra, c, pwntools)
* [writeups/2020/csictf/vietnam](writeups/2020/csictf/vietnam/) (ghidra, c, perl, gdb)
* [writeups/2020/csaw/not_malware](writeups/2020/csaw/not_malware/) (malware, ghidra, c, gdb, angr, pwntools, binary patching, strace)
* [writeups/2021/nahamconctf/banking_on_it](writeups/2021/nahamconctf/banking_on_it/) (priv esc, c, python, pexpect)
* [writeups/2021/angstromctf/free_flags](writeups/2021/angstromctf/free_flags/) (ghidra, c, python)
* [writeups/2021/b01lersctf/weenie_hut_general](writeups/2021/b01lersctf/weenie_hut_general/) (ghidra, c, xor, rand)
* [writeups/2021/b01lersctf/swirler](writeups/2021/b01lersctf/swirler/) (js, image, qr)
* [writeups/2021/damctf/seed](writeups/2021/damctf/seed/) (seed, hash, time, python)
* [writeups/2021/damctf/sneaky](writeups/2021/damctf/sneaky/) (malware, bash, python, wireshark)
* [writeups/2021/damctf/danceparty](writeups/2021/damctf/danceparty/) (malware, windows, ghidra, base64, xor)

## Pwnables

* [writeups/2020/castorsctf/abcbof](writeups/2020/castorsctf/abcbof/) (buffer overflow, gdb, pwntools)
* [writeups/2020/castorsctf/babybof1](writeups/2020/castorsctf/babybof1/) (buffer overflow, gdb, pwntools)
* [writeups/2020/castorsctf/babybof2](writeups/2020/castorsctf/babybof2/) (buffer overflow, gdb, pwntools)
* [writeups/2020/ractf/finches_in_a_stack](writeups/2020/ractf/finches_in_a_stack/) (buffer overflow, format string, canary, gdb, pwntools)
* [writeups/2020/ractf/finches_in_a_pie](writeups/2020/ractf/finches_in_a_pie/) (buffer overflow, format string, canary, pie, gdb, pwntools)
* [writeups/2020/csictf/pwn_intended](writeups/2020/csictf/pwn_intended/) (buffer overflow, gdb, perl)
* [writeups/2020/csictf/secret_society](writeups/2020/csictf/secret_society/) (buffer overflow, null terminator)
* [writeups/2020/csictf/global_warming](writeups/2020/csictf/global_warming/) (format string, gdb, perl)
* [writeups/2021/angstromctf/secure_login](writeups/2021/angstromctf/secure_login/) (urandom, strcmp, c)
* [writeups/2021/angstromctf/tranquil](writeups/2021/angstromctf/tranquil/) (buffer overflow, c, perl)
* [writeups/2021/angstromctf/sanity_checks](writeups/2021/angstromctf/sanity_checks/) (buffer overflow, c, perl)
* [writeups/2021/angstromctf/stickystacks](writeups/2021/angstromctf/stickystacks/) (format string, c, perl)
* [writeups/2021/angstromctf/raiid_shadow_legends](writeups/2021/angstromctf/raiid_shadow_legends/) (c++, stack garbage, pwntools)
* [writeups/2022/cyberedu/baby-rop](writeups/2022/cyberedu/baby-rop) (rop, gdb, pwntools, libc)

## Web

* [writeups/2020/bsidessf/simple_todos](writeups/2020/bsidessf/simple_todos) (mongodb, meteor, websocket, burpsuite)
* [writeups/2020/castorsctf/quiz](writeups/2020/castorsctf/quiz/) (dirb, golang, curl)
* [writeups/2021/angstromctf/sea_of_quills](writeups/2021/angstromctf/sea_of_quills/) (ruby, sqli)
* [writeups/2021/b01lersctf/lorem_ipsum](writeups/2021/b01lersctf/lorem_ipsum/) (lfi, flask, python)

## Crypto

* [writeups/2020/rgbctf/occasionally_tested_protocol](writeups/2020/rgbctf/occasionally_tested_protocol/) (xor, rand, time, python, pwntools)
* [writeups/2020/allesctf/aaslr1](writeups/2020/allesctf/aaslr1/) (ghidra, time, rand, python, pwntools)
* [writeups/2020/allesctf/doors_of_durin](writeups/2020/allesctf/doors_of_durin/) (hash collision, md5, hashclash, strcmp, python, c, pwntools)
* [writeups/2021/damctf/xorpals](writeups/2021/damctf/xorpals/) (xor, python, bruteforce)

## Miscellaneous

* [writeups/2020/ractf/teleport](writeups/2020/ractf/teleport/) (python, float)
* [writeups/2020/csictf/friends](writeups/2020/csictf/friends/) (python, float, sed, parsing)
* [writeups/2020/allesctf/shebang](writeups/2020/allesctf/shebang/) (bash, fd)

## Forensics

* [writeups/2020/ractf/cut_short](writeups/2020/ractf/cut_short/) (pngcheck, dd, hexdump, pcrt)

