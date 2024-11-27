import time
from hit_and_run_agent import HitAndRunAgent
from aggressive_agent import AggressiveAgent
from defensive_agent import DefensiveAgent

def run_game():
    NB_GAMES = 1000
    increment = 0
    while increment < NB_GAMES:
        print(f"Génération {increment + 1}")
        listAgent = []
        listAgent.append(HitAndRunAgent('1'))
        listAgent.append(AggressiveAgent('2'))
        listAgent.append(DefensiveAgent('3'))
        
        for agent in listAgent:
            agent.join('arena-1')

        while True:
            tmp = True
            for agent in listAgent:
                tmp = tmp and agent.is_ended
            if tmp:
                increment += 1
                break                
            else:
                time.sleep(0.5)

# Lancer le jeu
if __name__ == "__main__":
    run_game()