import discord
from discord.ext import commands
import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check
import cogs.basic.rcon as rcon
import asyncio
import steam
import sys
from collections import Counter
import ast

steamapi_file = open("steamapi", "r")
steamapi_key = str(steamapi_file.readline())
steamapi_file.close()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

api = steam.WebAPI(key=steamapi_key)

filth = [".com", ".lt", ".net", ".org", ".gg", "csgogem", "csgolottery", "hellcase"]

def fixname(name):
    new_name = ''
    count = 1
    for namepart in name.split(' '):
        if any(x in namepart.lower() for x in filth):
            print("fuck this shit lol")
            if count == len(name.split(' ')):
                new_name = new_name.rstrip(' ')
        else:
            if count == len(name.split(' ')):
                new_name = new_name+namepart
            else:
                new_name = new_name+namepart + ' '
        count = count+1
    return new_name

class Background:
    def __init__(self, bot):
        self.bot = bot
        self.runvip = True
        self.runmember = True
        self.runnickname = True
        self.oxidegroupdiscord = True
        self.mutelist = True
        self.clanchat = True
        self.guild = self.bot.get_guild(297628706875375616)
        bot.bg_task = bot.loop.create_task(self.member())
        bot.bg_task = bot.loop.create_task(self.vip())
        bot.bg_task = bot.loop.create_task(self.nickname())
        bot.bg_task = bot.loop.create_task(self.oxide_group_discord())
        bot.bg_task = bot.loop.create_task(self.mute())
        bot.bg_task = bot.loop.create_task(self.clan_chat())


    async def vip(self):
        while True:
            vip_role = discord.utils.get(self.guild.roles, name='VIP')
            if self.runvip is True:
                discord_ids = db.get_linked_users()
                vip_list_steam = rcon.get_vip_steamid_list()
                for discord_user in discord_ids:
                    user = db.get_discord_user(discord_user)
                    try:
                        if str(user['SteamID']) in vip_list_steam:
                            member = discord.utils.get(self.guild.members, id=int(discord_user))
                            if member is None:
                                continue
                            print(str(member.name).translate(non_bmp_map)+" is a VIP")
                            if vip_role not in member.roles:
                                print(str(member.name).translate(non_bmp_map)+ " added to VIP")
                                await member.add_roles(vip_role, reason="VIP user.")

                        if str(user['SteamID']) not in vip_list_steam:
                            member = discord.utils.get(self.guild.members, id=int(discord_user))
                            if member is None:
                                continue
                            print(str(member.name).translate(non_bmp_map) + " is not VIP")
                            if vip_role in member.roles:
                                print(str(member.name).translate(non_bmp_map) + " removed from VIP")
                                await member.remove_roles(vip_role, reason="Not a VIP anymore.")
                    except Exception as e:
                        print(e)

            await asyncio.sleep(300)  # task runs every 5min

    async def member(self):
        while True:
            member_role = discord.utils.get(self.guild.roles, name='Verified')
            if self.runmember is True:
                discord_ids = db.get_linked_users()
                try:
                    for id in discord_ids:
                        member = discord.utils.get(self.guild.members, id=int(id))
                        if member is None:
                            continue
                        await member.add_roles(member_role, reason="Linked user.")
                except Exception as e:
                    print(e)

            await asyncio.sleep(300)  # task runs every 5min

    async def nickname(self):
        while True:
            if self.runnickname is True:
                discord_ids = db.get_linked_users()
                try:
                    for discord_id in discord_ids:
                        user = steam.SteamID(int(db.get_discord_user(discord_id)['SteamID']))
                        display_name = fixname(api.call('ISteamUser.GetPlayerSummaries', steamids=user)['response']['players'][0]['personaname'])
                        member = discord.utils.get(self.guild.members, id=int(discord_id))
                        try:
                            if member is None:
                                continue
                            print("NICKNAMECHECK FOR "+str(member.name).translate(non_bmp_map))
                            if not member.display_name == display_name:
                                print("CHANGING NICKNAME FOR "+str(member.name).translate(non_bmp_map))
                                await member.edit(nick=display_name, reason="Synced nickname with Steam displayname.")
                        except discord.Forbidden as e:
                            print(e)
                            pass
                except Exception as e:
                    print(e)

            await asyncio.sleep(600)  # task runs every 10min

    async def oxide_group_discord(self):
        while True:
            if self.oxidegroupdiscord is True:
                try:
                    discord_ids = db.get_linked_users()
                    sl_list = rcon.get_steamlink_steamid_list()
                    print(sl_list)
                    for discord_id in discord_ids:
                        print(discord_id)
                        steamID = db.get_discord_user(str(discord_id))['SteamID']
                        print("STEAMLINK: " + str(steamID))
                        if not str(steamID) in sl_list:
                            print("ADDING TO STEAMLINK GROUP: "+str(steamID))
                            rcon.add_group(str(steamID), 'steamlink')

                except Exception as e:
                    print(e)

            await asyncio.sleep(300)  # task runs every 5min

    async def mute(self):
        while True:
            muted_role = discord.utils.get(self.guild.roles, name='Muted')
            if self.mutelist is True:
                try:
                    steam_muted_ids = rcon.get_mutelist()
                    discord_linked_ids = db.get_linked_users()
                    discord_muted_ids = []

                    for steam_id in steam_muted_ids:
                        discord_id = db.get_steam_user(steam_id)['DiscordID']
                        discord_muted_ids.append(discord_id)

                    for discord_id in discord_linked_ids:
                        member = discord.utils.get(self.guild.members, id=int(discord_id))
                        if member is None:
                            continue

                        if muted_role in member.roles:
                            if not discord_id in discord_muted_ids:
                                await member.remove_roles(muted_role, reason="User has been unmuted.")
                                return

                        if discord_id in discord_muted_ids:
                            await member.add_roles(muted_role, reason="User has been muted.")

                except Exception as e:
                    print(e)

            await asyncio.sleep(300)  # task runs every 5min

    async def clan_chat(self):
        while True:
            if self.clanchat is True:
                try:

                    category = discord.utils.get(self.guild.categories, id=396774544658137088)

                    linked_list = db.get_linked_users()
                    clans_list = rcon.get_clanslist2()
                    clan_chats = db.get_clanchats()
                    print(clan_chats)

                    taglist = []
                    clandic = {}
                    for discord_id in linked_list:
                        user = db.get_discord_user(discord_id)
                        member = discord.utils.get(self.guild.members, id=int(discord_id))

                        if int(user['SteamID']) in clans_list:
                            tag = clans_list[int(user['SteamID'])]
                            print(member.name+" is in clan with the tag of "+tag)

                            if tag in taglist:
                                taglist.append(tag)

                                clandic[tag] = list(clandic[tag]) + [int(user['SteamID'])]

                            if not tag in taglist:
                                clandic[tag] = [int(user['SteamID'])]
                                taglist.append(tag)

                    print(clandic)

                    print("Counter")

                    tagcount = Counter(taglist)

                    adminoverwrites = {}
                    adminroles = ["Consul", "Community Manager", "Moderator", "Chat Mod"]
                    for role in adminroles:
                        role = discord.utils.get(self.guild.roles, name=role)
                        adminoverwrites[role] = discord.PermissionOverwrite(connect=True, read_messages=True)
                        adminoverwrites[self.guild.default_role] = discord.PermissionOverwrite(connect=False, read_messages=False)

                    print("Delete")
                    # Delete
                    for clan in clan_chats:
                        if not clan['Tag'] in taglist:
                            db.delete_clan(clan['Tag'])
                            voice_channel = discord.utils.get(self.guild.channels, id=int(clan['VoiceChannelID']))
                            if not voice_channel is None:
                                await voice_channel.delete(reason="Clan no longer exists or is renamed.")

                    print("For Clan In Tagcount")

                    for clan in tagcount:
                        exists = False
                        member_list = []
                        dic = {}
                        old_clan_members = []
                        if tagcount[clan] > 1:

                            if any(clan in x['Tag'] for x in clan_chats):
                                print("EXISTS")
                                exists = True

                            for steam_id in list(clandic[clan]):
                                discord_id = int(db.get_steam_user(steam_id)['DiscordID'])
                                member = discord.utils.get(self.guild.members, id=discord_id)
                                if member is None:
                                    continue
                                member_list.append(discord_id)

                                dic = {**dic, member: discord.PermissionOverwrite(connect=True, read_messages=True)}
                                #print(member)


                            print("If Exists")

                            if exists:
                                claninfo = {}

                                for clans_db in clan_chats:
                                    if clans_db['Tag'] == clan:
                                        claninfo = clans_db
                                        print(claninfo)


                                db_members = ast.literal_eval(claninfo['MembersIDList'])
                                print(set(db_members))
                                print(set(member_list))
                                # Same
                                if set(member_list) == set(db_members):
                                    print("Same")
                                    continue

                                print("Updated")
                                #Updated
                                if not set(member_list) == set(db_members):
                                    print("OVERWRITES")
                                    overwrites = {**dic, **adminoverwrites, self.guild.me: discord.PermissionOverwrite(connect=True, read_messages=True)}
                                    print("VC")
                                    voice_channel = discord.utils.get(self.guild.channels, id=int(claninfo['VoiceChannelID']))
                                    print("if not voice_channel is None")
                                    if not voice_channel is None:
                                        print("IF NOT VOICE CHANNEL IS NONE")

                                        old = set(db_members)
                                        new = set(member_list)

                                        left = old.difference(new)
                                        joined = new.difference(old)
                                        print(left)
                                        print(joined)
                                        for member_id in joined:
                                            overwrite2 = discord.PermissionOverwrite()
                                            overwrite2.connect = True
                                            overwrite2.read_messages = True
                                            member = discord.utils.get(self.guild.members, id=int(member_id))
                                            await voice_channel.set_permissions(member,overwrite=overwrite2, reason="Joined Clan")

                                        for member_id in left:
                                            member = discord.utils.get(self.guild.members, id=int(member_id))
                                            await voice_channel.set_permissions(member,overwrite=None, reason="Left clan")
                                        db.update_clan_members(member_list,clan)

                            print("if not exists")
                            #New
                            if not exists:
                                overwrites = {**dic, **adminoverwrites, self.guild.me:discord.PermissionOverwrite(connect=True, read_messages=True)}
                                print(overwrites)
                                voice_channel = await self.guild.create_voice_channel(str(clan), overwrites=overwrites, category=category, reason="Clanchat")
                                db.add_clan(clan, voice_channel.id, member_list)



                except Exception as e:
                    print(e)

            await asyncio.sleep(600)  # task runs every 10min

def setup(bot):
    bot.add_cog(Background(bot))