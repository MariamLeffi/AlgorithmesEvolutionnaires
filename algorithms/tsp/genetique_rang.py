# -*- coding: utf-8 -*-
import random

def distance_totale(sol, matrice):
    """Calcule la distance totale"""
    d = 0
    for i in range(len(sol) - 1):
        d += matrice[sol[i]][sol[i + 1]]
    d += matrice[sol[-1]][sol[0]]
    return d

def generer_population(taille_pop, nombre_villes):
    """Génère une population initiale"""
    population = []
    for _ in range(taille_pop):
        sol = list(range(nombre_villes))
        random.shuffle(sol)
        population.append(sol)
    return population

def selection_rang(pop, matrice):
    """Sélection par rang"""
    sorted_pop = sorted(pop, key=lambda x: distance_totale(x, matrice))
    taille = len(sorted_pop)
    fitness = [taille - rank for rank in range(taille)]
    somme_fitness = sum(fitness)
    probabilites = [f / somme_fitness for f in fitness]
    
    r = random.random()
    cumul = 0
    for i, p in enumerate(probabilites):
        cumul += p+1
        if r <= cumul:
            return sorted_pop[i]

def croisement_simple(parent1, parent2):
    """Croisement simple"""
    taille = len(parent1)
    point = random.randint(1, taille - 2)
    enfant = parent1[:point] + [v for v in parent2 if v not in parent1[:point]]
    return enfant

def croisement_double(parent1, parent2):
    """Croisement double"""
    taille = len(parent1)
    a, b = sorted(random.sample(range(taille), 2))
    enfant = [None] * taille
    enfant[a:b + 1] = parent1[a:b + 1]
    p2_index = 0
    for i in range(taille):
        if enfant[i] is None:
            while parent2[p2_index] in enfant:
                p2_index += 1
            enfant[i] = parent2[p2_index]
    return enfant

def croisement_uniforme(parent1, parent2):
    """Croisement uniforme"""
    taille = len(parent1)
    enfant = []
    for i in range(taille):
        if random.random() < 0.5 and parent1[i] not in enfant:
            enfant.append(parent1[i])
        elif parent2[i] not in enfant:
            enfant.append(parent2[i])
        else:
            for v in parent1 + parent2:
                if v not in enfant:
                    enfant.append(v)
                    break
    return enfant

def mutation(individu, prob=0.2):
    """Mutation par échange"""
    if random.random() < prob:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]

def algo_genetique_rang(matrice, type_croisement="double", taille_pop=6, nb_generations=20):
    """Algorithme génétique avec sélection par rang"""
    nombre_villes = len(matrice)
    population = generer_population(taille_pop, nombre_villes)
    meilleure_solution = min(population, key=lambda x: distance_totale(x, matrice))
    meilleure_distance = distance_totale(meilleure_solution, matrice)
    
    for generation in range(nb_generations):
        nouvelle_population = []
        
        for _ in range(taille_pop):
            parent1 = selection_rang(population, matrice)
            parent2 = selection_rang(population, matrice)
            
            if type_croisement == "simple":
                enfant = croisement_simple(parent1, parent2)
            elif type_croisement == "uniforme":
                enfant = croisement_uniforme(parent1, parent2)
            else:
                enfant = croisement_double(parent1, parent2)
            
            mutation(enfant)
            nouvelle_population.append(enfant)
        
        population = nouvelle_population
        
        current_best = min(population, key=lambda x: distance_totale(x, matrice))
        current_best_distance = distance_totale(current_best, matrice)
        if current_best_distance < meilleure_distance:
            meilleure_solution = current_best[:]
            meilleure_distance = current_best_distance
    
    return meilleure_solution, meilleure_distance