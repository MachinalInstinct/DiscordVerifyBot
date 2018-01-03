import discord
from discord.ext import commands
import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check
import cogs.basic.rcon as rcon
import asyncio





class Background:
    def __init__(self, bot):
        self.bot = bot
        self.runvip = True
        self.runmember = True
        bot.bg_task = bot.loop.create_task(self.member())
        bot.bg_task = bot.loop.create_task(self.vip())


    async def vip(self):
        while True:
            guild = self.bot.get_guild(297628706875375616)
            vip_role = discord.utils.get(guild.roles, name='VIP')
            if self.runvip is True:
                viplist = rcon.get_vip_steamid_list()
                print(viplist)
                for vip in viplist:
                    print(vip)
                    user = db.get_steam_user(vip)
                    print("USER: "+str(user))
                    if user is not None:
                        discordid = user['DiscordID']
                        print(discordid)
                        member = discord.utils.get(guild.members, id=int(discordid))
                        print(member.name)
                        await member.add_roles(vip_role, reason="VIP user")




            await asyncio.sleep(300)  # task runs every 5min

    async def member(self):
        while True:
            guild = self.bot.get_guild(297628706875375616)
            member_role = discord.utils.get(guild.roles, name='Member')
            if self.runmember is True:
                discordids = db.get_linked_users()
                #print("DISCORDIDS"+discordids)
                for id in discordids:
                    member = discord.utils.get(guild.members, id=int(id))
                    await member.add_roles(member_role, reason="Linked user")

            await asyncio.sleep(300)  # task runs every 5min




def setup(bot):
    bot.add_cog(Background(bot))