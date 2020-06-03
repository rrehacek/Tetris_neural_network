#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:19:42 2020

@author: radekrehacek
"""

import numpy as np

class Layer():
    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons)
    
    
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights)
    
    
    def activation_ReLU(self, inputs):
        self.output = np.maximum(0, inputs)


    def activation_sigmoid(self, inputs):
        self.output = 1/(1+np.exp(-inputs))



class NeuralNetwork():
    def __init__(self):
        self.layers = []


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
        self.out_left = self.layers[-1].output[0]
        self.out_down = self.layers[-1].output[1]
        self.out_right = self.layers[-1].output[2]
        self.out_rotate = self.layers[-1].output[3]
        return (self.out_left, self.out_down, self.out_right, self.out_rotate)

        
    def save_score(self, time, piece, level, score):
        self.time_score = time
        self.piece_score = piece
        self.level_score = level      
        self.score = score
        

    def get_score(self):
        return self.time_score, self.piece_score, self.level_score, self.score           
            
                    
        
        
        
        
        
        
        