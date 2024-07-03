import discord

from commands.functions.add_gamer_role import add_gamer_role


async def on_register_event(member: discord.Member):
    try:
        await add_gamer_role(member=member)

    except Exception as e:
        print("error: ", e)
        return