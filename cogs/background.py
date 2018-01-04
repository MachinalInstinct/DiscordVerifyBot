import discord
from discord.ext import commands
import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check
import cogs.basic.rcon as rcon
import asyncio
import steam

steamapi_file = open("steamapi", "r")
steamapi_key = str(steamapi_file.readline())
steamapi_file.close()

api = steam.WebAPI(key=steamapi_key)


class Background:
    def __init__(self, bot):
        self.bot = bot
        self.runvip = True
        self.runmember = True
        self.runnickname = True
        self.oxidegroupdiscord = True
        self.guild = self.bot.get_guild(297628706875375616)
        bot.bg_task = bot.loop.create_task(self.member())
        bot.bg_task = bot.loop.create_task(self.nickname())
        bot.bg_task = bot.loop.create_task(self.vip())
        bot.bg_task = bot.loop.create_task(self.oxide_group_discord())


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
                            print(member.name+" is a VIP")
                            if vip_role not in member.roles:
                                print(member.name + " added to VIP")
                                await member.add_roles(vip_role, reason="VIP user.")

                        if str(user['SteamID']) not in vip_list_steam:
                            member = discord.utils.get(self.guild.members, id=int(discord_user))
                            print(member.name + " is not VIP")
                            if vip_role in member.roles:
                                print(member.name + " removed from VIP")
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
                        display_name = api.call('ISteamUser.GetPlayerSummaries', steamids=user)['response']['players'][0]['personaname']
                        member = discord.utils.get(self.guild.members, id=int(discord_id))
                        try:
                            print("NICKNAMECHECK FOR "+member.name)
                            if not member.display_name == display_name:
                                print("CHANGING NICKNAME FOR "+member.name)
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
                discord_ids = db.get_linked_users()
                try:
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







def setup(bot):
    bot.add_cog(Background(bot))