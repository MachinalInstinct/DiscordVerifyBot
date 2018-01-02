import discord
from discord.ext import commands
import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check


class Linking:
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Linking(bot))