from actions import Action

class Statistics:
  def __init__(self, life: int, strength: int, armor: int, speed: int) -> None:
    self.life = life
    self.strength = strength
    self.armor = armor
    self.speed = speed

class Character:
  def __init__(self, id: str, statistics: Statistics) -> None:
    self.id = id
    self.statistics = statistics

    self.action = None

  def is_dead(self) -> bool:
    return self.statistics.life <= 0

  def prepare_action(self, action: Action):
    self.action = action

  def reset(self):
    self.action = None
    