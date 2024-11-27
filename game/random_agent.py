from random import randint
from base_agent import BaseAgent
from server.actions import ActionType

class RandomAgent(BaseAgent):
    def __init__(self, id) -> None:
        listStats = [1, 1, 1, 1]
        for i in range(16):
            randNum = randint(0, 3)
            listStats[randNum] += 1

        super().__init__(id, listStats[0], listStats[1], listStats[2], listStats[3])

    def do_action(self):
        characters_alive = self.get_characters_alive()
        target = None
        if len(characters_alive) >= 1:
            target = characters_alive[randint(0, len(characters_alive) - 1)]['id']
            action = ActionType(randint(0,2))
        else:
            action = ActionType(randint(1,2))

        return action, target

    def next_turn(self, turn_id):
        print(f"Turn {turn_id}: Agent {self.id} stats - {self.current}")

    def finished(self):
        print(f"Game finished for Agent {self.id}")
    
    def death(self, turn):
        print(f"Agent {self.id} is dead at turn {turn}")