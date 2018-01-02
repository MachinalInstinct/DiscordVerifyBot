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
        bot.bg_task = bot.loop.create_task(self.vip())

    async def vip(self):
        while True:
            #print(self.runvip)
            print(rcon.get_vip_steamid_list())
            await asyncio.sleep(300)  # task runs every 5min




def setup(bot):
    bot.add_cog(Background(bot))