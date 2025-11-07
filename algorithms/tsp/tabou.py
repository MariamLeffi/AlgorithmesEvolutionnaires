# -*- coding: utf-8 -*-
import random
from collections import deque

def calculer_distance_totale(solution, matrice_distances):
    """Calcule la distance totale d'un parcours TSP (retour au départ)"""
    distance_totale = 0
    # Somme des distances entre chaque paire consecutive
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    # Ajouter la distance retour
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisins(solution):
    """Génère tous les voisins par échange de deux villes"""
    voisins = []
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    """Recherche Tabou pour le TSP"""
    nombre_villes = len(matrice_distances)
    
    # Solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    
    # Initialiser la meilleure solution
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)
    
    # Liste tabou avec taille maximale
    tabu_list = deque(maxlen=taille_tabu)
    
    for _ in range(nombre_iterations):
        # Générer tous les voisins
        voisins = generer_voisins(solution_actuelle)
        
        # Filtrer les voisins tabous
        voisins = [v for v in voisins if v not in tabu_list]
        
        if not voisins:
            break
        
        # Choisir le meilleur voisin
        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        
        # Ajouter à la liste tabou
        tabu_list.append(solution_actuelle[:])
        
        # Mise à jour de la meilleure solution
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
    
    return meilleure_solution, meilleure_distance