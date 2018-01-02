import pymysql as mysql
#import discord

conn = mysql.connect(host='setomaa.win',
                             user='DiscordBot',
                             password='91Qs5iU1GQK718aR',
                             db='DiscordBot',
                             charset='utf8mb4',
                             cursorclass=mysql.cursors.DictCursor)

c = conn.cursor()

def is_verified(user):
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

    #sql = "SELECT {} FROM {} WHERE {}=?".format(column_to, table, column_by)
    #selection = [item[0] for item in c.execute(sql, (value_by,))]

def if_exists(user):
    id = user.id
    sql = "SELECT * FROM `discord_link` where `DiscordID` = %s;"
    exec = c.execute(sql,(str(id),))
    print(exec)

    if exec == 1:
        return True
    if exec == 0:
        return False

def get_user(user):
    id = user.id
    sql = "SELECT * FROM `discord_link` where `DiscordID` = %s;"
    c.execute(sql, (str(id),))
    selection = c.fetchall()
    for item in selection:
        selection = item
    return selection

def get_authkey(user):
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

def get_authkeys():
    sql = "SELECT `AuthKey` FROM `discord_link`;"
    c.execute(sql)
    selection = c.fetchall()
    print(selection)
    key_list = []
    for item in selection:
        dict(item)
        key_list.append(item['AuthKey'])

    return key_list

def add_user(user, authkey):
    id = user.id

    sql = "INSERT INTO `discord_link` (`DiscordID`, `AuthKey`, `Verified`) VALUES (%s, %s, %s);"
    c.execute(sql, (str(id),str(authkey),str(0)))


