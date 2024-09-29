import random
import numpy as np
import pickle
from Game_Network import game_network

def crossover_layer(layer, x, y, mutation):

    x_layer = x.network.layers[layer]
    y_layer = y.network.layers[layer]

    num_weights = len(x_layer.weights)
    num_biasese = len(x_layer.biases)

    rand = np.random.rand(num_biasese)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_weights)

    for w in range(num_weights):
        if (rand[w] > 0.5):
           temp = x_layer.weights[w]
           x_layer.weights[w] = y_layer.weights[w]
           y_layer.weights[w] = temp

        x_layer.weights[w] += mutations[w]
        y_layer.weights[w] += mutations[w + num_biasese]

    rand = np.random.rand(num_biasese)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_biasese)

    for b in range(num_biasese):
        if (rand[b] > 0.5):
           temp = x_layer.biases[b]
           x_layer.biases[b] = y_layer.biases[b]
           y_layer.biases[b] = temp

        x_layer.biases[b] += mutations[b]
        y_layer.biases[b] += mutations[b + num_biasese]

    x.network.layers[layer] = x_layer
    y.network.layers[layer] = y_layer
    return [x, y]

def crossover(a, b, mutation):

    for i in range(len(a.network.layers)):
        [a,b] = crossover_layer(i, a, b, mutation)

    return [a, b]

def select_parents(population, scores):

    score_sum = sum(scores)

    weighted_chance = np.array([(score / score_sum) for score in scores])

    new_parents = np.random.choice(population, len(population), p = weighted_chance)
    
    return new_parents


def crossover_parents(parents):

    # Bug: The same input network produces the same crossover in the end. . .

    new_population = []

    num_parents = len(parents)

    np.random.seed(1465)

    rand = np.random.randint(num_parents, size = 2 * num_parents)
    mutation = np.random.rand(num_parents)
    j = 0

    for i in range(num_parents // 2):

        rand_a = rand[i]
        rand_b = rand[i + (num_parents // 2)]
        new_population = new_population + (crossover(parents[rand[i]], parents[rand[i + (num_parents // 2)]], mutation[i]))[:]

    return new_population



ai_id = 13

population = np.array([game_network(ai_id + i) for i in range(10)])
scores =     [0, 15000, 15000, 0, 0, 0, 0, 0, 0, 0]

parents = select_parents(population, scores)

new_population = crossover_parents(parents)

generation = 0
pickle.dump(new_population, open("Saved_Networks/generation" + str(generation) + ".pickle", "wb"))

print("Saved generation " + str(generation))