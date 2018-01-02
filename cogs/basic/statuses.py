import discord

def error(error):
    embed = discord.Embed(title="ERROR! An exception has occurred!", description=str(error), color=discord.Color.red())
    embed.set_footer(text="If the problem persists, contact @jensolaf#9386")
    return embed

def wrong_input(solution):
    embed = discord.Embed(title="Wrong Input", description=str(solution), color=discord.Color.red())
    embed.set_footer(text="If the problem persists, consult the manual by saying !help or contact @jensolaf#9386")
    return embed

# LINK

def authkey(key):
    embed = discord.Embed(title="Authentication Key", description="Your authentication key is `"+str(key)+"`", color=discord.Color.blue())
    embed.add_field(name="What am I supposed to do with it?", value="Go in-game and do `/link "+str(key)+"` to link your Discord and Steam account.", inline=False)
    embed.set_footer(text="This is your secret key, don't share it with anyone!")
    return embed

def is_verified():
    embed = discord.Embed(title="Already linked!", description="You've already linked your Steam and Discord account!", color=discord.Color.blue())
    return embed

def user_info(user,exists,steamid=False,authkey=False,verified=False):
    if not exists:
        embed = discord.Embed(title="Userinfo of "+str(user.name)+" ("+str(user.id)+")", description="User isn't in the database.",
                              color=discord.Color.blue())
        return embed
    embed = discord.Embed(title="Userinfo of " + str(user.name) + " (" + str(user.id) + ")",
                          description="",
                          color=discord.Color.blue())
    if steamid:
        embed.add_field(name="Steam Profile", value="http://steamcommunity.com/profiles/"+str(steamid), inline=False)

    embed.add_field(name="AuthKey", value=str(authkey), inline=False)
    embed.add_field(name="Verification Status", value=str(verified), inline=False)

    return embed