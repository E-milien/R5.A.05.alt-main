import requests
from server.actions import ActionType

ARENAS = {
  'arena-1': 'localhost:5000',
  'arena-2': 'localhost:5000',
  'arena-3': 'localhost:5000',
}

class BaseAgent:
  def __init__(self, id: str, life: int, strength: int, armor: int, speed: int):
    self.id = id

    self.arena_url = None
    self.is_dead = False

    self.base = {
      "life": life,
      "strength": strength,
      "armor": armor,
      "speed": speed
    }

    self.current = {
      "life": life,
      "strength": strength,
      "armor": armor,
      "speed": speed
    }
    
    self.join_arena()
    self.do_action()

  def action(self, action: ActionType, target_id: str):
    response = requests.post(f"{self.arena_url}/characters/{self.character_id}/action", json = {
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
  
  def join(self, arena_id: str):
    url = ARENAS[arena_id]

    response = requests.post(f"{url}/characters/{self.character_id}/join", json = self.base)
    if response != 200:
      raise Exception("Error while joining the arena")
    
    self.arena_url = url

  def leave(self):
    response = requests.post(f'{self.arena_url}/characters/{self.id}/leave')
    if response.status_code != 200:
      raise Exception("Error while leaving the game")

    self.arena_url = None

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

  def finished(self):
    pass

  def loop(self):
    last_turn = 0

    while True:
      state = self.state()
      turn = state['turn']

      if last_turn != turn:
        last_turn = turn

        if state['is_finished']:
          self.finished()
          self.leave()
        else:
          self.update()
          self.do_action()