
acurless kdf
200

I've made a cool new KDF! Try it out.
I've encrypted a file with a key generated from the seed 'L1nuX>W1nd0ze'.

made by: acurless

http://us-east-1.linodeobjects.com/wpictf-challenge-files/acurless-kdf.pdf
http://us-east-1.linodeobjects.com/wpictf-challenge-files/secret_data.enc

Notes:
    I suggest you base your blowfish implementation on the pseudocode found on wikipedia.
    My implementation is in C if that helps you understand the spec.



kali@kali:~/Downloads/wipctf/acurless_kdf$ ls -l
total 136
-rw-r--r-- 1 kali kali 133116 Apr 18 18:29 acurless-kdf.pdf
-rw-r--r-- 1 kali kali     65 Apr 16 21:36 secret_data.enc
kali@kali:~/Downloads/wipctf/acurless_kdf$ cat secret_data.enc 
U2FsdGVkX19/1ffk4kdsmRWnTVnWMU2voWW0o2L/hV+X44zzMMP0f9vzR80j+Gg7
kali@kali:~/Downloads/wipctf/acurless_kdf$ file acurless-kdf.pdf 
acurless-kdf.pdf: PDF document, version 1.5


New files were uploaded after some problems.

kali@kali:~/Downloads/wipctf/acurless_kdf$ wget http://us-east-1.linodeobjects.com/wpictf-challenge-files/acurless-kdf-1.pdf
--2020-04-18 21:33:37--  http://us-east-1.linodeobjects.com/wpictf-challenge-files/acurless-kdf-1.pdf
Resolving us-east-1.linodeobjects.com (us-east-1.linodeobjects.com)... 173.255.231.96, 45.79.157.59, 96.126.106.143, ...
Connecting to us-east-1.linodeobjects.com (us-east-1.linodeobjects.com)|173.255.231.96|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 130709 (128K) [application/pdf]
Saving to: ‘acurless-kdf-1.pdf’

acurless-kdf-1.pdf       100%[==================================>] 127.65K   688KB/s    in 0.2s    

2020-04-18 21:33:37 (688 KB/s) - ‘acurless-kdf-1.pdf’ saved [130709/130709]

kali@kali:~/Downloads/wipctf/acurless_kdf$ wget http://us-east-1.linodeobjects.com/wpictf-challenge-files/secret_data-1.enc
--2020-04-18 21:33:45--  http://us-east-1.linodeobjects.com/wpictf-challenge-files/secret_data-1.enc
Resolving us-east-1.linodeobjects.com (us-east-1.linodeobjects.com)... 173.255.231.96, 45.79.157.59, 96.126.106.143, ...
Connecting to us-east-1.linodeobjects.com (us-east-1.linodeobjects.com)|173.255.231.96|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 65 [text/plain]
Saving to: ‘secret_data-1.enc’

secret_data-1.enc        100%[==================================>]      65  --.-KB/s    in 0s      

2020-04-18 21:33:45 (9.76 MB/s) - ‘secret_data-1.enc’ saved [65/65]

kali@kali:~/Downloads/wipctf/acurless_kdf$ ls
acurless-kdf-1.pdf  acurless-kdf.pdf  decrypt.c  secret_data-1.enc  secret_data.enc
kali@kali:~/Downloads/wipctf/acurless_kdf$ rm secret_data.enc acurless-kdf.pdf
kali@kali:~/Downloads/wipctf/acurless_kdf$ ls
acurless-kdf-1.pdf  decrypt.c  secret_data-1.enc

kali@kali:~/Downloads/wipctf/acurless_kdf$ ls -l
total 136
-rw-r--r-- 1 kali kali 130709 Apr 18 20:49 acurless-kdf-1.pdf
-rw-r--r-- 1 kali kali   1096 Apr 18 21:35 decrypt.c
-rw-r--r-- 1 kali kali     65 Apr 18 20:51 secret_data-1.enc
kali@kali:~/Downloads/wipctf/acurless_kdf$ cat secret_data-1.enc 
U2FsdGVkX19oo9RbInzmNYwRIqabb71fEUCeAKLFzMYANlfEvxKsOVbNVXlUYEw2



NOTE: I did not finish this challenge. Ran out of time while figuring out the implementation.
Including the partial code for future reference anyway.

