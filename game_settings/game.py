import json
import os

from user_settings.data_managment import PlayerData 


class GameLogic():
    def check_if_won(self, pos, move, side):
        def cast_line(pos, move, v, dir, side):
            len = 0
            x, y = move["x"] + (v[0] * dir), move["y"] + (v[1] * dir)

            while x in range(0, 7) and y in range(0,6):
                if (pos[x][y] == side): len += 1
                else: break
                x += v[0] * dir
                y += v[1] * dir

            return len

        #[x, y]
        vectors = [[1, 0], [1, 1], [1, -1], [0, 1]]
        
        for v in vectors:
            if cast_line(pos, move, v, 1, side) + cast_line(pos, move, v, -1, side) + 1 >= 4:
                return True
        
        return False


    def move(self, move, side, pos):
        #for easier logic coins are goona be saved as P and E
        #then in rendering they will be set to a specified skin by user
        col = ord(move.upper())-65 
        row = pos[col].count(".")-1

        pos[col][row] = side

        if self.check_if_won(pos, {"x": col, "y": row}, side):
            return pos, True

        return pos, False
    

    def get_pos(self, pos, p_id):
        out = "```\n"

        p = PlayerData(p_id, "info")
        skins = p.get_skins()

        
        for row in range(6):
            for col in range(7):
                coin_id = pos[col][row]
                out += skins[f"{coin_id.lower()}_skin"]          
            out += "\n"
        
        return out + "```"





class Game():
    def __init__(self, id):
        self.id = id
        self.path = f"_games/{self.id}"
        self.side_dict = {0: "P", 1: "E", }

        self.game_logic = GameLogic()

        if self.exists():
            self.game = self.get_game()
            return

        print('Game.py __init__: Error, no such game exists')
        print('Game.py __init__: path: ', self.path)

    def exists(self):
        return os.path.exists(self.path)
    

    def get_game(self):
        with open(self.path) as file:
            json_object = json.load(file)

        return json_object
    

    def update_game(self):
        json_object = json.dumps(self.game, indent=4)

        with open(self.path, "w") as file:
            file.write(json_object)
    

    #checks if the move that player did is possible and if it's his turn
    def valid_place(self, move):
        return (move.lower() in ("a", "b", "c", "d", "e", "f", "g"))

    def can_move(self, move):
        return self.game["pos"][ord(move.upper())-65].count(".") > 0
    
    def users_turn(self, cmd_author, p_id, e_id):
        return (cmd_author == p_id and self.game["n_move"]%2 == 0) or (cmd_author == e_id and self.game["n_move"]%2 == 1)


    def make_move(self, move):
        side = self.side_dict[self.game["n_move"]%2]
        self.game["n_move"] += 1

        new_pos, has_won = self.game_logic.move(move, side, self.game['pos'])

        self.game["pos"] = new_pos
        if (has_won):
            return 'game_ended'


        self.update_game()
        return 'game_going'


    def get_position(self):
        return self.game_logic.get_pos(self.game["pos"], self.game["p_id"])


    def update_last_pos_msg(self, msg_id):
        self.game["last_msg"] = msg_id

        self.update_game()

    async def remove_last_pos_msg(self, channel):
        msg = await channel.fetch_message(self.game["last_msg"])

        if msg:
            await msg.delete()


    # Elo calculation method
    def calculate_elo(self, winner_elo, loser_elo):
        K_factor = 40

        # Calculates expected result of player A
        def expected_score(A, B):
            return 1 / (pow(10, ((B-A) / 400)) + 1)
        

        # Calculate expected scorer
        expected_winner_score = expected_score(winner_elo, loser_elo)
        expected_loser_score = expected_score(loser_elo, winner_elo)
        
        # Calculate elo_diff
        winner_elo_diff = K_factor * (1 - expected_winner_score)
        loser_elo_diff = K_factor * (0 - expected_loser_score)


        return winner_elo_diff, loser_elo_diff



    def end_game(self, loser_id, winner_id):
        winner = PlayerData(winner_id, "update")
        loser = PlayerData(loser_id, "update")

        winner_elo = winner.manager.user_data["elo"]
        loser_elo = loser.manager.user_data["elo"]


        winner_elo_diff, loser_elo_diif = self.calculate_elo(winner_elo, loser_elo)

        winner.update_stats(round(winner_elo_diff), "w")
        loser.update_stats(round(loser_elo_diif), "l")


        os.remove(self.path)

