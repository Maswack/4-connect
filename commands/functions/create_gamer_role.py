import discord
import os

role_name = "gamer-4-connect"



def create_guild_role_file(role:discord.Role, guild_id:int):
    with open(f"_servers/{guild_id}", "w") as file:
        file.write(f"{role.id}")



def fetch_guild_role_id(guild_id:int):
    role_id = 0

    if not os.path.exists(f"_servers/{guild_id}"):
        return role_id
    
    else:
        with open(f"_servers/{guild_id}", "r") as file:
            role_id = int(file.readline())

    return role_id



def guild_role_exists(guild_id:int):
    if fetch_guild_role_id(guild_id) != 0:
        return True

    return False



async def create_gamer_role(guild:discord.Guild):
    try:
        if not guild_role_exists(guild_id=guild.id):
            gamer_role = await guild.create_role(
                name=role_name,
                reason="responsible for knowing who is a 4-connect-player on the server"
            )

            create_guild_role_file(gamer_role, guild.id)
        else:
            print('Role already exists')

    except Exception as e:
        print("error: ", e)
        return
