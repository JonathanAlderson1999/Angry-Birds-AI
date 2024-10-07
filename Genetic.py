import copy
import random
import numpy as np
import pickle
from Game_Network import game_network

total_mutation = 0

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

def crossover_layer(layer, x, y, mutation):

    x_layer = x.network.layers[layer]
    y_layer = y.network.layers[layer]

    [weights_x, weights_y] = [len(x_layer.weights[0]), len(x_layer.weights)]
    rand = [np.random.rand(weights_x) for i in range(weights_y)]
    mutations = [np.random.uniform(-mutation / 2, mutation / 2, 2 * weights_x) for i in range(weights_y)]

    for w in range(weights_y):
        for n in range(weights_x):
            #if (rand[w][n] > 0.5):
            #   temp = x_layer.weights[w][n]
            #   x_layer.weights[w][n] = y_layer.weights[w][n]
            #   y_layer.weights[w][n] = temp

            x_layer.weights[w][n] += mutations[w][n]
            y_layer.weights[w][n] += mutations[w][n + weights_x]

        global total_mutation
        total_mutation += mutations[w][n]
        total_mutation += mutations[w][n + weights_x]

    num_biases = len(x_layer.biases)
    rand = np.random.rand(num_biases)
    mutations = np.random.uniform(-mutation / 2, mutation / 2, 2 * num_biases)

    num_biasese = len(x_layer.biases)

    for b in range(num_biasese):
        if (rand[b] > 0.5):
           temp = x_layer.biases[b]
           x_layer.biases[b] = y_layer.biases[b]
           y_layer.biases[b] = temp

        x_layer.biases[b] += mutations[b]
        y_layer.biases[b] += mutations[b + num_biasese]

    x.network.layers[layer] = x_layer
    y.network.layers[layer] = y_layer

    #print(total_mutation)

    return [x, y]

def crossover(a, b, mutation):

    # todo: faster way to do this?
    new_a = copy.deepcopy(a)
    new_b = copy.deepcopy(b)

    for i in range(len(a.network.layers)):
        [new_a, new_b] = crossover_layer(i, new_a, new_b, mutation)

    return [new_a, new_b]

def mutate(a, mutation):

    new_a = copy.deepcopy(a)

    for i in range(len(a.network.layers)):
        new_a = mutate_layer(i, new_a, mutation)

    new_a.__repr__()

    return new_a

temperature = 0.2

def select_parents(population, scores):

    population_count = len(population)
    population = [population[i] for i in range(len(population)) if scores[i] >= 0]
    scores = [score for score in scores if score >= 0]

    score_sum = sum(scores)

    if (score_sum == 0):
        score_sum = len(scores)
        scores = [1 for score in scores]

    unbiased_weighted_chance = np.repeat(1. / len(scores) , len(scores))
    biased_weighted_chance = np.array([(score / score_sum) for score in scores])
    
    global temperature
    temperature -= 0.01

    weighted_chance = unbiased_weighted_chance * temperature + biased_weighted_chance * ( 1. - temperature)

    print("\nSelecting Parents: ", str(weighted_chance))

    new_parents = np.random.choice(population, population_count, p = weighted_chance)
    
    return new_parents

def crossover_parents(parents):
    new_population = []
    num_parents = len(parents)
    mutation = np.random.rand(num_parents) * 0.1 # not sure

    for i in range(num_parents):
        parent = parents[i]
        mutated_parent = mutate(parent, mutation[i])
        new_population = new_population + [mutated_parent]

    return new_population

def make_new_population(generation, population_size):

    if (generation == 0):
        random.seed(1)
        prev_population = [game_network(random.randint(1, 10000)) for i in range(population_size)]
        scores = [1 for i in range(population_size)]
    else:
        with open("Saved_Networks/generation" + str(generation - 1) + ".pickle", "rb") as f:
            [prev_population, scores] = pickle.load(f)

    new_parents = select_parents(prev_population, scores)

    new_parents.__repr__()

    new_population = crossover_parents(new_parents)

    pickle.dump(new_population, open("Saved_Networks/generation" + str(generation) + ".pickle", "wb"))

    return new_population


#https://medium.com/@harshit158/softmax-temperature-5492e4007f71


    ## let's see if the average of any value is changing
    #average_biases = 0
    #average_weights = 0
    #for network in parents:
    #    average_biases += sum(network.network.layers[0].biases)
    #    average_weights += sum([sum(weights) for weights in network.network.layers[0].weights])
    #average_biases /= len(parents) * len(parents[0].network.layers[0].biases)
    #average_weights /= len(parents) * len(parents[0].network.layers[0].weights)
    ##print(average_biases)
    ##print(average_weights)

# Todo: actually cross over parents 
    #for i in range(num_parents // 2):

    #    rand_a = rand[i]
    #    rand_b = rand[i + (num_parents // 2)]
    #    new_population = new_population + (crossover(parents[rand[i]], parents[rand[i + (num_parents // 2)]], mutation[i]))[:]
