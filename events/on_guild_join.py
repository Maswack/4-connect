import discord
from discord.ext import commands

from commands.functions.create_gamer_role import create_gamer_role
from commands.functions.add_gamer_role import add_gamer_role


class OnGuildJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_name = "4-connect-gamer"
    

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        # Create a gamer role
        try:
            await create_gamer_role(guild=guild)
        except Exception as e:
            print("error: ", e)
            return


        print('Guild joined: ',guild.name)
        print('Guild id: ', guild.id)
        print("--------------------------------------")

        # Here bot is trying to add role to members of a server
        # That are in data
        try:
            async for member in guild.fetch_members():
                await add_gamer_role(member)
            
        except Exception as e:
            print("error: ", e)
            print('was not able to add gamer_role to all members of a joined server')