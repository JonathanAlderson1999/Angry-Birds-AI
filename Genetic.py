import random
import numpy as np
import pickle
from Game_Network import game_network

def crossover_layer(x, y, mutation):

    num_weights = len(x.weights)
    num_biasese = len(x.biases)

    rand = np.random.rand(num_biasese)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_weights)

    for w in range(num_weights):
        if (rand[w] > 0.5):
           temp = x.weights[w]
           x.weights[w] = y.weights[w]
           y.weights[w] = temp

        x.weights[w] += mutations[w]
        y.weights[w] += mutations[w + num_biasese]

    rand = np.random.rand(num_biasese)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_biasese)

    for b in range(num_biasese):
        if (rand[b] > 0.5):
           temp = x.biases[b]
           x.biases[b] = y.biases[b]
           y.biases[b] = temp

        x.biases[b] += mutations[b]
        y.biases[b] += mutations[b + num_biasese]

def crossover(a, b, mutation):

    for i in range(len(a.network.layers)):
        crossover_layer(a.network.layers[i], b.network.layers[i], mutation)

    return [a, b]

def select_parents(population, scores):

    score_sum = sum(scores)

    weighted_chance = np.array([(score / score_sum) for score in scores])

    new_parents = np.random.choice(population, len(population), p = weighted_chance)
    
    return new_parents


def crossover_parents(parents):

    new_population = []

    num_parents = len(parents)

    rand = np.random.randint(num_parents, size = num_parents)
    mutation = np.random.rand(num_parents)
    j = 0

    for i in range(num_parents // 2):

        new_population = new_population + (crossover(parents[rand[j]], parents[rand[j + 1]], mutation[i]))[:]
        j += 2



ai_id = 13

population = np.array([game_network(ai_id + i) for i in range(10)])
scores =     [0, 15000, 15000, 0, 0, 0, 0, 0, 0, 0]

parents = select_parents(population, scores)

new_population = crossover_parents(parents)

generation = 0
pickle.dump(new_population, open("Saved_Networks/generation" + str(generation) + ".pickle", "wb"))

print("Saved generation " + str(generation))