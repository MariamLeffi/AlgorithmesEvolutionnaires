# -*- coding: utf-8 -*-
import random
from collections import deque

def calculer_makespan(solution, durees_taches):
    """Calcule le makespan (temps total)"""
    temps = 0
    for tache in solution:
        temps += durees_taches[tache]
    return temps

def generer_voisins(solution):
    """Génère les voisins par échange"""
    voisins = []
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def tabu_search_ordonnancement(durees_taches, nombre_iterations, taille_tabu):
    """Recherche Tabou pour ordonnancement"""
    n = len(durees_taches)
    
    # Solution initiale aléatoire
    solution_actuelle = list(range(n))
    random.shuffle(solution_actuelle)
    
    meilleure_solution = solution_actuelle[:]
    meilleur_makespan = calculer_makespan(solution_actuelle, durees_taches)
    
    # Liste tabou
    tabu_list = deque(maxlen=taille_tabu)
    
    for _ in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        
        # Filtrer les tabous
        voisins = [v for v in voisins if v not in tabu_list]
        
        if not voisins:
            break
        
        # Meilleur voisin
        solution_actuelle = min(voisins, key=lambda x: calculer_makespan(x, durees_taches))
        makespan_actuel = calculer_makespan(solution_actuelle, durees_taches)
        
        # Ajouter à la liste tabou
        tabu_list.append(solution_actuelle[:])
        
        # Mise à jour
        if makespan_actuel < meilleur_makespan:
            meilleure_solution = solution_actuelle[:]
            meilleur_makespan = makespan_actuel
    
    return meilleure_solution, meilleur_makespan