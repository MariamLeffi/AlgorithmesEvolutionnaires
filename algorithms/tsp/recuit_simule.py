# -*- coding: utf-8 -*-
import math
import random

def distance_totale(sol, dist):
    """Calcule la distance totale d'un parcours"""
    d = 0
    for i in range(len(sol) - 1):
        d += dist[sol[i]][sol[i + 1]]
    d += dist[sol[-1]][sol[0]]  # Retour au départ
    return d

def voisin(sol):
    """Génère un vois in en échangeant deux villes"""
    v = sol[:]
    i, j = random.sample(range(len(sol)), 2)
    v[i], v[j] = v[j], v[i]
    return v

def recuit(dist, T_init, refroid, nb_iter):
    """Algorithme du Recuit Simulé pour TSP"""
    # Solution initiale aléatoire
    sol = list(range(len(dist)))
    random.shuffle(sol)
    best_sol = sol[:]
    best_dist = distance_totale(sol, dist)
    T = T_init
    
    for _ in range(nb_iter):
        v = voisin(sol)
        d_sol = distance_totale(sol, dist)
        d_v = distance_totale(v, dist)
        delta = d_v - d_sol
        
        # Critère d'acceptation
        if delta < 0 or random.random() < math.exp(-delta / T):
            sol = v
            if d_v < best_dist:
                best_sol, best_dist = v[:], d_v
        
        # Refroidissement progressif
        T *= refroid
    
    return best_sol, best_dist

