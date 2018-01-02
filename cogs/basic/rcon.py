from websocket import create_connection
import json
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
ws = create_connection("ws://rust.setomaa.win:28016/MinaSiin")
name = "Peko"


def rcon(msg):
    try:
        d = {
            "Message": str(msg),
            "Identifier": 0,
            "Name": name,
            "Stacktrace": "",
        }
        json_info = json.dumps(d, separators=(',', ':'))
        #print(json_info)
        ws.send(json_info)
        raw = ws.recv()
        #print(raw)
        ws.close()
        result = json.loads(raw)
        #print(type(result))
        message = result['Message']
        return message
    except Exception as e:
        raise e

def get_oxide_group_users(group):
    try:
        id_list = []
        raw = rcon("oxide.show group "+str(group))
        list_str = raw.splitlines()[1]
        raw_list = list_str.split(",")
        for entry in raw_list:
            id_list.append(entry.split(' (', 1)[0])

        return id_list

    except Exception as e:
        raise e


def get_vip_steamid_list():
    try:
        print("test")
        vips = get_oxide_group_users("p2w")

        return vips
    except Exception as e:
        raise e
