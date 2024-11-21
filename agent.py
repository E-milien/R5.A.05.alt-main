import os
import json
from dotenv import load_dotenv
from random import randint, choice
import requests
from server.actions import ActionType

load_dotenv() 

class Agent:
  API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000")

  def __init__(self) -> None:
    listStats = [0,0,0,0]
    
    for i in range(20):
      randNum = randint(0,3)
      listStats[randNum]+=1
    
    
    self.life, self.strength, self.armor, self.speed = listStats
 
    print(self.life)
    
    # while(self.life + self.strength + self.armor + self.speed != 20):
    #   self.life = int(input("life :"))
    #   self.strength = int(input("strength :"))
    #   self.armor = int(input("armor :"))
    #   self.speed = int(input("speed :"))

    self.character_id = str(randint(10000,99999))
    response = requests.post(f"{self.API_URL}/characters/{self.character_id}/join", json = {
      'life':self.life,
      'strength':self.strength,
      'armor':self.armor,
      'speed':self.speed
    })

  def do_action(self):
    action = choice(list(ActionType))
    responseCharacters = requests.get(f"{self.API_URL}/characters")
    listCharacters = responseCharacters.json()
    target_id = self.character_id
    
    while(target_id == self.character_id):
      target_id = listCharacters[randint(0,len(listCharacters)-1)]['id']
      
    responseAction = requests.post(f"{self.API_URL}/characters/{self.character_id}/action", json = {
      'type':action.name,
      'target':target_id
    })
    
    return responseAction.text
    

perso1 = Agent()
perso2 = Agent()

perso1.do_action()
perso2.do_action()


# x = requests.get(perso.API_URL + '/state')
# print(x.text)