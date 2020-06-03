#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:33:53 2020

@author: radekrehacek
"""

from neural_network import Layer, NeuralNetwork
import copy
import numpy as np
import random


class EvolutionAlgorithm():
    def __init__(self):
        self.number_of_agents = None
        self.number_of_generations = None
        
        self.sorted_by_level = None
        self.sorted_by_pieces = None
        
        self.new_generation = None
        
        self.list_of_neural_nets = []
        self.list_of_all_generations = []
        
        self.terminate = False
    
    
    def populate_list_of_neural_nets(self):
        for _ in range(self.number_of_agents):
            
            net = NeuralNetwork()
            
            layer1 = Layer(210, 10)
            layer2 = Layer(10, 10)
            layer3 = Layer(10, 4)

            net.layers.append(layer1)
            net.layers.append(layer2)
            net.layers.append(layer3)
            
            self.list_of_neural_nets.append(net)
            
    
    
    def save_last_generation(self):
        self.list_of_all_generations.append(self.list_of_neural_nets)
        
        #Create new generation according to score
        self.new_generation = []
    
    
    def choose_the_best_agent(self):
        #Sort by score
        self.sorted_by_score = sorted(self.list_of_neural_nets, key=lambda x: x.score, reverse=True)
        
        #Take the best agent who passed at least one level        
        self.new_generation.append(copy.deepcopy(self.sorted_by_score[0]))
        self.new_generation.append(copy.deepcopy(self.sorted_by_score[1]))
    
    
    def crossover(self):
        #Introduce crossover
        while len(self.new_generation) < self.number_of_agents:
            
            net = NeuralNetwork()
            
            layer1 = Layer(210, 10)
            layer2 = Layer(10, 10)
            layer3 = Layer(10, 4)

            net.layers.append(layer1)
            net.layers.append(layer2)
            net.layers.append(layer3)
            
            # Crossover weights from each layer two nets
            for i, layer in enumerate(net.layers):
                random_place_in_genom = random.randint(1, len(layer.weights)-1)
                layer.weights = np.concatenate((self.new_generation[0].layers[i].weights[:random_place_in_genom], \
                                                self.new_generation[1].layers[i].weights[random_place_in_genom:]))
                
            self.new_generation.append(copy.deepcopy(net))
            
            
        print(f"\nNumber of agents for next generation: {len(self.list_of_neural_nets)}")
        
        self.list_of_neural_nets = []
        self.list_of_neural_nets = copy.deepcopy(self.new_generation)
    
    
    def mutate(self):
        #Introduce mutation
        for i, agent in enumerate(self.new_generation):
            
            #Skip first two agents because they are the copy from previous generation
            for i_l, layer in enumerate(agent.layers):
                if not i < 2 and i % 2 == 0:
                    agent.layers[i_l].weights += 0.05 * np.random.randn(len(agent.layers[i_l].weights), 1)
            

        
    def final_results(self):
        #Summarize overal results
        if self.terminate == True:
            print("\n\n----------- TERMINATED -----------")
        print("\n\n-------------- Results --------------")
        print("\nScore pieces:")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"\n{i+1}.generation: ", end="", flush=True)
            for agent in generation:
                print(agent.get_score()[-3], end=", ", flush=True)
        
        
        print("\n\n\nScore levels:")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"\n{i+1}.generation: ", end="", flush=True)
            for agent in generation:
                print(agent.get_score()[-2], end=", ", flush=True)
        
        
        print("\n\n\nAverage piece score per generation:\n")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"{i+1}.generation: ", end="", flush=True)
            
            sum_of_piece_score = 0
            
            for agent in generation:
                sum_of_piece_score += agent.get_score()[-3]
                
            print(sum_of_piece_score/len(generation))
        
        
        print("\n\nAverage level score per generation:\n")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"{i+1}.generation: ", end="", flush=True)
            
            sum_of_level_score = 0
            
            for agent in generation:
                sum_of_level_score += agent.get_score()[-2]
                
            print(sum_of_level_score/len(generation))


        
        
