
# I stumbled across this and stole it as a starting point. because lazy.
#  https://gist.github.com/ConnorNelson/07229c0a55aaf05571c26c854c300e33

import socket
import subprocess
from swpag_client import Team # pip install swpag_client
from pwn import * # pip install pwntools
import time

# attack functions for each service...

# everybodys_got_something_to_hide
def attack_svc1(flag_id):
    print("running attack on service 1, flag id:", flag_id)
    flag = ""
    return flag

# yellow_submarine
def attack_svc2(flag_id):
    print("running attack on service 2, flag id:", flag_id)
    flag = ""
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
            flag_id = target['flag_id']
            ip = socket.gethostbyname(target['hostname'])
            port = target['port']
            print("ip:", ip, ", port:", port, ", flag_id:", flag_id)
            if flag_id in service_flag_ids[service['service_name']]:
                print("Skipping... already processed this flag_id.")
                continue
            try:
                conn = remote(ip, port, timeout=30)
                flag = attack_functions[service['service_id']](flag_id)
                print("flag:", flag)
                conn.close()
                # result = team.submit_flag(flag)
                # print(result)
            except Exception as e:
                print("Error connecting to", target['team_name'], target['hostname'], ip, port)
                print(e)
            service_flag_ids[service['service_name']].add(flag_id)

    time.sleep(10) # DOS is against the rules


