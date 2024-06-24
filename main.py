import discord
from discord.ext import commands


#----------------------------------------------------
# Commands Import segment
from bot.bot_commands_setup import BotCommandsSetup
from _legacy_files.bot_commands import BotCommands

#Game-related
from commands.challenge_command import ChallengeCommand
from commands.play_command import PlayCommand
from commands.surrender_command import SurrenderCommand

#Settings/Info-related
from commands.register_command import RegisterCommand
from commands.skin_command import SkinCommand
from commands.info_command import InfoCommand
#----------------------------------------------------


from bot.bot_log import BotLog


import os
import asyncio
from dotenv import load_dotenv


#setup intents -> what bot can do
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True


#create bot
bot = commands.Bot(command_prefix='/', intents=intents)

#get the toekn from .env file
load_dotenv() 
TOKEN = os.getenv("TOKEN")


#cog loading
async def cogs_setup():
    await bot.add_cog(BotCommandsSetup(bot))
    await bot.add_cog(BotLog(bot))

    #-------------------------------------------
    #Cog-Adding for commands
    await bot.add_cog(ChallengeCommand(bot))
    await bot.add_cog(PlayCommand(bot))
    await bot.add_cog(SurrenderCommand(bot))

    await bot.add_cog(RegisterCommand(bot))
    await bot.add_cog(SkinCommand(bot))
    await bot.add_cog(InfoCommand(bot))
    #-------------------------------------------

    

#run the cog loading procedure
asyncio.run(cogs_setup())



#load the token and run the bot
bot.run(TOKEN)