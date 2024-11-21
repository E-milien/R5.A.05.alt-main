from enum import Enum
from random import randint

class ActionType(Enum):
  HIT = 0
  BLOCK = 1
  DODGE = 2
  FLY = 3

  def from_str(type: str):
    return ActionType[type]

class Action:
  def __init__(self, type: ActionType, source: str, target: str = None) -> None:
    self.type = type

    self.source = source
    self.target = target

  def do(self, arena) -> None:
    source_character = arena.get_character(self.source)
    target_character = arena.get_character(self.target)

    if target_character is None:
      return

    print("Character do action", self.type, "from", self.source, "to", self.target)

    if target_character.is_dead():
      return

    if self.type == ActionType.HIT:
      self.hit(source_character, target_character)

    if self.type == ActionType.FLY:
      arena.leave_character(self.source)

  def hit(self, source, target) -> None:
    if target.action.type == ActionType.BLOCK:
      reduce_damage = ( 1 - (target.armor / (target.armor + 8)) ) * source.strength
      target.statistics.life -= reduce_damage

      return

    if target.action.type == ActionType.DODGE:
      random = randint(0, 25)

      if random > target.speed:
        target.statistics.life -= source.strength

      return

    target.statistics.life -= source.strength
    