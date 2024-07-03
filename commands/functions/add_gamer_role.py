import discord
from typing import List


from commands.functions.create_gamer_role import guild_role_exists
from commands.functions.create_gamer_role import fetch_guild_role_id


def print_guild_role_not_exists_error(guild_name, guild_id):
    print("error: ", "guild role does not exist")
    print("guild_id: ", guild_id)
    print("guild_name: ", guild_name)


def has_gamer_role(role:discord.Role, member_roles:List[discord.Role]):
    return role in member_roles



def get_guild_role(member:discord.Member):
    role_id = fetch_guild_role_id(guild_id=member.guild.id)
    return member.guild.get_role(role_id)



async def add_gamer_role(member:discord.Member):
    guild_id = member.guild.id

    if not guild_role_exists(guild_id=guild_id):
        print_guild_role_not_exists_error(guild_name=member.guild.name, guild_id=guild_id)
        return

    
    role = get_guild_role(member=member)


    if not has_gamer_role(role=role, member_roles=member.roles) and role != None:
        try: 
            await member.add_roles(role)
        except Exception as e:
            print("error(member.add_roles): ", e)
    
    elif role == None:
        print("error: ", "role equal to None")


