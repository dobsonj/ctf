# rgbCTF 2020
Sat, 11 July 2020, 11:00 MDT — Mon, 13 July 2020, 11:00 MDT

<https://ctf.rgbsec.xyz/>

Team: [burner_herz0g](https://ctftime.org/team/63292)

# Summary

## Reverse Engineering

* [too_slow](too_slow/)
* [advanced_reversing_mechanics_1](advanced_reversing_mechanics_1/)
* [advanced_reversing_mechanics_2](advanced_reversing_mechanics_2/)

## Cryptography

* [occasionally_tested_protocol](occasionally_tested_protocol/)

# Ranking

85 out of 923 scoring teams (>= 50 pts).

# Lessons Learned

* Using `time()` to seed your PRNG is a bad idea because it's easy to derive that seed using the current time range and some known output.
* Binary patching, FTW :)

