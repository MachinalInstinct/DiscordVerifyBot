import pymysql as mysql
#import discord

sqlinfo = []
with open("sqlinfo") as fin:
    for line in fin:
        sqlinfo.append(line.strip( '\n'))
#print(sqlinfo)

conn = mysql.connect(host=sqlinfo[0],user=sqlinfo[1],password=sqlinfo[2],db=sqlinfo[3],charset='utf8mb4',cursorclass=mysql.cursors.DictCursor)

c = conn.cursor()

### ---LINKING---

def is_verified(user):
    try:
        id = user.id

        sql = "SELECT `Verified` FROM `discord_link` where `DiscordID` = %s;"
        c.execute(sql, (str(id),))
        #cursor.execute("select name_first, name_last from address")
        selection = c.fetchall()

        for item in selection:
            selection = item

        verified = selection['Verified']

        if verified == None or verified == 0:
            return False

        if verified == 1:
            return True
    except Exception as e:
        raise e

    #sql = "SELECT {} FROM {} WHERE {}=?".format(column_to, table, column_by)
    #selection = [item[0] for item in c.execute(sql, (value_by,))]

def if_exists(userid):
    try:
        sql = "SELECT * FROM `discord_link` where `DiscordID` = %s;"
        exec = c.execute(sql,(str(userid),))
        #print(exec)

        if exec == 1:
            return True
        if exec == 0:
            return False
    except Exception as e:
        raise e

def get_discord_user(userid):
    try:
        sql = "SELECT * FROM `discord_link` where `DiscordID` = %s;"
        c.execute(sql, (str(userid),))
        selection = c.fetchall()
        for item in selection:
            selection = item
        return selection
    except Exception as e:
        print("ERROR IN GET_DISCORD_USER")
        raise e

def get_steam_user(userid):
    try:
        sql = "SELECT * FROM `discord_link` where `SteamID` = %s;"
        c.execute(sql, (str(userid),))
        selection = c.fetchall()
        for item in selection:
            selection = item
        if not selection:
            selection = None
        return selection
    except Exception as e:
        raise e

def get_linked_users():
    try:
        sql = "SELECT * FROM `discord_link`;"
        c.execute(sql)
        selection = c.fetchall()
        #print(selection)
        user_list = []
        for user in selection:
            #print(user)
            dict(user)
            #print(user)
            member = user['DiscordID']
            #print(member)
            if not user['SteamID'] is None:
                user_list.append(member)
        return user_list
    except Exception as e:
        raise e

def get_authkey(user):
    try:
        id = user.id
        sql = "SELECT `AuthKey` FROM `discord_link` where `DiscordID` = %s;"
        c.execute(sql, (str(id),))
        selection = c.fetchall()
        print(selection)
        for item in selection:
            selection = item

        authkey = selection['AuthKey']
        print(authkey)
        return authkey
    except Exception as e:
        raise e

def get_authkeys():
    try:
        sql = "SELECT `AuthKey` FROM `discord_link`;"
        c.execute(sql)
        selection = c.fetchall()
        print(selection)
        key_list = []
        for item in selection:
            dict(item)
            key_list.append(item['AuthKey'])

        return key_list
    except Exception as e:
        raise e

def add_user(user, authkey):
    try:
        id = user.id

        sql = "INSERT INTO `discord_link` (`DiscordID`, `AuthKey`, `Verified`) VALUES (%s, %s, %s);"
        c.execute(sql, (str(id),str(authkey),str(0)))
    except Exception as e:
        raise e

### ---CLAN CHAT---

def get_clanchats():
    try:
        sql = "SELECT * FROM `discord_clan`;"
        c.execute(sql)
        selection = c.fetchall()
        #print(selection)
        return selection
    except Exception as e:
        raise e

def add_clan(tag, vc_id, member_list):
    try:
        sql = "INSERT INTO `discord_clan` (`Tag`, `VoiceChannelID`, `MembersIDList`) VALUES (%s, %s, %s);"
        c.execute(sql, (str(tag),str(vc_id),str(member_list)))
    except Exception as e:
        raise e

def delete_clan(tag):
    try:
        sql = "DELETE FROM `discord_clan` WHERE `Tag` = %s;"
        c.execute(sql, (str(tag),))
    except Exception as e:
        raise e

def update_clan_members(newmembers, tag):
    try:
        sql = "UPDATE `discord_clan` SET `MembersIDList` = %s WHERE `discord_clan`.`Tag` = %s;"
        c.execute(sql, (str(newmembers),str(tag)))
    except Exception as e:
        raise e