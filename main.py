import discord
from discord.ext import commands


#----------------------------------------------------
#Game-related commands
from commands.challenge_command import ChallengeCommand
from commands.play_command import PlayCommand
from commands.surrender_command import SurrenderCommand

#Settings/Info-related commands
from commands.register_command import RegisterCommand
from commands.skin_command import SkinCommand
from commands.info_command import InfoCommand
from commands.leaderboard_command import LeaderboardCommand
from commands.help_command import HelpCommand
#----------------------------------------------------


#----------------------------------------------------
from events.on_ready import OnReady
from events.on_member_join import OnMemberJoin
from events.on_guild_join import OnGuildJoin
#----------------------------------------------------


# Os stuff
import os
import asyncio
from dotenv import load_dotenv


#setup intents -> what bot can do
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True


#create bot
bot = commands.Bot(command_prefix='/', intents=intents)

#get the toekn from .env file
load_dotenv() 
TOKEN = os.getenv("TOKEN")


#cog loading
async def cogs_setup():
    #-------------------------------------------
    # Cog-Adding for commands
    await bot.add_cog(ChallengeCommand(bot))
    await bot.add_cog(PlayCommand(bot))
    await bot.add_cog(SurrenderCommand(bot))

    await bot.add_cog(RegisterCommand(bot))
    await bot.add_cog(SkinCommand(bot))
    await bot.add_cog(InfoCommand(bot))
    await bot.add_cog(LeaderboardCommand(bot))
    await bot.add_cog(HelpCommand(bot))
    #-------------------------------------------
    # Cog-Adding for events
    await bot.add_cog(OnReady(bot))
    await bot.add_cog(OnMemberJoin(bot))
    await bot.add_cog(OnGuildJoin(bot))
    #-------------------------------------------

#run the cog loading procedure
asyncio.run(cogs_setup())



#load the token and run the bot
bot.run(TOKEN)