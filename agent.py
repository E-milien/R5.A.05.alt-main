import os
from dotenv import load_dotenv
from random import randint, choice
import requests
from server.actions import ActionType

load_dotenv() 

class Agent:
  API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000")

  def __init__(self, auto = True) -> None:
    self.auto = auto
    if auto:
    
      listStats = [0,0,0,0]
      
      for i in range(20):
        randNum = randint(0,3)
        listStats[randNum]+=1
      
      self.life, self.strength, self.armor, self.speed = listStats
      
    else :    
      while self.life + self.strength + self.armor + self.speed != 20:
        self.life = int(input("life :"))
        self.strength = int(input("strength :"))
        self.armor = int(input("armor :"))
        self.speed = int(input("speed :"))
        if self.life + self.strength + self.armor + self.speed != 20:
          print("Le total n'est pas égal à 20. Veuillez réessayer.")
          
    self.character_id = str(randint(10000,99999))
    response = requests.post(f"{self.API_URL}/characters/{self.character_id}/join", json = {
      'life':self.life,
      'strength':self.strength,
      'armor':self.armor,
      'speed':self.speed
    })
    
    

  def do_action(self):
    x = requests.get(f"{self.API_URL}/characters/{self.character_id}")
    print(f"{self.character_id} is {'dead' if x.json()['is_dead'] else 'alive'}")  
            
    if self.auto:
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
    else:
      inputAction = int(input("Choisissez une action HIT: 0, BLOCK: 1, DODGE: 2, FLY: 3: "))
      action = ActionType(inputAction)

      responseCharacters = requests.get(f"{self.API_URL}/characters")
      response_data = responseCharacters.json()

      id_list = [item['id'] for item in response_data if item['id'] != self.character_id]
      print("Liste des ids disponibles :")
      print(id_list)

      target_id = None

      while target_id not in id_list:
        target_id = input("Entrez un id cible parmi ceux affichés : ")
        if target_id not in id_list:
            print(f"L'id {target_id} n'est pas valide. Veuillez réessayer.")
        
      responseAction = requests.post(f"{self.API_URL}/characters/{self.character_id}/action", json = {
        'type':action.name,
        'target':target_id
      })
    
    return responseAction.status_code

def play(auto = True):
  if auto:
    perso1 = Agent()
    perso2 = Agent()

    while True:
      perso1.do_action()
      perso2.do_action()
      x = requests.get('http://127.0.0.1:5000/state')
      print(x.text)
      input("fin du tour")
      
  else:
    listPlayer = []
    numPlayer = int(input("nombre d'agent :"))
    for i in range(0,numPlayer):
      listPlayer.append(Agent(False))
    
    for y in listPlayer:
      y.do_action()

play(True)

x = requests.get('http://127.0.0.1:5000/state')
print(x.text)