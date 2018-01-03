import discord
from discord.ext import commands
import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check
import random


def authkey():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    p = "".join(random.sample(s, 5))
    return p


class Linking:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='link')
    async def cmd_link(self, ctx):
        """Link yourself."""
        try:
            user = ctx.author
            if not db.if_exists(user.id):
                print("Doesn't exist, adding..")

                same = True
                otherauthkeys = db.get_authkeys()
                print(otherauthkeys)
                #authkey = authkey()

                while same:
                    print("GETTING AUTHKEY")
                    #ak = []
                    #ak.append(authkey())
                    ak = authkey()
                    print(ak)
                    print("CHECKING AUTHKEY")
                    if not ak in otherauthkeys:
                        same = False

                print("ADDING")

                db.add_user(user, ak)

            await ctx.message.add_reaction('\N{BALLOT BOX WITH CHECK}')

            auth = db.get_authkey(user)

            print("USER:" + user.name)
            print("USER ID:" + str(user.id))
            print("AUTHKEY:" + auth)

            if db.is_verified(user):
                await user.send(embed=status.is_verified())
                return


            await user.send(embed=status.authkey(auth))

        except Exception as e:
            try:
                await ctx.channel.send(embed=status.error(e))
                print(e)
            except:
                print(e)

    @commands.command(name='info')
    @commands.guild_only()
    #@commands.check(check.check_mod)
    async def cmd_info(self, ctx, user: discord.User = None):
        """Info about linked person."""
        try:
            print(user)
            if user is None or user == ctx.author:
                user = ctx.author

            if user is not ctx.author:
                if not check.check_mod(ctx):
                    return

            if not db.if_exists(user.id):
                await ctx.author.send(embed=status.user_info(user, False))
                return

            user_db = db.get_discord_user(user.id)

            steamid = user_db['SteamID']
            if steamid is None:
                steamid = False

            authkey = user_db['AuthKey']

            verified = user_db['Verified']

            await ctx.author.send(embed=status.user_info(user, True, steamid, authkey, verified))
            return

        except Exception as e:
            try:
                await ctx.channel.send(embed=status.error(e))
                print(e)
            except:
                print(e)


def setup(bot):
    bot.add_cog(Linking(bot))
