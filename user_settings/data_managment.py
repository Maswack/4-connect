import json
import os


class PlayerData():
    def __init__(self, id, operation):
        self.id = id
        self.manager = DataManager(id, operation)


    def exists(self):
        return self.manager.data_exists()

    def get(self):
        return self.manager.user_data
    
    def create_perms(self):
        return self.manager.has_create_perms()
    
    def update_info_perms(self):
        return self.manager.has_update_info_perms()

    def create(self):
        self.manager.save_user_data()

    def update_skins(self, player_skin, enemy_skin): 
        self.manager.update_skins(player_skin, enemy_skin)

    def get_skins(self):
        return self.manager.get_skins()

    def update_stats(self, elo_gain, result):
        self.manager.update_aftergame(elo_gain, result)




class DataManager():
    def __init__(self, id, operation):
        self.id = id
        self.operation = operation
        self.user_data = {
            "id": id,
            "elo": 1000,
            "w": 0,
            "l": 0,
            "player_skin": "🟨",
            "enemy_skin": "🟥",
            "empty_skin": "⬛"
        }

        self.operation_validity()


    #checks if data managment mode is correct
    def operation_validity(self):   
        if self.has_create_perms():
            print(f"creating new user of id: {self.id}")
            return


        if self.has_update_info_perms():
            print(f"updating or getting info about user with id: {self.id}")

            self.user_data = self.get_user_data()
  
        else:
            print(f"Error no user with specified id, (ID: {self.id})")      


    #function responsible for checking operation perms 
    def has_update_info_perms(self):
        return (self.operation == "update" or self.operation == "info") and self.data_exists()

    def has_create_perms(self):
        return self.operation == "create" and (not self.data_exists())

    #checks if player exist:
    def data_exists(self):
        return os.path.exists(f"_users/{self.id}")

  

    #Reads a specific user data
    def get_user_data(self):
        with open(f"_users/{self.id}") as openfile:
            json_object = json.load(openfile)

        return json_object
    

    #Saves user data to a file
    def save_user_data(self):
        json_object = json.dumps(self.user_data, indent=4)

        with open(f"_users/{self.id}", "w") as outfile:
            outfile.write(json_object) 
    


    #Updates Elo after game
    def update_aftergame(self, elo_gain, result):
        self.user_data["elo"] += elo_gain
        self.user_data[result] += 1

        self.save_user_data()



    #updates skins on the end of customizing the skins
    def update_skins(self, player_skin, enemy_skin):
        self.user_data["player_skin"] = player_skin
        self.user_data["enemy_skin"] = enemy_skin

        self.save_user_data()

    
    def get_skins(self):
        return {"p_skin": self.user_data["player_skin"], "e_skin": self.user_data["enemy_skin"], "._skin": self.user_data["empty_skin"]}

        