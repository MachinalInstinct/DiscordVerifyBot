from websocket import create_connection
import json
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
ws = create_connection("ws://rust.setomaa.win:28016/MinaSiin")

def test():
    d = {
        "Message": "oxide.show group p2w",

        "Identifier": 0,
        "Name": "rConBot",

        "Stacktrace": "",
    }

    json_mylist = json.dumps(d, separators=(',', ':'))
    print(json_mylist)
    ws.send(json_mylist)
    result = ws.recv()
    print(str("Received " + result).translate(non_bmp_map))
    ws.close()