import time
from character import Character

class Arena:
  def __init__(self, min_player_to_start: int = 2) -> None:
    self.min_player_to_start = min_player_to_start

    self.turn = 0
    self.characters = []

    self.leavers = []

    self.golds = {}

    self.run = False

  def add_character(self, character: Character) -> None:
    self.characters.append(character)

  def remove_character(self, id: str) -> None:
    self.characters = self.characters.filter(lambda character: character.id != id)

  def leave_character(self, id: str) -> None:
    self.leavers.append(id)

  def get_character(self, id: str) -> Character:
    for character in self.characters:
      if character.id == id:
        return character

  def is_ready(self) -> bool:
    return self.has_required_number_of_characters() and self.everyone_has_an_action()

  def has_required_number_of_characters(self) -> bool:
    return len(self.characters) >= self.min_player_to_start

  def everyone_has_an_action(self) -> bool:
    return all([character.action for character in self.characters])
  
  def exec(self) -> None:
    self.turn += 1
    characters = sorted(self.characters, key=lambda character: character.statistics.speed)

    print("Run turn", self.turn)
    print("Characters count is", len(characters))

    for character in characters:
      character.action.do(self)

    for leaver in self.leavers:
      print("Character leave the arena", leaver)
      self.remove_character(leaver)

    for character in characters:
      character.reset()

  def loop(self) -> None:
    self.run = True

    while self.run:
      time.sleep(.5)

      if self.is_ready():
        self.exec()

  def to_dict(self):
    return {
      "turn": self.turn,
      "characters": [character.to_dict() for character in self.characters],
      
      "leavers": self.leavers,
      "golds": self.golds,
    }