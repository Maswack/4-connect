import discord
from discord.ext import commands

from user_settings.data_managment import PlayerData
from user_settings.user_settings import SkinView

from game_settings.game_setup import SetupGame
from game_settings.game import Game

from game_settings.challenge_view import challengeView

import time

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





    #Create account t be able to play
    @commands.hybrid_command(
        name="register",
        description="register an account to play"
    )
    async def register(self, ctx):
        user_id = ctx.author.id
        user = PlayerData(user_id, operation="create")

        if (user.exists()):
            await ctx.reply("Account already registered", ephemeral=True,  delete_after=5)
            return

        if (user.create_perms()):
            user.create()
            await ctx.reply("Account Created :)", ephemeral=True, delete_after=5)





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

    



    @commands.hybrid_command(
        name="challenge",
        description="challenge someone to a game of 4-connect",
    )
    async def challenge(self, ctx, enemy_member: discord.Member):
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


        game_setup = SetupGame(p_id=player_id, e_id=enemy_id, channel=channel_id)
        if game_setup.game_exits():
            await ctx.reply("Game is already played on this channel", ephemeral=True, delete_after=5)
            return
    

        #Send a challenge to oponent
        view = challengeView(ctx.guild.id , ctx.channel.id, ctx.author)

        await enemy_member.send(content=f"{ctx.author.name.capitalize()} send you a 4-connect challenge", view=view)
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
        




    @commands.hybrid_command(
        name="play",
        description="play a move in a game of 4-connect",
    )
    async def play(self, ctx, move:str):
        channel_id = ctx.channel.id
        author_id = ctx.author.id

        game = Game(channel_id)

        if not (game.exists()):
            await ctx.reply("No game is played on this channel, can't make a move",ephemeral=True, delete_after=5)
            return

        player_id = game.game["p_id"]
        enemy_id = game.game["e_id"]


        if not (author_id == player_id or author_id == enemy_id):
            await ctx.reply("You are not a player nor enemy in this game", ephemeral=True, delete_after=5)
            return

        #move validity check
        if not (game.valid_place(move)):
            await ctx.reply("You made a move that is not allowed, choose a column from A-G", ephemeral=True, delete_after=5)
            return
    
        if not (game.can_move(move)):
            await ctx.reply("You made a move that is not allowed, column you choosed is already full", ephemeral=True, delete_after=5)
            return

        if not (game.users_turn(author_id, p_id=player_id, e_id=enemy_id)):
            await ctx.reply("Wait for your turn", ephemeral=True, delete_after=5)
            return

        #make the move
        game_status = game.make_move(move=move)
        await game.remove_last_pos_msg(ctx.channel)

        if (game_status == "game_ended"):
            game.end_game()

            embed = discord.Embed(
                title = f"{ctx.author} has won",
                color= 0x26ad00,
            )
            
            embed.set_image(url=ctx.author.avatar)
        
            await ctx.send(embed=embed, delete_after=45)
            return
        

        msg = await ctx.send(game.get_position())
        game.update_last_pos_msg(msg.id)
        

