# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

# Import des algorithmes TSP
from algorithms.tsp import tabou as tsp_tabou
from algorithms.tsp import recuit_simule as tsp_recuit
from algorithms.tsp import genetique_roulette as tsp_gen_roulette
from algorithms.tsp import genetique_rang as tsp_gen_rang

# Import des algorithmes Ordonnancement
from algorithms.scheduling import tabou as sched_tabou
from algorithms.scheduling import recuit_simule as sched_recuit
from algorithms.scheduling import genetique_roulette as sched_gen_roulette
from algorithms.scheduling import genetique_rang as sched_gen_rang

app = Flask(__name__)
CORS(app)

def generer_matrice_distances(n):
    """Génère une matrice de distances aléatoire symétrique"""
    matrice = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distance = random.randint(1, 20)
            matrice[i][j] = distance
            matrice[j][i] = distance
    return matrice

def generer_durees_taches(n):
    """Génère des durées de tâches aléatoires"""
    return [random.randint(2, 10) for _ in range(n)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.json
        problem_type = data.get('problem')
        algorithm = data.get('algorithm')
        iterations = int(data.get('iterations', 100))
        crossover = data.get('crossover', 'double')

        # === TSP ===
        if problem_type == 'tsp':
            num_cities = int(data.get('cities', 15))
            matrice_distances = generer_matrice_distances(num_cities)

            solution = None
            distance = None
            fitness = None

            if algorithm == 'tabou':
                solution, distance = tsp_tabou.tabu_search(
                    matrice_distances,
                    nombre_iterations=iterations,
                    taille_tabu=min(50, num_cities * 2)
                )
            elif algorithm == 'recuit':
                solution, distance = tsp_recuit.recuit(
                    matrice_distances,
                    T_init=1000,
                    refroid=0.995,
                    nb_iter=iterations
                )
            elif algorithm == 'genetic_roulette':
                solution, distance = tsp_gen_roulette.algo_genetique_roulette(
                    matrice_distances,
                    type_croisement=crossover,
                    taille_pop=min(50, num_cities * 2),
                    nb_generations=iterations
                )
            elif algorithm == 'genetic_rank':
                solution, distance = tsp_gen_rang.algo_genetique_rang(
                    matrice_distances,
                    type_croisement=crossover,
                    taille_pop=min(50, num_cities * 2),
                    nb_generations=iterations
                )
            else:
                return jsonify({
                    'success': False,
                    'error': f"Algorithme TSP inconnu : {algorithm}"
                }), 400

            # Calcul du fitness
            if 'genetic' in algorithm and distance > 0:
                fitness = round(1 / distance * 1000, 4)

            return jsonify({
                'success': True,
                'solution': solution,
                'distance': round(distance, 2),
                'cost': round(distance, 2),
                'fitness': fitness
            })

        # === SCHEDULING ===
        else:
            num_tasks = int(data.get('tasks', 15))
            durees_taches = generer_durees_taches(num_tasks)

            solution = None
            makespan = None

            if algorithm == 'tabou':
                solution, makespan = sched_tabou.tabu_search_ordonnancement(
                    durees_taches,
                    nombre_iterations=iterations,
                    taille_tabu=min(20, num_tasks)
                )
            elif algorithm == 'recuit':
                solution, makespan = sched_recuit.recuit_ordonnancement(
                    durees_taches,
                    T_init=1000,
                    refroid=0.995,
                    nb_iter=iterations
                )
            elif algorithm == 'genetic_roulette':
                solution, makespan = sched_gen_roulette.algo_genetique_roulette(
                    durees_taches,
                    type_croisement=crossover,
                    taille_pop=min(30, num_tasks * 2),
                    nb_generations=iterations
                )
            elif algorithm == 'genetic_rank':
                solution, makespan = sched_gen_rang.algo_genetique_rang(
                    durees_taches,
                    type_croisement=crossover,
                    taille_pop=min(30, num_tasks * 2),
                    nb_generations=iterations
                )
            else:
                return jsonify({
                    'success': False,
                    'error': f"Algorithme scheduling inconnu : {algorithm}"
                }), 400

            # Calcul des positions des tâches
            task_data = []
            for i, task_id in enumerate(solution):
                task_data.append({
                    'id': task_id,
                    'duration': durees_taches[task_id],
                    'start': sum(durees_taches[solution[j]] for j in range(i)),
                    'color': f'hsl({330 + (task_id * 360 / num_tasks)}, 70%, 65%)'
                })

            return jsonify({
                'success': True,
                'solution': solution,
                'makespan': makespan,
                'tasks': task_data,
                # 'cost' supprimé ici car inutile pour scheduling
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)