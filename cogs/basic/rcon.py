from websocket import create_connection
import json
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
name = "Peko"

rcon_file = open("rconinfo", "r")
ws_info = str(rcon_file.readline())
rcon_file.close()

def rcon(msg):
    try:
        ws = create_connection(str(ws_info))
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
        #ws.close()
        result = json.loads(raw)
        #print(type(result))
        message = result['Message']
        #print(message)
        ws.close()
        return message
    except Exception as e:
        raise e

def get_oxide_group_users(group):
    try:
        id_list = []
        raw = rcon("oxide.show group "+str(group))
        list_str = raw.splitlines()[1]
        raw_list = list_str.split(",")
        count = 0
        for entry in raw_list:
            userid1 = entry.split(' (', 1)[0]
            userid2 = userid1
            if count > 0:
                userid2 = userid1.split(' ')[1]
            id_list.append(userid2)
            count = count+1

        return id_list

    except Exception as e:
        raise e


def get_vip_steamid_list():
    try:
        vips = get_oxide_group_users("p2w")
        return vips
    except Exception as e:
        raise e

def get_steamlink_steamid_list():
    try:
        sl_list = get_oxide_group_users("steamlink")
        return sl_list
    except Exception as e:
        raise e

def add_group(steamid, group):
    try:
        rcon('oxide.usergroup add '+steamid+' '+group)
    except Exception as e:
        raise e

def get_mutelist():
    try:
        mutelist = []
        raw = rcon('mutelist')
        if raw == "There is nobody muted at the moment.":
            return mutelist
        for line in raw.splitlines():
            steam_id = line.split(',')[0]
            #print(steam_id)
            mutelist.append(steam_id)
        return mutelist
    except Exception as e:
        raise e

def get_clanslist2():
    try:
        clanlist = []
        raw = rcon('clans.listex')
        count = 0
        dic = {}
        for line in raw.splitlines():
            rawentry = line.split(' ')
            entrylist = []
            for entry in rawentry:
                if not entry is '':
                    entrylist.append(entry)


            if entrylist:
                if count > 2:
                    tag = entrylist[0]
                    steamid = entrylist[len(entrylist)-2]
                    dic[int(steamid)] = tag
                count = count+1

        return dic
    except Exception as e:
        raise e
