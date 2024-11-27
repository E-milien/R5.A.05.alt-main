import requests
import time

from threading import Thread
from server.actions import ActionType

ARENAS = {
  'arena-1': 'http://10.109.150.143:5000',
  'arena-2': 'http://10.109.150.138:5000'
}

class BaseAgent:
  def __init__(self, id: str, life: int, strength: int, armor: int, speed: int):
    self.is_ended = False
    self.id = id

    self.arena_url = None
    self.is_dead = False

    self.base = {
      "life": life * 2,
      "strength": strength,
      "armor": armor,
      "speed": speed
    }

    self.current = {
      "life": life * 2,
      "strength": strength,
      "armor": armor,
      "speed": speed
    }

    self.game_run = False
    
    self.is_started = False

  def get_characters_alive(self):
    response = requests.get(f'{self.arena_url}/characters_alive')
    
    if response.status_code == 200:
      result = response.json()
      return list(filter(lambda character: character['id'] != self.id, result))
    else:
      raise Exception("Error while getting characters alive")

  def action(self, action: ActionType, target_id: str):
    response = requests.post(f"{self.arena_url}/characters/{self.id}/action", json = {
      'type': action.name,
      'target': target_id
    })

    if response.status_code != 200:
      raise Exception("Error while performing action")

  def state(self):
    response = requests.get(f'{self.arena_url}/state')
    if response.status_code != 200:
      raise Exception("Error while getting state")

    return response.json()
  
  def join(self, arena_id: str = None):
    if not arena_id:
      url = list(ARENAS.values())[randint(0, len(ARENAS) - 1)]
    else:
      url = ARENAS[arena_id]

    response = requests.post(f"{url}/characters/{self.id}/join", json = self.base)
    if response.status_code != 200:
      raise Exception("Error while joining the arena")
    
    self.arena_url = url
    
    self.thread = Thread(target = self.loop)
    self.thread.daemon = True
    self.thread.start()

  def leave(self):
    response = requests.post(f'{self.arena_url}/characters/{self.id}/leave')
    if response.status_code != 200:
      raise Exception("Error while leaving the game")

    self.arena_url = None
    self.game_run = False

    return True

  def update(self):
    response = requests.get(f'{self.arena_url}/characters/{self.id}')
    if response.status_code != 200:
      raise Exception("Error while updating character")

    json = response.json()
    
    self.is_dead = json['is_dead']
    self.current = json['statistics']
      
    return True
  
  def do_action(self):
    pass

  def next_turn(self):
    pass

  def death(self, turn):
    pass
    
  def finished(self):
    pass

  def loop(self):
    self.game_run = True

    last_turn = 0
    
    #WAIT GAME STARTED
    while self.game_run:
      state = self.state()

      if state['is_started']:
        break

    action, target_id = self.do_action()
    self.action(action, target_id)

    while self.game_run:
      time.sleep(.5)

      state = self.state()
      turn = state['turn']
      
      self.is_started = state['is_started']

      if last_turn != turn:
        last_turn = turn

        if not self.is_dead:
          self.update()
          
          if self.is_dead:
            self.death(turn)
          else:
            self.next_turn(turn)

        if state['is_finished']:
          self.is_ended = True
          self.finished()
          self.leave()
        else:
          action, target_id = self.do_action()
          self.action(action, target_id)