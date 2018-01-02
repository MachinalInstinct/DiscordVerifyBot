import discord
from discord.ext import commands
import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check
import cogs.basic.rcon as rcon


class RCON:
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.loop.create_task(self.my_background_task())




    async def my_background_task(self):
        await self.wait_until_ready()

        channel = self.get_channel(1234567)  # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60)  # task runs every 60 seconds


def setup(bot):
    bot.add_cog(RCON(bot))