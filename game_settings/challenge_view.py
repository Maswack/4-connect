from typing import Any
import discord


class acceptButton(discord.ui.Button):
    def __init__(self):
        label = "Accept"
        style = discord.ButtonStyle.green

        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        self.view.update_state(True)
        await self.view.end(interaction, "accepted")


class declineButton(discord.ui.Button):
    def __init__(self):
        label = "Decline"
        style = discord.ButtonStyle.red

        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        self.view.update_state(False)
        await self.view.end(interaction, "declined")



class challengeDeclined(discord.ui.Button):
    def __init__(self):
        label = "_____Challenge Declined_____"
        style = discord.ButtonStyle.grey

        super().__init__(label=label, style=style)


class challengeAccepted(discord.ui.Button):
    def __init__(self):
        label = "_____Challenge Accepted_____"
        style = discord.ButtonStyle.blurple

        super().__init__(label=label, style=style)




class challengeView(discord.ui.View):
    accepted = False

    def __init__(self, server_id, channel_id, author):
        super().__init__()

        self.origin = f"{author}  https://discord.com/channels/{server_id}/{channel_id}"

        self.add_item(acceptButton())
        self.add_item(declineButton())


    def update_state(self, state): 
        self.accepted = state

    async def end(self, interaction: discord.Interaction, action):
        self.clear_items()

        if action == "accepted": self.add_item(challengeAccepted())
        else: self.add_item(challengeDeclined())

        await interaction.response.edit_message(content=self.origin, view=self)
        #await interaction.response.edit_message(content="", view=self)

        self.stop()