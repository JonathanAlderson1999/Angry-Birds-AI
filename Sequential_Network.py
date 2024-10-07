import math
import random
import numpy as np

def relu(x):
    return max(0, x)

def tanh(x):
    return math.tanh(x)

class layer:

    weights     = []
    biases      = []
    activations = []
    dimension   = [0, 0]

    use_relu = True

    # conv2DTranspose
    kernels = []

    def input(self, input_x, input_y, relu = True):
        self.type = "input"

        self.weights = []
        self.biases = []
        self.dimension = [input_x, input_y]
        self.use_relu = relu

    def __repr__(self):

        out = ""
        
        show_hash = False

        if show_hash:
            out += " w: "
            for weights in self.weights:
                out += str(hash("".join([str(i) for i in (weights.tolist())])))

            out += " b: "
            out += str(hash("".join([str(i) for i in (self.biases.tolist())])))

        else:
            out += "b: "
            out += ",  ".join([f"{str(round(b, 1)):<6s}" for b in self.biases])

            out += "        w: "
            for weights in self.weights:
                out += ",  ".join([f"{str(round(w, 1)):<6s}" for w in weights])
                out += "        "

        return out

    def dense(self, network, input_x, input_y, output_x, output_y, relu = False):
        
        self.type = "dense"
        num_input_nodes  = input_x  * input_y
        num_dense_nodes = output_x * output_y

        self.weights   = ([network.initialize_weights(num_input_nodes) for j in range(num_dense_nodes)])
        self.biases = (np.zeros(num_dense_nodes))
        self.dimension = [output_x, output_y]
        self.use_relu = relu

    def conv2DTranspose(self, prev_layer, kernel_size, stride):

        self.type = "conv2DTranspose"
        prev_x = prev_layer.dimension[0]
        prev_y = prev_layer.dimension[1]
    
        self.kernels = [np.random.rand(kernel_size * kernel_size) for i in range(prev_x * prev_y)]
        self.kernel_size = kernel_size
        self.stride = stride
        self.biases = np.random.random(prev_x * prev_y)
        self.dimension = [prev_x * stride, prev_y * stride]

    def conv2D(self, prev_layer, num_kernels, kernel_size, stride):

        self.type = "conv2D"
    
        self.kernels = [np.random.rand(kernel_size * kernel_size) for i in range(num_kernels)]
        self.biases = np.random.random(num_kernels)
        self.kernel_size = kernel_size
        self.stride = stride
        self.dimension = [num_kernels, 1]

    def feed_forward(self, input, dimension):

        num_neurons = len(self.biases)
        biases  = self.biases

        if (self.type == "input"):
            self.activations = input

        if (self.type == "dense"):
            weights = self.weights
            if self.use_relu:  
                self.activations = np.array([tanh(relu(np.sum(input * weights[j]) - biases[j])) for j in range(num_neurons)])
            else:
                self.activations = np.array([tanh((np.sum(input * weights[j]) - biases[j])) for j in range(num_neurons)])

        elif (self.type == "conv2DTranspose"):
            kernels = self.kernels

            activations = [np.zeros(dimension[0] * self.stride) for i in range(dimension[1] * self.stride)]

            # TODO: We don't want to be multiplying single elements like a fool
            # when we could be making use of np's vectorized multiplications.
            # I'll come back when training is slow.

            for input_y in range(dimension[1]):
                for input_x in range(dimension[0]):

                    neuron_id = (input_y * dimension[0]) + input_x

                    for kernel_x in range(self.kernel_size):
                        for kernel_y in range(self.kernel_size):

                            x_layer_kernel = input_x * self.stride + kernel_x
                            y_layer_kernel = input_y * self.stride + kernel_y

                            activations[y_layer_kernal][x_layer_kernal] += input[neuron_id] * kernels[neuron_id][(kernel_y * self.kernel_size) + kernel_x]

            self.activations = np.concatenate(activations)

        elif (self.type == "conv2D"):
            kernels = self.kernels

            activations = np.zeros(len(kernels))

            # TODO: This is so slow it's pretty unbelievable 

            # Instead of padding with zeros, 
            # just don't iterate where the kernel won't fit
            # no branches no problem

            half_kernel_stride = (self.kernel_size // 2) * self.stride

            for k in range(len(kernels)):
                print(k)
                for input_y in range(half_kernel_stride, dimension[1] - half_kernel_stride, self.stride):
                    for input_x in range(half_kernel_stride, dimension[0] - half_kernel_stride, self.stride):
                        for kernel_x in range(self.kernel_size):
                            for kernel_y in range(self.kernel_size):

                                x_input_kernel = input_x + (kernel_x - (self.kernel_size // 2)) * self.stride
                                y_input_kernel = input_y + (kernel_y - (self.kernel_size // 2)) * self.stride
                    
                                x_y_input_kernel = (y_input_kernel * dimension[0]) + x_input_kernel
                                
                                activations[k] += input[x_y_input_kernel] * kernels[k][kernel_y * self.kernel_size + kernel_x]

            activations = np.zeros(len(kernels))

            #for kernel_id in range(len(kernels)):


class sequential_network:

    def __init__(self, num_input_neurons):

        self.layers = []
        self.num_input_neurons = num_input_neurons

    def __str__(self):

       return "".join([self.format(layer) for layer in self.layers])

    def __repr__(self):

        out = ""
        for layer in self.layers:
            out += layer.__repr__()

        return out

    def format(self, layer):

        out = ("Layer: " + str(len(layer[0])) + " : " + str(len(layer)))
        out += "\n"

        for y in layer:
            for x in y:
                out += ("%6.2f " % x)
            out += "\n"

        out += "\n"
        
        return out

    # he method
    def initialize_weights(self, num_values):
        variance = 2 / self.num_input_neurons
        return np.array([-variance + random.random() * 2 * variance for value in range(num_values)])

    def input(self, dimension):

        new_layer = layer()
        new_layer.input(dimension[0], dimension[1])
        self.layers.append(new_layer)

    def dense(self, input_x, input_y, output_x, output_y, relu = False):

        new_layer = layer()
        new_layer.dense(self, input_x, input_y, output_x, output_y, relu)
        self.layers.append(new_layer)

    def conv2DTranspose(self, kernel_size, stride):

        prev_layer = self.layers[-1]
        new_layer = layer()
        new_layer.conv2DTranspose(prev_layer, kernel_size, stride)
        self.layers.append(new_layer)

    def conv2D(self, num_kernels, kernel_size, stride):

        prev_layer = self.layers[-1]
        new_layer = layer()
        new_layer.conv2D(prev_layer, num_kernels, kernel_size, stride)
        self.layers.append(new_layer)

    def feed_forward(self, input, dim_x, dim_y):

        # for each neruon in the 'next' layer
        #   for each neuron in the 'current' layer
        #       multiply the neuron by the nth weight of the 'next' neuron
        #   subract the 'next' neurons bias
        #   run through relu activation function

        prev_activations = input
        prev_dimension = [dim_x, dim_y]

        for i in range(len(self.layers)):


            self.layers[i].feed_forward(prev_activations, prev_dimension)

            prev_activations = self.layers[i].activations
            prev_dimension = self.layers[i - 1].dimension

        # final tanh
        for activation in self.layers[-1].activations:
            activation = tanh(activation)

        return (self.layers[-1])

# https://medium.com/@sanjay_dutta/understanding-glorot-and-he-initialization-a-guide-for-college-students-00f3dfae0393