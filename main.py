import discord
from discord.ext import commands

from bot_commands_setup import BotCommandsSetup
from bot_commands import BotCommands

from bot_log import BotLog


import os
import asyncio
from dotenv import load_dotenv


#setup intents -> what bot can do
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#create bot
bot = commands.Bot(command_prefix='/', intents=intents)

#get the toekn from .env file
load_dotenv() 
TOKEN = os.getenv("TOKEN")


#cog loading
async def cogs_setup():
    await bot.add_cog(BotCommands(bot))
    await bot.add_cog(BotCommandsSetup(bot))
    await bot.add_cog(BotLog(bot))
    

#run the cog loading procedure
asyncio.run(cogs_setup())



#load the token and run the bot
bot.run(TOKEN)