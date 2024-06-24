import discord

from game_settings.game import Game


async def end_the_game(winner:discord.Member, channel, game:Game, loser_id:int):
    game.end_game(winner_id=winner.id, loser_id=loser_id)

    embed = discord.Embed(
        title = f"{winner} has won",
        color= 0x26ad00,
    )
    
    embed.set_image(url=winner.avatar)
    embed.add_field(
        name="End position",
        value=game.get_position(),
        inline=False
    )

    await channel.send(embed=embed, delete_after=45)
