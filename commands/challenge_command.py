import discord
from discord.ext import commands

# For options in [mode] parameter
from typing import Literal


from user_settings.data_managment import PlayerData

from game_settings.game_setup import SetupGame
from game_settings.game import Game

from game_settings.challenge_view import challengeView



class ChallengeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # Challenge other player to a battle
    @commands.hybrid_command(
        name="challenge",
        description="challenge someone to a game of 4-connect",
    )
    async def challenge(self, ctx, enemy_member: discord.Member, mode: Literal["casual", "competetive"]):
        player_id = ctx.author.id
        enemy_id = enemy_member.id 
        channel_id = ctx.channel.id

        player = PlayerData(player_id, "info")
        enemy = PlayerData(enemy_id, "info")


        if (player_id == enemy_id):
            await ctx.reply("You can't play against yourself lmao", ephemeral=True, delete_after=5)
            return
        
        if not (player.exists()):
            await ctx.reply("You are not registered in the system, please do that", ephemeral=True, delete_after=5)
            return
        
        if not (enemy.exists()):
            await ctx.reply("Player you are trying to challenge is not registered", ephemeral=True, delete_after=5)
            return

        # doesn't work enemy_status always returns 'offline', probably a bug
        # enemy_status = enemy_member.status

        # if (enemy_status in (discord.Status.offline, discord.Status.invisible)):
        #    await ctx.reply("Player you are trying to challenge is offline or does not want to be disturbed", ephemeral=True, delete_after=5)
        #    return


        game_setup = SetupGame(p_id=player_id, e_id=enemy_id, channel=channel_id, mode=mode)
        if game_setup.game_exits():
            await ctx.reply("Game is already played on this channel", ephemeral=True, delete_after=5)
            return
    

        #Send a challenge to oponent
        view = challengeView(ctx.guild.id , ctx.channel.id, ctx.author)

        await enemy_member.send(content=f"{ctx.author.name.capitalize()} send you a 4-connect challenge [{mode}]", view=view)
        await ctx.reply("...", ephemeral=True, delete_after=5)
        await view.wait()


        #Check if challenge accepted
        if not (view.accepted):
            await ctx.reply("Your challenge proposal was swiftly declined", ephemeral=True, delete_after=5)
            return

        await ctx.reply("Your enemy has accepted your proposition", ephemeral=True, delete_after=5)

        #creating a game and getting it even tho it is still not recognised in the system
        await game_setup.create()
        game = Game(channel_id)
        
        #Sending basic startic position
        msg = await ctx.send(game.get_position())
        game.update_last_pos_msg(msg.id)
        