#!/usr/bin/env python3
import angr, time, claripy

BINARY='./secure_db'
OUTFILE='out.db'
t=time.time()
proj = angr.Project(BINARY, auto_load_libs=False)
print(proj.arch)
print(proj.filename)
print("Entry: 0x%x" % proj.entry)

FIND=0x080488d6 # puts("The password is valid.");
AVOID=0x0804890a # puts("Wrong password sorry, exiting.");
print("Find: 0x%x" % FIND)
print("Avoid: 0x%x" % AVOID)

password = claripy.BVS('password', 8 * 16)
state = proj.factory.entry_state(args=[BINARY, OUTFILE], stdin=password)
simgr = proj.factory.simulation_manager(state)
simgr.explore(find=FIND, avoid=AVOID)

print(simgr.found[0].posix.dumps(0))
print(time.time() - t, "seconds")
