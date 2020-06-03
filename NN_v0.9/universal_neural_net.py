#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 22:18:47 2020

@author: radekrehacek
"""

import numpy as np
import copy



class NeuralNetwork():
    
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
        
    
    def forward_neurons(self):
        self.neuron_outputs = np.dot(self.inputs, self.weights)


    def forward_activation_function(self):
        self.output = copy.deepcopy(self.neuron_outputs)
        for i, element in enumerate(self.neuron_outputs):
            self.output[i] = 1 if element > 0 else 0
            
     
    def read_inputs(self, grid):
        self.inputs = []
        for row in grid:
            for cell in row:
                # print("1" if cell != (0,0,0) else "0")
                self.inputs.append(1 if cell != (0,0,0) else -1)


    def get_outputs(self):
        self.out_left = self.output[0]
        self.out_down = self.output[1]
        self.out_right = self.output[2]
        self.out_rotate = self.output[3]
        return (self.out_left, self.out_down, self.out_right, self.out_rotate)

            
    def save_score(self, time, piece, level):
        self.time_score = time
        self.piece_score = piece
        self.level_score = level            
            
            
    def get_score(self):
        return self.time_score, self.piece_score, self.level_score            
            
            