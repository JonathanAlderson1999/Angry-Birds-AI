import os
import copy
import random
import numpy as np
import pickle
from Game_Network import game_network

mutation_chance = 0.01

all_time_best = 0

def mutate_layer(layer, x, mutation):

    x_layer = x.network.layers[layer]

    [weights_x, weights_y] = [len(x_layer.weights[0]), len(x_layer.weights)]
    rand = [np.random.rand(weights_x) for i in range(weights_y)]
    mutations = [np.random.uniform(-mutation / 2, mutation / 2, weights_x) for i in range(weights_y)]

    for w in range(weights_y):
        for n in range(weights_x):
            x_layer.weights[w][n] += mutations[w][n]

    num_biases = len(x_layer.biases)
    rand = np.random.rand(num_biases)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, num_biases)

    num_biasese = len(x_layer.biases)

    for b in range(num_biasese):
        x_layer.biases[b] += mutations[b]

    x.network.layers[layer] = x_layer

    return x

def crossover_layer(layer, x, y):

    x_layer = x.network.layers[layer]
    y_layer = y.network.layers[layer]

    [weights_x, weights_y] = [len(x_layer.weights[0]), len(x_layer.weights)]
    rand = [np.random.rand(weights_x) for i in range(weights_y)]

    mutated_weights = x.network.initialize_weights(weights_x)
    num_mutations = 0

    for w in range(weights_y):
        for n in range(weights_x):

            if (rand[w][n] > 0.5):
               temp = x_layer.weights[w][n]
               x_layer.weights[w][n] = y_layer.weights[w][n]
               y_layer.weights[w][n] = temp

            if (rand[w][n] > (1.0 - mutation_chance)):
                x_layer.weights[w][n] = mutated_weights[num_mutations]
                num_mutations += 1

            if (rand[w][n] < mutation_chance):
                y_layer.weights[w][n] = mutated_weights[num_mutations]
                num_mutations += 1

    x.network.layers[layer] = x_layer
    y.network.layers[layer] = y_layer

    return [x, y]

def crossover(a, b):

    # todo: faster way to do this?
    new_a = copy.deepcopy(a)
    new_b = copy.deepcopy(b)

    for i in range(len(a.network.layers)):
        [new_a, new_b] = crossover_layer(i, new_a, new_b)

    return [new_a, new_b]

def mutate(a, mutation):

    new_a = copy.deepcopy(a)

    for i in range(len(a.network.layers)):
        new_a = mutate_layer(i, new_a, mutation)

    new_a.__repr__()

    return new_a

temperature = 0.2

def select_parents(population, scores, levels_complete):
    global all_time_best

    print("\nAverage population score: ", round(sum(scores) / len(scores), 2))
    print("Average population level: ",  round(sum([len(i) for i in levels_complete]) / len(levels_complete), 2))
    print("Best: ", max(scores), "\t\tAll Time Best: ", str(all_time_best))
    all_time_best = max(all_time_best, max(scores))

    # Favour AI's which have completed levels other AI's have not
    all_completed_levels = sum(levels_complete, [])
    for i in range(len(scores)):
        for completed_level in levels_complete[i]:
            level_pass_rate = all_completed_levels.count(completed_level) / len(scores)
            bonus = 100000 * (1.0 - level_pass_rate)
            scores[i] += bonus

    for i in range(len(levels_complete)):
        scores[i] = max(scores[i], 0)

    score_sum = sum(scores)
    if (score_sum == 0):
        score_sum = len(scores)
        scores = [1 for score in scores]

    unbiased_weighted_chance = np.repeat(1. / len(scores) , len(scores))
    biased_weighted_chance = np.array([(score / score_sum) for score in scores])
    
    global temperature
    temperature -= 0.01
    temperature = max(temperature, 0)

    weighted_chance = unbiased_weighted_chance * temperature + biased_weighted_chance * ( 1. - temperature)

    new_parents = np.random.choice(population, len(population), p = weighted_chance)

    return new_parents

def crossover_parents(parents):
    new_population = []
    num_parents = len(parents)
    other_parent = np.random.choice(parents, len(parents))

    for i in range(0, num_parents - 1, 2):
        new_parents = crossover(parents[i], parents[i + 1])
        new_population = new_population + new_parents


    return new_population

def load_population(run_dir, generation, population_size, num_pigs):

    np.random.seed(generation)
    random.seed(generation)

    if (generation == 0):
        initial_population = [game_network(random.randint(1, 10000), num_pigs) for i in range(population_size)]
        random.seed(generation)
        np.random.seed(generation)

        if not os.path.exists(run_dir):
            os.mkdir(run_dir)

        pickle.dump(initial_population, open(run_dir + "generation0.pickle", "wb"))
        population = initial_population
    else:
        with open(run_dir + "generation" + str(generation) + ".pickle", "rb") as f:
            population = pickle.load(f)

    random.seed(generation)
    np.random.seed(generation)

    return population

def make_new_population(generation, population, scores, levels_complete):

    new_parents = select_parents(population, scores, levels_complete)

    new_population = crossover_parents(new_parents)

    return new_population


#https://medium.com/@harshit158/softmax-temperature-5492e4007f71
#https://www.geeksforgeeks.org/genetic-algorithms/
