import json
import os

class SetupGame():
    def __init__(self, p_id, e_id, channel):
        self.data = {
            "p_id": p_id,
            "e_id": e_id,
            "channel": channel,
            "last_msg": "",
            "n_move": 0,
            "pos": [["." for x in range(6)] for y in range(7)] 
        }

    def game_exits(self):
        return os.path.exists(f"_games/{self.data['channel']}")


    async def create(self):
        json_object = json.dumps(self.data, indent=4)

        with open(f"_games/{self.data['channel']}", "w") as file:
            file.write(json_object)