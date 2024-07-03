from discord.ext import commands
import os


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def create_directories(self):
        dir_list = [
            "_users",
            "_games",
            "_servers",
        ]

        was_dir_added = False

        for dir in dir_list:
            if not os.path.exists(dir):
                os.mkdir(path=dir)
                was_dir_added = True
        

        print('------------------------------------------------------')
        if was_dir_added:
            print("Some data storages were missing so they were added")
        else:
            print("All data storages intact")



    @commands.Cog.listener()
    async def on_ready(self):
        # Create directories (if it's first time running)
        self.create_directories()


        # Made for knowing that it works / whats id it is logged in as
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")


        # Sync commands (so that /commands work)
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"error: {e}")

        print('Bot Ready')
        print('------------------------------------------------------')