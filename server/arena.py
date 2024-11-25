import time
from character import Character
#from metrics import Metrics

class Arena:
  def __init__(self, id: str, min_player_to_start: int = 2) -> None:
    self.id = id

    self.min_player_to_start = min_player_to_start

    #self.metrics = Metrics()

    self.turn = 0
    self.characters = []

    self.leavers = []

    self.golds = {}

    self.run = False

  def add_character(self, character: Character) -> None:
    print(f"Character {character.id} has been connected")
    self.characters.append(character)

  def remove_character(self, id: str) -> None:
    print(f"Character {id} has been removed")
    self.characters = list(filter(lambda character: character.id != id, self.characters))

  def leave_character(self, id: str) -> None:
    self.leavers.append(id)

  def get_character(self, id: str) -> Character:
    for character in self.characters:
      if character.id == id:
        return character
      
  def give_golds(self, character_id: str, value: int):
    if character_id not in self.golds:
      self.golds[character_id] = 0

    print(f"Character {id} give {value} golds")
    self.golds[character_id] += value

  def is_ready(self) -> bool:
    return self.has_required_number_of_characters() and self.everyone_has_an_action()

  def is_finished(self) -> bool:
    number_alive = 0
    
    for character in self.characters:
      if not character.is_dead():
        number_alive += 1
        
    return number_alive <= 1

  def has_required_number_of_characters(self) -> bool:
    return len(self.characters) >= self.min_player_to_start

  def everyone_has_an_action(self) -> bool:
    return all([character.action for character in self.characters])
  
  def update_metrics(self):
    life = dict(map(lambda item: (item.id, item.statistics.life), self.characters))

    self.metrics.push_metrics("golds", { self.id: sum(self.golds.values()) })
    self.metrics.push_metrics("life", life)

    self.metrics.push_metric("alive", len(self.characters))
    
  def exec(self) -> None:
    self.turn += 1
    characters = sorted(self.characters, key=lambda character: character.statistics.speed)

    print("Run turn", self.turn)
    print("Characters count is", len(characters))

    for character in characters:
      if not character.is_dead():
        character.action.do(self)

    for leaver in self.leavers:
      self.remove_character(leaver)

    for character in characters:
      character.reset()

  def loop(self) -> None:
    self.run = True

    while self.run:
      time.sleep(.01)

      #self.update_metrics()

      if self.is_ready():
        self.exec()

  def to_dict(self):
    return {
      "turn": self.turn,
      "is_finished": self.is_finished(),
      
      "characters": [character.to_dict() for character in self.characters],
      
      "leavers": self.leavers,
      "golds": self.golds,
    }