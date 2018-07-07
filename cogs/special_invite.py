import discord
from discord.ext import commands
import json


def write(data):
    with open('invites', 'w') as outfile:
        json.dump(data, outfile)


def load():
    with open('invites') as json_file:
        try:
            data = json.load(json_file)
        except Exception:
            data = {}
        return data


def new(inv_data,code):
    data = load()
    a = {code:inv_data}
    data.append(a)
    write(data)


def update(code,count):
    data = load()
    new_data = {}
    for inv in data:
        dic = {}
        uses = data[inv]['uses']
        role = data[inv]['role']
        if inv == code:
            uses = count
        dic['uses'] = uses
        dic['role'] = role
        new_data[inv] = dic
        print(new_data)

    write(new_data)


async def is_owner(ctx):
    return ctx.author.id == 107541327125708800


class Invite:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        data = load()
        print(data)
        print("LOAD")
        for invite in await member.guild.invites():
            try:
                inv = data[invite.code]
                print("Code found")
                print(str(invite.uses)+' > '+str(inv['uses']))
                if invite.uses > inv['uses']:
                    role = discord.utils.get(member.guild.roles, id=int(inv['role']))
                    print(role.name)
                    update(invite.code, invite.uses)
                    await member.add_roles(role,reason="Joined by using invite link - "+invite.code)
                    return
            except Exception:
                pass

    @commands.command(name='testinv')
    @commands.guild_only()
    @commands.check(is_owner)
    async def cmd_testinv(self, ctx, code: str = None):
        data = load()
        print(data)
        print("LOAD")
        for invite in await ctx.guild.invites():
            try:
                inv = data[invite.code]
                print("Code found")
                print(str(invite.uses)+' > '+str(inv['uses']))
                if invite.uses > inv['uses']:
                    role = discord.utils.get(ctx.guild.roles, id=int(inv['role']))
                    print(role.name)
                    update(invite.code,invite.uses)
                    return
            except Exception:
                pass

    @commands.command(name='newinv')
    @commands.guild_only()
    @commands.check(is_owner)
    async def cmd_newinv(self, ctx, code: str=None, role: discord.Role = None):
        """New invite."""

        if not code:
            return
        if not role:
            return

        guild = ctx.guild
        legit = False
        uses = 0
        for invite in await guild.invites():
            if invite.code == code:
                legit = True
                uses = invite.uses
        if legit is False:
            return

        data = {}

        data['uses'] = uses
        data['role'] = role.id

        new(data, code)
        await ctx.message.add_reaction('\N{BALLOT BOX WITH CHECK}')


def setup(bot):
    bot.add_cog(Invite(bot))