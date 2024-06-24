import discord


options=[
    discord.SelectOption(label="🟨", value="🟨"),
    discord.SelectOption(label="🟧", value="🟧"),
    discord.SelectOption(label="🟥", value="🟥"),
    discord.SelectOption(label="🟦", value="🟦"),
    discord.SelectOption(label="🟪", value="🟪"),
    discord.SelectOption(label="🟩", value="🟩"),
    discord.SelectOption(label="🟫", value="🟫"),
    discord.SelectOption(label="⬜", value="⬜"),


    discord.SelectOption(label="💎", value="💎"),
    discord.SelectOption(label="👮", value="👮"),
    discord.SelectOption(label="🤓", value="🤓"),
    discord.SelectOption(label="🧐", value="🧐"),
    discord.SelectOption(label="🏳️‍⚧️", value="🏳️‍⚧️"),
    discord.SelectOption(label="🏳️‍🌈", value="🏳️‍🌈"),
    discord.SelectOption(label="💀", value="💀"),
]


class EnemySkin(discord.ui.Select):
    def __init__(self):
        placeholder="What skin do you want to use for your enemy's coins"

        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.update_enemy_skin(self.values[0])
        self.placeholder = f"enemy skin: {self.values[0]}"
        self.disabled = True

        await interaction.response.edit_message(view=self.view)


class PlayerSkin(discord.ui.Select):
    def __init__(self):
        placeholder=f"What skin do you want to use for your coins"

        super().__init__(placeholder=placeholder, options=options)


    async def callback(self, interaction: discord.Interaction):
        self.view.update_player_skin(self.values[0])
        self.placeholder = f"player skin: {self.values[0]}"
        self.disabled = True
        
        await interaction.response.edit_message(view=self.view)



class SkinView(discord.ui.View):
    player_skin = None
    enemy_skin = None

    def __init__(self):
        super().__init__()
        
        self.add_item(PlayerSkin())


    def update_player_skin(self, values):
        self.player_skin = values

        self.add_item(EnemySkin())


    def update_enemy_skin(self, values):
        self.enemy_skin = values

        self.stop()

