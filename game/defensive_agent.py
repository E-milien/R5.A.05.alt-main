from random import randint
from base_agent import BaseAgent
from server.actions import ActionType

class DefensiveAgent(BaseAgent):
    def __init__(self, id) -> None:

        super().__init__(id, 7, 3, 8, 2)

    def do_action(self):
        characters_alive = self.get_characters_alive()

        if len(characters_alive) <= 2:
            weakest_target = None
            lowest_life = float('inf')
            for character in characters_alive:
                if character['id'] != self.id and character['statistics']['life'] < lowest_life:
                    weakest_target = character['id']
                    lowest_life = character['statistics']['life']
            
            if not weakest_target:
                weakest_target = characters_alive[randint(0, len(characters_alive) - 1)]['id']

            
            return ActionType.HIT, weakest_target
        
        return ActionType.BLOCK, None

    def next_turn(self, turn_id):
        print(f"Turn {turn_id}: Agent {self.id} stats - {self.current}")

    def finished(self):
        print(f"Game finished for Agent {self.id}")
    
    def death(self, turn):
        print(f"Agent {self.id} is dead at turn {turn}")