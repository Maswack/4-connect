import discord
from discord.ext import commands

from game_settings.game import Game
from commands.functions.end_the_game import end_the_game


class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="play",
        description="play a move in a game of 4-connect moves:[A-G]",
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
            await ctx.reply("You are not participating in this game", ephemeral=True, delete_after=5)
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

        # make the move
        game_status = game.make_move(move=move)
        await game.remove_last_pos_msg(ctx.channel)


        # end the game
        if (game_status == "game_ended"):
            await end_the_game(winner=ctx.author, channel=ctx.channel, game=game, loser_id=enemy_id)
            await ctx.send('')
            return
        

        msg = await ctx.send(game.get_position())
        game.update_last_pos_msg(msg.id)
