import discord
from discord.ext import commands

from user_settings.data_managment import PlayerData
from commands.functions.add_gamer_role import get_guild_role


class RankUserData():
    def __init__(self, id, name, elo) -> None:
        self.id = id
        self.name = name
        self.elo = elo




class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def get_pos_in_ranks(self, user:RankUserData, ranks):
        for i, r in enumerate(ranks):
            if user.elo > r.elo:
                ranks.insert(i, user)
                ranks.pop()
                break



    async def get_rankings(self, guild:discord.Guild, top:int):
        member_count = guild.member_count
        max_top = 25
        
        ranks = [RankUserData(0, "", 0)] * min(top, member_count, max_top) # Choses the lower value so that the rankings are not absurdly big
        
        try:
            async for member in guild.fetch_members():
                guild_role = get_guild_role(member=member) # Check if has 4-connect gamer role

                if guild_role in member.roles:
                    user_info = PlayerData(member.id, "info") # Try to get elo of a player
                    data = user_info.manager.user_data


                    member_rank = RankUserData(member.id, member.global_name, elo=data["elo"]) # Initialize member rank

                    self.get_pos_in_ranks(user=member_rank, ranks=ranks)
                else:
                    continue

        except Exception as e:
            print("error: ", e)
            print("Couldn't fetch members in get_rankings command")

        return ranks



    def format_rank(self, i, rank:RankUserData):
        return f"{i+1}.{rank.name} elo: {rank.elo}\n"




    @commands.hybrid_command(
        name="leaderboard",
        description="get ranking of players on this server"
    )
    async def leaderboard(self, ctx, top:int=10):
        guild = ctx.guild # Prepare data
        msg = ""


        rankings = await self.get_rankings(guild=guild, top=top) # Get the rankings of server players
        

        for i, rank in enumerate(rankings):
            if rank.id != 0: # If not empty data
                msg += self.format_rank(i, rank) # Format to text and add to the msg

        
        embed = discord.Embed(
            title=f"{guild.name} rankings:",
            color= 0x26ad00
        )

        embed.add_field(name="", value=msg)


        await ctx.reply(embed=embed, delete_after=60, ephemeral=True)
        


