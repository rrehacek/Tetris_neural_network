#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 22:18:47 2020

@author: radekrehacek
"""

import numpy as np



class NeuralNetwork():
    
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        # self.out_weights = 0.1 * np.random.randn(n_neurons, 4)
        self.out_weights = np.random.randn(n_neurons, 4)
        self.biases = np.zeros((1, n_neurons))
        self.key_outputs = [0, 0, 0, 0]
        self.score = 0
        
    
    def forward_neurons(self):
        self.neuron_outputs = np.dot(self.inputs, self.weights)


    def forward_activation_function(self):
        #Weird activation function I came up with
        # self.key_outputs = np.dot(self.neuron_outputs, self.out_weights)
        # for i, element in enumerate(self.key_outputs):
        #     self.key_outputs[i] = 1 if element > 0 else 0
        
        #ReLU activation function
        # after_activation_outputs = np.maximum(0, self.neuron_outputs)
        prev_outs = self.key_outputs
        # self.key_outputs = np.dot(after_activation_outputs, self.out_weights)
        
        
        #Sigmoidal activation function
        self.after_activation_outputs = self.sigmoid(self.neuron_outputs)
        self.key_outputs = np.dot(self.after_activation_outputs, self.out_weights)
        
        
        # if self.key_outputs[0] != prev_outs[0]:
        #     print(self.key_outputs)

            
    def sigmoid(self, s):
        # activation function
        return 1/(1+np.exp(-s))


    def read_inputs(self, grid):
        self.inputs = []
        # Create a vector out of grid and use it as an input
        for row in grid:
            for cell in row:
                # print("1" if cell != (0,0,0) else "0")
                self.inputs.append(1 if cell != (0,0,0) else -1)
           
        self.collumns_heights = [0 for _ in range(10)]
        # Read height of each collumn and use it as another 10 inputs
        for i_row, row in enumerate(grid):
            for i_cell, cell in enumerate(row):
                if cell != (0,0,0):
                    if self.collumns_heights[i_cell] == 0:
                        self.collumns_heights[i_cell] = 20-i_row
                        break
        
        self.inputs += self.collumns_heights 
                


    def get_outputs(self):
        self.out_left = self.key_outputs[0]
        self.out_down = self.key_outputs[1]
        self.out_right = self.key_outputs[2]
        self.out_rotate = self.key_outputs[3]
        return (self.out_left, self.out_down, self.out_right, self.out_rotate)

            
    def save_score(self, time, piece, level, score):
        self.time_score = time
        self.piece_score = piece
        self.level_score = level      
        self.score = score
            
            
    def get_score(self):
        return self.time_score, self.piece_score, self.level_score, self.score           
            
            