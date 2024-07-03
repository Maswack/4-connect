import discord
from discord.ext import commands

from commands.functions.add_gamer_role import add_gamer_role


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        try:
            await add_gamer_role(member=member)

        except Exception as e:
            print("error: ", e)
            return