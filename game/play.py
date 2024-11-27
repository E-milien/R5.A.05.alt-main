import time
from hit_and_run_agent import HitAndRunAgent
from aggressive_agent import AggressiveAgent
from defensive_agent import DefensiveAgent
from random_agent import RandomAgent
from threading import Thread


def run_game():
    gameRandom = Thread(target = game_rand)
    gameRandom.daemon = True

    gameRandom.start()
    
    gameStart = Thread(target = game_strat)
    gameStart.daemon = True

    gameStart.start()
    
    gameRandom.join()
    gameStart.join()    
                
def game_rand():
    NB_GAMES = 100
    increment1 = 0
    while increment1 < NB_GAMES:
        print(f"Génération rand {increment1 + 1}")
        listAgentRand = []
        listAgentRand.append(RandomAgent('random 1'))
        listAgentRand.append(RandomAgent('random 2'))
        listAgentRand.append(RandomAgent('random 3'))
        listAgentRand.append(RandomAgent('random 4'))
        listAgentRand.append(RandomAgent('random 5'))
        listAgentRand.append(RandomAgent('random 6'))
        
        for agent in listAgentRand:
            agent.join('arena-2')

        while True:
            tmp = True
            for agent in listAgentRand:
                tmp = tmp and agent.is_ended
            if tmp:
                increment1 += 1
                break                
            else:
                time.sleep(0.5)

def game_strat():
    NB_GAMES = 100
    increment2 = 0
    while increment2 < NB_GAMES:
        print(f"Génération strat {increment2 + 1}")
        listAgent = []
        
        for i in range(15):
            listAgent.append(HitAndRunAgent(f'hit&run {i}'))
            listAgent.append(AggressiveAgent(f'aggressive {i}'))
            listAgent.append(DefensiveAgent(f'defensive {i}'))
            listAgent.append(RandomAgent(f'random {i}'))
        
        for agent in listAgent:
            agent.join('arena-1')

        while True:
            tmp = True
            for agent in listAgent:
                tmp = tmp and agent.is_ended
            if tmp:
                increment2 += 1
                break                
            else:
                time.sleep(0.5)

# Lancer le jeu
if __name__ == "__main__":
    run_game()