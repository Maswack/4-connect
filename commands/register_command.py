from discord.ext import commands
from user_settings.data_managment import PlayerData

from events.in_bot.on_register import on_register_event


class RegisterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

     #Create account t be able to play
    @commands.hybrid_command(
        name="register",
        description="register an account to play"
    )
    async def register(self, ctx):
        # Make event on register command execution (not related to registration procces):
        await on_register_event(ctx.author)

        user_id = ctx.author.id
        user = PlayerData(user_id, operation="create")

        if (user.exists()):
            await ctx.reply("Account already registered", ephemeral=True,  delete_after=5)
            return

        if (user.create_perms()):
            user.create()
            await ctx.reply("Account Created :)", ephemeral=True, delete_after=5)
