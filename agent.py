import os
import time
from dotenv import load_dotenv
from random import randint, choice, random
import requests
from server.actions import ActionType

load_dotenv()

class Agent:
    API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000")

    def __init__(self, stats=None) -> None:
        # Génère les statistiques soit de manière aléatoire soit via des gènes passés
        
        self.left = False
        
        if stats:
            self.life, self.strength, self.armor, self.speed = stats
        else:
            listStats = [0, 0, 0, 0]
            for _ in range(200):
                randNum = randint(0, 3)
                listStats[randNum] += 1
            self.life, self.strength, self.armor, self.speed = listStats

        self.character_id = str(randint(10000, 99999))
        response = requests.post(f"{self.API_URL}/characters/{self.character_id}/join", json={
            'life': self.life,
            'strength': self.strength,
            'armor': self.armor,
            'speed': self.speed
        })
    
    def is_dead(self):
        response = requests.get(f"{self.API_URL}/characters/{self.character_id}")
        data = response.json()
        
        return data["is_dead"]
        
    def leave(self):
        requests.delete(f"{self.API_URL}/characters/{self.character_id}/leave")
        self.left = True

    def fitness(self):
        # Calcul de la "fitness" (survie + dégâts infligés)
        response = requests.get(f"{self.API_URL}/characters/{self.character_id}")
        data = response.json()
        return data.get('damage_dealt', 0) - data.get('damage_taken', 0)

    def do_action(self):
        action = ActionType(randint(0, 2))
        responseCharacters = requests.get(f"{self.API_URL}/characters")
        listCharacters = responseCharacters.json()

        # Choisir une cible différente de soi-même
        target_id = self.character_id
        while target_id == self.character_id:
            target_id = listCharacters[randint(0, len(listCharacters) - 1)]['id']

        responseAction = requests.post(f"{self.API_URL}/characters/{self.character_id}/action", json={
            'type': action.name,
            'target': target_id
        })

        return responseAction.status_code


class GeneticAlgorithm:
    def __init__(self, population_size=10, generations=10, mutation_rate=0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        return [Agent() for _ in range(self.population_size)]

    def mutate(self, stats):
        # Applique une mutation sur les gènes (stats)
        mutated_stats = stats[:]
        if random() < self.mutation_rate:
            index = randint(0, 3)
            adjustment = randint(-2, 2)
            mutated_stats[index] = max(0, mutated_stats[index] + adjustment)
            total = sum(mutated_stats)
            for i in range(len(mutated_stats)):
                mutated_stats[i] = round(mutated_stats[i] * 20 / total)
        return mutated_stats

    def crossover(self, parent1, parent2):
        # Combine les stats de deux parents
        child_stats = [(parent1[i] + parent2[i]) // 2 for i in range(4)]
        return child_stats

    def evolve(self):
        # Initialisation
        population = self.initialize_population()

        for generation in range(self.generations):
            lap, _ = state()
            is_finished = False
            print(f"Generation {generation + 1}/{self.generations}")
            while not is_finished:
                # Évaluation de la fitness
                fitness_scores = []
                for agent in population:
                    if not agent.left and agent.is_dead():
                        agent.leave()
                        pass
                    
                    agent.do_action()  # Simule l'action
                    fitness_scores.append((agent.fitness(), agent))
                    
                while True:
                    time.sleep(.01)
                    currentLap, is_finished = state()
                    if currentLap > lap:
                        break
            
                print(is_finished)
            
                print("prochain tour")

            for agent in population:
                if not agent.left:
                    agent.leave()

            # Sélection des meilleurs
            fitness_scores.sort(reverse=True, key=lambda x: x[0])
            survivors = fitness_scores[:self.population_size // 2]

            # Reproduction
            next_population = []
            for i in range(len(survivors)):
                for j in range(i + 1, len(survivors)):
                    parent1 = survivors[i][1]
                    parent2 = survivors[j][1]
                    child_stats = self.crossover(
                        [parent1.life, parent1.strength, parent1.armor, parent1.speed],
                        [parent2.life, parent2.strength, parent2.armor, parent2.speed]
                    )
                    child_stats = self.mutate(child_stats)
                    next_population.append(Agent(child_stats))

            # Remplissage de la population
            while len(next_population) < self.population_size:
                next_population.append(Agent())

            population = next_population

        # Retour des meilleurs agents après toutes les générations
        return sorted(population, key=lambda agent: agent.fitness(), reverse=True)

def state():
    reponse = requests.get("http://127.0.0.1:5000/state")
    result = reponse.json()
    return result['turn'], result['is_finished']

if __name__ == "__main__":
    ga = GeneticAlgorithm(population_size=10, generations=100, mutation_rate=0.1)
    best_agents = ga.evolve()

    print("Best agent stats:")
    for agent in best_agents[:3]:
        print(f"Life: {agent.life}, Strength: {agent.strength}, Armor: {agent.armor}, Speed: {agent.speed}")