import discord
from discord.ext import commands

from bot.useful_data.photo_links import PhotoLinks
from bot.useful_data.embed_lines import EmbedLines

from dotenv import load_dotenv
import os

load_dotenv()

AUTHOR_ID = os.getenv("AUTHOR_ID")
AUTHOR_AVATAR = os.getenv("AUTHOR_AVATAR") 


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="4_connect_help",
        description="shows some usefull info"
    )
    async def help(self, ctx):
        info_line = EmbedLines.help_lines["help"]+EmbedLines.help_lines["info"]
        info_line += EmbedLines.help_lines["register"]+EmbedLines.help_lines["set_skins"]
        

        game_line = EmbedLines.help_lines["challenge"]+EmbedLines.help_lines["play"]
        game_line += EmbedLines.help_lines["surrender"]
        

        
        embed = discord.Embed(
            title=f"Help Page",
            color= discord.Color.blurple()
        )

        embed.set_thumbnail(url=PhotoLinks.photoDict["stars1"])

        # Info / Settings commands
        embed.add_field(
            name="Info / Settings commands",
            value=info_line,
            inline=False
        )

        # Seperator
        embed.add_field(name="", value="")

        # Game commands
        embed.add_field(
            name="Game commands",
            value=game_line,
            inline=False
        )
        
        
        # Seperator
        embed.add_field(name="", value="")

        # Github project page
        embed.add_field(name="Checkout the github page: ", value="[4-connect repo](https://github.com/Maswack/4-connect)", inline=False)


        # Handling getting the author name
        author = None
        try:
            author = await self.bot.fetch_user(AUTHOR_ID)
        except Exception as err:
            print("Error, couldn't find user of specified AUTHOR_ID")
            print("Error detail: ", err)
            return
        
        # Setting the Footer
        embed.set_footer(
            text="bot created by: " + author.global_name.capitalize(),
            icon_url=AUTHOR_AVATAR
        )

        # Sending reply
        await ctx.reply(embed=embed, ephemeral=True, delete_after=60)