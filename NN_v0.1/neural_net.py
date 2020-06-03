# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:30:59 2020

@author: Radek
"""

import numpy as np


class NeuralNetwork():
    def __init__(self):
        self.inputs = []
        
        self.neuron_left = None
        self.neuron_down = None
        self.neuron_right = None
        self.neuron_rotate = None
        
        self.weights_left = [0.10 * np.random.randn(200, 1)]
        self.weights_down = [0.10 * np.random.randn(200, 1)]
        self.weights_right = [0.10 * np.random.randn(200, 1)]
        self.weights_rotate = [0.10 * np.random.randn(200, 1)]
        
        self.out_left = None
        self.out_down = None
        self.out_right = None
        self.out_rotate = None
        
        self.bias = 0
        

    def read_inputs(self, grid):
        self.inputs = []
        for row in grid:
            for cell in row:
                # print("1" if cell != (0,0,0) else "0")
                self.inputs.append(1 if cell != (0,0,0) else -1)
        
        print("\n",self.inputs)
    
    
    def forward_neurons(self):
        self.out_left = np.dot(self.inputs, self.weights_left) + self.bias
        self.out_down = np.dot(self.inputs, self.weights_down) + self.bias
        self.out_right = np.dot(self.inputs, self.weights_right) + self.bias
        self.out_rotate = np.dot(self.inputs, self.weights_rotate) + self.bias
    
    
    def forward_activation_function(self):
        in_left = self.out_left
        in_down = self.out_down
        in_right = self.out_right
        in_rotate = self.out_rotate
        
        self.out_left = 1 if in_left > 0 else 0
        self.out_down = 1 if in_down > 0 else 0
        self.out_right = 1 if in_right > 0 else 0
        self.out_rotate = 1 if in_rotate > 0 else 0


    def get_outputs(self):
        return (self.out_left, self.out_down, self.out_right, self.out_rotate)


    
    
    
    
    
    
    
    