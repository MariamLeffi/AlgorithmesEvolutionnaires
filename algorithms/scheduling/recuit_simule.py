# -*- coding: utf-8 -*-
import math
import random

def calculer_makespan(sol, durees):
    """Calcule le makespan"""
    return sum(durees[t] for t in sol)

def voisin(sol):
    """Génère un voisin par échange"""
    v = sol[:]
    i, j = random.sample(range(len(sol)), 2)
    v[i], v[j] = v[j], v[i]
    return v

def recuit_ordonnancement(durees, T_init, refroid, nb_iter):
    """Recuit simulé pour ordonnancement"""
    sol = list(range(len(durees)))
    random.shuffle(sol)
    best_sol = sol[:]
    best_makespan = calculer_makespan(sol, durees)
    T = T_init
    
    for _ in range(nb_iter):
        v = voisin(sol)
        m_sol = calculer_makespan(sol, durees)
        m_v = calculer_makespan(v, durees)
        delta = m_v - m_sol
        
        # Critère d'acceptation
        if delta < 0 or random.random() < math.exp(-delta / T):
            sol = v
            if m_v < best_makespan:
                best_sol = v[:]
                best_makespan = m_v
        
        # Refroidissement
        T *= refroid
    
    return best_sol, best_makespan