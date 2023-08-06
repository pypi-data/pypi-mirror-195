from valclient import *

class Main:
    def __init__(self):
        self.logarValorant()

    def logarValorant(self):
        self.client = Client(region="br")
        self.client.activate()
    
class ExternalPick(Main):
    def select(self, agent):
        self.client.pregame_select_character(agent)

    def lock(self, agent):
        self.client.pregame_lock_character(agent)

    def instalock(self, agent):
        self.client.pregame_select_character(agent)
        self.client.pregame_lock_character(agent)
    
    # def log(self, player):
    #     match = self.client.pregame_fetch_match()
    #     print(match["MapID"])
    #     print(self.get_player_name_from_puid(match["AllyTeam"]["Players"][player]["Subject"]))
    #     try:
    #         print(self.agent_name_from_id(match["AllyTeam"]["Players"][player]["CharacterID"]))
    #     except:
    #         print("Pickando")
    #     print(match["AllyTeam"]["Players"][player]["CharacterSelectionState"])
        
        