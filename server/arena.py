import time
from character import Character
from metrics import Metrics

class Arena:
  def __init__(self, id: str, min_player_to_start: int = 2) -> None:
    self.id = id

    self.min_player_to_start = min_player_to_start
    self.metrics = Metrics()

    self.reset()

  def add_character(self, character: Character) -> None:
    print(f"Character {character.id} has been connected")
    
    self.metrics.push_events("character_join", self.id)
    self.characters.append(character)

  def remove_character(self, id: str) -> None:
    print(f"Character {id} has been removed", self.id)

    self.metrics.push_events("character_leave", self.id)
    self.characters = [character for character in self.characters if character.id != id]

  def leave_character(self, id: str) -> None:
    self.leavers.append(id)

  def get_character(self, id: str) -> Character:
    for character in self.characters:
      if character.id == id:
        return character
      
  def get_characters_alive(self) -> list:
    return [character for character in self.characters if not character.is_dead()]
  
  def get_characters_dead(self) -> list:
    return [character for character in self.characters if character.is_dead()]

  def is_ready(self) -> bool:
    return self.has_required_number_of_characters() and self.everyone_has_an_action()

  def is_finished(self) -> bool:
    return self.is_started and len(self.get_characters_alive()) <= 1

  def has_required_number_of_characters(self) -> bool:
    return len(self.characters) >= self.min_player_to_start

  def everyone_has_an_action(self) -> bool:
    return all([character.action for character in self.get_characters_alive()])
  
  def reset(self) -> None:
    self.turn = 0
    self.characters = []

    self.leavers = []

    self.is_started = False
    
  def push_metrics(self) -> None:
    self.metrics.push_metric("state", self.id, { 
      "turn": self.turn,
      "total": len(self.characters),
      "death": len(self.get_characters_dead()),
      "alive": len(self.get_characters_alive())
    })

    for character in [character.to_dict() for character in self.characters]:
      self.metrics.push_metric("character", self.id, character)

  def exec(self) -> None:
    self.turn += 1
    characters = sorted(self.characters, key = lambda character: character.statistics.speed)

    print("Run turn", self.turn)
    print("Characters count is", len(characters))

    for character in characters:
      if character.is_dead():
        continue

      character.action.do(self)

    for leaver in self.leavers:
      self.remove_character(leaver)

    for character in characters:
      character.reset()

  def main_loop(self) -> None:
    while True:
      time.sleep(.5)
      
      if not self.is_started and self.has_required_number_of_characters():
        self.is_started = True

      if self.is_ready():
        self.exec()
        self.push_metrics()

  def check_loop(self) -> None:
    while True:
      time.sleep(.5)

      if self.is_finished() and len(self.characters) <= 0:
        self.reset()

  def to_dict(self):
    return {
      "state": {
        "turn": self.turn,

        "is_started": self.is_started,
        "is_finished": self.is_finished(),
      },

      "characters": [character.to_dict() for character in self.characters],
      "characters_alive": [character.to_dict() for character in self.get_characters_alive()],
      "characters_dead": [character.to_dict() for character in self.get_characters_dead()],
      
      "leavers": self.leavers,
    }