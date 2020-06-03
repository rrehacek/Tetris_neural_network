#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:52:42 2020

@author: radekrehacek
"""

from neural_network import Layer, NeuralNetwork

grid = [[(255,0,0) for n in range(10)] for i in range(20)]


net = NeuralNetwork()

net.read_inputs(grid)

#Layer(inputs, neurons)
layer1 = Layer(210, 10)
layer2 = Layer(10, 10)
layer3 = Layer(10, 4)

net.layers.append(layer1)
net.layers.append(layer2)
net.layers.append(layer3)

layer1.forward(net.inputs)
layer1.activation_sigmoid(layer1.output)


print(layer1.output)
print()


layer2.forward(layer1.output)
layer2.activation_sigmoid(layer2.output)


print(layer2.output)
print()


layer3.forward(layer2.output)
layer3.activation_sigmoid(layer3.output)



print(layer3.output)
print(net.layers[-1].output)
