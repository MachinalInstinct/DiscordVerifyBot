import discord

adminroles = ["Consul", "Community Manager", "Moderator", "Chat Mod", "Bot"]

def check_mod(ctx):
    roles = ctx.author.roles
    print(roles)

    userroles = [role.name for role in roles]
    userroleslower = [x.lower() for x in userroles]
    print(userroles)

    adminroleslower = [x.lower() for x in adminroles]

    if any(x in userroleslower for x in adminroleslower):
        print("Is admin.")
        return True
    return False