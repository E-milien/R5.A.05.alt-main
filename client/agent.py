import os
from dotenv import load_dotenv
from random import randint
import requests

load_dotenv() 

class Agent:
  API_URL = os.environ.get("API_URL", "http://localhost:5000")

  def __init__(self) -> None:
    self.life = self.strength = self.armor = self.speed = 0
    while(self.life + self.strength + self.armor + self.speed != 20):
      self.life = int(input("life :"))
      self.strength = int(input("strength :"))
      self.armor = int(input("armor :"))
      self.speed = int(input("speed :"))

    self.character_id = randint(10000,99999)
    response = requests.post(f"{self.API_URL}/characters/{self.character_id}/join", json = {
      'life':self.life,
      'strength':self.strength,
      'armor':self.armor,
      'speed':self.speed
    })

    return response.status_code

  def do_action(self):
    pass


perso1 = Agent()
perso2 = Agent()

x = requests.get(perso.API_URL + '/state')

print(x.text)