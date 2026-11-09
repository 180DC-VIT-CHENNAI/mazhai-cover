import os, resource, socket
assert os.getuid() == 65534
assert resource.getrlimit(resource.RLIMIT_CPU)[0] == 8
try:
    socket.socket()
except OSError:
    pass
else:
    raise AssertionError("network socket was allowed")
try:
    open("/tmp/doomforge-test-write", "w").close()
except OSError:
    pass
else:
    raise AssertionError("filesystem write was allowed")
print("CONTAINER_DIAGNOSTIC_OK")
