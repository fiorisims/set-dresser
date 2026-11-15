# send_to_maya.py — run with your normal python3, outside Maya.
#
#   python3 send_to_maya.py "cmds.polySphere(n='from_outside')"
#
# Maya must be open with its command port on 7001:
#   cmds.commandPort(name=":7001", sourceType="python")

import socket
import sys

code = sys.argv[1]

s = socket.create_connection(("127.0.0.1", 7001), timeout=10)
s.sendall(code.encode("utf-8") + b"\n")
reply = s.recv(65536).decode("utf-8", "replace").replace("\x00", "").strip()
s.close()

print(reply or "(Maya did it, and said nothing back)")
