import time
from random import randint

from base_agent import BaseAgent
from server.actions import ActionType

class Agent(BaseAgent):
  def __init__(self, id) -> None:
    listStats = [0, 0, 0, 0]
    
    for i in range(20):
      randNum = randint(0, 3)
      listStats[randNum] += 1
    
    super().__init__(id, listStats[0], listStats[1], listStats[2], listStats[3])

  def do_action(self):
    character_alive = self.get_characters_alive()

    target_id = self.id
    while(target_id == self.id):
      target_id = character_alive[randint(0, len(character_alive) - 1)]['id']

    return ActionType.HIT, target_id
  
  def next_turn(self, turn_id):
    print(turn_id, self.id, self.is_dead, self.cu)

  def finished(self):
    print('GAME IS FINISHED')

agent1 = Agent('1')
agent1.join('arena-1')

agent2 = Agent('2')
agent2.join('arena-1')

input()