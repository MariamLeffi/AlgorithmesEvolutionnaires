# -*- coding: utf-8 -*-
import random

def calculer_makespan(sol, durees):
    """Calcule le makespan"""
    return sum(durees[t] for t in sol)

def generer_population(taille_pop, nombre_taches):
    """Génère une population initiale"""
    population = []
    for _ in range(taille_pop):
        sol = list(range(nombre_taches))
        random.shuffle(sol)
        population.append(sol)
    return population

def selection_roulette(population, durees):
    """Sélection par roulette"""
    makespans = [calculer_makespan(ind, durees) for ind in population]
    fitness = [1 / m for m in makespans]
    somme_fitness = sum(fitness)
    probabilites = [f / somme_fitness for f in fitness]
    
    r = random.random()
    cumul = 0
    for i, p in enumerate(probabilites):
        cumul += p
        if r <= cumul:
            return population[i]

def croisement_simple(parent1, parent2):
    """Croisement simple"""
    point = random.randint(1, len(parent1)-2)
    enfant = parent1[:point] + [t for t in parent2 if t not in parent1[:point]]
    return enfant

def croisement_double(parent1, parent2):
    """Croisement double"""
    a, b = sorted(random.sample(range(len(parent1)), 2))
    enfant = [None]*len(parent1)
    enfant[a:b+1] = parent1[a:b+1]
    p2_index = 0
    for i in range(len(parent1)):
        if enfant[i] is None:
            while parent2[p2_index] in enfant:
                p2_index += 1
            enfant[i] = parent2[p2_index]
    return enfant

def croisement_uniforme(parent1, parent2):
    """Croisement uniforme"""
    enfant = []
    for i in range(len(parent1)):
        if random.random() < 0.5 and parent1[i] not in enfant:
            enfant.append(parent1[i])
        elif parent2[i] not in enfant:
            enfant.append(parent2[i])
        else:
            for t in parent1 + parent2:
                if t not in enfant:
                    enfant.append(t)
                    break
    return enfant

def mutation(individu, prob=0.2):
    """Mutation"""
    if random.random() < prob:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]

def algo_genetique_roulette(durees, type_croisement="double", taille_pop=6, nb_generations=20):
    """Algorithme génétique avec roulette"""
    nombre_taches = len(durees)
    population = generer_population(taille_pop, nombre_taches)
    meilleure_solution = min(population, key=lambda x: calculer_makespan(x, durees))
    meilleur_makespan = calculer_makespan(meilleure_solution, durees)
    
    for _ in range(nb_generations):
        nouvelle_population = []
        
        for _ in range(taille_pop):
            parent1 = selection_roulette(population, durees)
            parent2 = selection_roulette(population, durees)
            
            if type_croisement == "simple":
                enfant = croisement_simple(parent1, parent2)
            elif type_croisement == "uniforme":
                enfant = croisement_uniforme(parent1, parent2)
            else:
                enfant = croisement_double(parent1, parent2)
            
            mutation(enfant)
            nouvelle_population.append(enfant)
        
        population = nouvelle_population
        current_best = min(population, key=lambda x: calculer_makespan(x, durees))
        current_best_makespan = calculer_makespan(current_best, durees)
        if current_best_makespan < meilleur_makespan:
            meilleure_solution = current_best[:]
            meilleur_makespan = current_best_makespan
    
    return meilleure_solution, meilleur_makespan