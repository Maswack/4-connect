import discord
from discord.ext import commands

from user_settings.data_managment import PlayerData


class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="info",
        description="get info about a specific player"
    )
    async def info(self, ctx, user: discord.Member):
        user_info = PlayerData(user.id, "info")

        if not (user_info.exists()):
            await ctx.reply("Player you are trying to get info about is not registered", ephemeral=True, delete_after=5)
            return
        
        #gathering data
        data = user_info.manager.user_data

        name = user.name.capitalize()
        elo = data["elo"]
        w = data["w"]
        l = data["l"]
        win_rate = float(w/(l+w)) * 100 if l != 0 else int(w>0) * 100
        skins = f"player_skin: {data['player_skin']}\nenemy_skin: {data['enemy_skin']}"

        embed = discord.Embed(
            title=f"{name} Info",
            color= 0x26ad00
        )


        embed.add_field(name="elo: ", value=elo, inline=True)
        embed.add_field(name="w/l: ", value=f"{w}/{l}", inline=True)
        embed.add_field(name="winrate: ", value=f"{win_rate}%", inline=True)
        embed.add_field(name="skins", value=skins, inline=False)
        embed.set_image(url=user.avatar)


        await ctx.reply(embed=embed, delete_after=30, ephemeral=True)