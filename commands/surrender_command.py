from discord.ext import commands

from game_settings.game import Game

from commands.functions.end_the_game import end_the_game

#-----------------------------------------------------
# ToDo
# ToDo
# ToDo
# ToDo
#-----------------------------------------------------


class SurrenderCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.hybrid_command(
        name="surrender",
        description="Forfeit a game of connect-4",
    )
    async def surrender(self, ctx):
        channel_id = ctx.channel.id
        author_id = ctx.author.id

        game = Game(channel_id)

        if not (game.exists()):
            await ctx.reply("No game is played on this channel, can't surrender",ephemeral=True, delete_after=5)
            return

        player_id = game.game["p_id"]
        enemy_id = game.game["e_id"]


        if not (author_id == player_id or author_id == enemy_id):
            await ctx.reply("You are not participating in this game", ephemeral=True, delete_after=5)
            return
        
        winner_id = player_id if author_id != player_id else enemy_id
        
        # Fetch the player that has won
        guild = ctx.channel.guild
        winner = guild.get_member(winner_id)

        await game.remove_last_pos_msg(ctx.channel)
        await end_the_game(winner=winner, channel=ctx.channel, game=game, loser_id=author_id)
