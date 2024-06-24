from discord.ext import commands

from user_settings.data_managment import PlayerData
from user_settings.user_settings import SkinView

class SkinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Configure settings for your 4-connect game

    @commands.hybrid_command(
        name="set_skins",
        description="set a special icon for 4-connect coins"
    )
    async def set_skins(self, ctx):
        user_id = ctx.author.id
        user = PlayerData(user_id, operation="update")

        if not (user.exists()):
            await ctx.reply("Account not created, register to proceed", ephemeral=True, delete_after=5)
            return
        
        view = SkinView()

        await ctx.reply(view=view, ephemeral=True)
        await view.wait()

        if (user.update_info_perms()):
            if (view.player_skin == view.enemy_skin):
                await ctx.reply("Skins are the same please choose diffrent ones", ephemeral=True, delete_after=5)
                return
            
            user.update_skins(view.player_skin, view.enemy_skin)

            await ctx.reply("Skins succesfully updated", ephemeral=True, delete_after=5)
            return
      
        print("Skins updated [failed], no update perms")
