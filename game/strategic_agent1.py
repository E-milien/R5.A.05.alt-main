import time
from random import randint
from base_agent import BaseAgent
from server.actions import ActionType

class StrategicAgent(BaseAgent):
    def __init__(self, id) -> None:
        # Génération aléatoire des statistiques
        listStats = [0, 0, 0, 0]
        for i in range(20):
            randNum = randint(0, 3)
            listStats[randNum] += 1

        super().__init__(id, listStats[0], listStats[1], listStats[2], listStats[3])

    def do_action(self):
        # Récupérer tous les personnages vivants
        characters_alive = self.get_characters_alive()

        # Trouver la cible avec la vie la plus faible
        weakest_target = None
        lowest_life = float('inf')
        for character in characters_alive:
            if character['id'] != self.id and character['statistics']['life'] < lowest_life:
                weakest_target = character['id']
                lowest_life = character['statistics']['life']

        # Si aucune cible valide n'est trouvée (par sécurité), attaquer au hasard
        if not weakest_target:
            weakest_target = characters_alive[randint(0, len(characters_alive) - 1)]['id']

        return ActionType.HIT, weakest_target

    def next_turn(self, turn_id):
        print(f"Turn {turn_id}: Agent {self.id} stats - {self.current}")

    def finished(self):
        print(f"Game finished for Agent {self.id}")
    
    def death(self, turn):
        print(f"Agent {self.id} is dead at turn {turn}, stats: {self.current}")