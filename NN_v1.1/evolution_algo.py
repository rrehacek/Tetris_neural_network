#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:33:53 2020

@author: radekrehacek
"""

from universal_neural_net import NeuralNetwork
import copy
import numpy as np
import random


class EvolutionAlgorithm():
    def __init__(self):
        self.number_of_agents = None
        self.number_of_generations = None
        self.number_of_neurons = None
        
        self.sorted_by_level = None
        self.sorted_by_pieces = None
        
        self.new_generation = None
        
        self.list_of_neural_nets = []
        self.list_of_all_generations = []
    
    
    def populate_list_of_neural_nets(self):
        for _ in range(self.number_of_agents):
            self.list_of_neural_nets.append(NeuralNetwork(200, self.number_of_neurons))
    
    
    def save_last_generation(self):
        self.list_of_all_generations.append(self.list_of_neural_nets)
        
        #Create new generation according to score
        self.new_generation = []
    
    
    def sort_results(self):
        #Sort by number of levels and add to new generation
        self.sorted_by_level = sorted(self.list_of_neural_nets, key=lambda x: x.level_score, reverse=True)
        
        #Sort by number of pieces and add to new generation
        self.sorted_by_pieces = sorted(self.list_of_neural_nets, key=lambda x: x.piece_score, reverse=True)
    
    
    def choose_the_best_agent(self):
        #Take the best agent who passed at least one level    
        if self.sorted_by_level[0].level_score > 0:
            self.new_generation.append(self.sorted_by_level[0])
            
            
            if self.sorted_by_level[1].level_score > 0:
                self.new_generation.append(self.sorted_by_level[1])
                
            else:
                self.new_generation.append(self.sorted_by_pieces[1])
                
        
        #Otherwise take the best agent who gained the most pieces
        else: 
            self.new_generation.append(self.sorted_by_pieces[0])
            self.new_generation.append(self.sorted_by_pieces[1])
    
        
    def populate_missing_agents(self):
            
        #Create new agent and mutate its weights
        try:
            new_agent_0 = copy.deepcopy(self.new_generation[0])
            new_agent_1 = copy.deepcopy(self.new_generation[1])
        except Exception as exception:
            print(f"Exception occured: {exception}")
            print(f"New agent had to be created.")
        
        self.new_generation.append(new_agent_0)
        self.new_generation.append(new_agent_1)
    
    
    def crossover(self):
        #Introduce crossover
        while len(self.new_generation) < self.number_of_agents:
            
            new_agent = NeuralNetwork(200, self.number_of_neurons)
            
            random_place_in_genom = random.randint(1, 199)
            
            #Copy certain part of all weights from parent i and the rest from parent i+1
            new_agent.weights = np.concatenate((self.new_generation[0].weights[:random_place_in_genom], \
                                                     self.new_generation[1].weights[random_place_in_genom:]))
        
            self.new_generation.append(new_agent)
            
        print(f"Number of agents for next generation: {len(self.list_of_neural_nets)}")
        
        self.list_of_neural_nets = []
        self.list_of_neural_nets = self.new_generation
    
    
    def mutate(self):
        #Introduce mutation
        for i, agent in enumerate(self.new_generation):
            
            #Skip first two agents because they are the copy from previous generation
            if not i < 2 and i % 2 == 2:
                agent.weights += 0.001 * np.random.randn(200, 1)
                    

        
    def final_results(self):
        #Summarize overal results
        print("\n\n-------------- Final results --------------")
        print("\nScore pieces:")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"\n{i}.generation: ", end="", flush=True)
            for agent in generation:
                print(agent.get_score()[-2], end=", ", flush=True)
        
        
        print("\n\nScore levels:")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"\n{i}.generation: ", end="", flush=True)
            for agent in generation:
                print(agent.get_score()[-1], end=", ", flush=True)
        
        
        print("\n\n\nAverage piece score per generation:\n")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"{i}.generation: ", end="", flush=True)
            
            sum_of_piece_score = 0
            
            for agent in generation:
                sum_of_piece_score += agent.get_score()[-2]
                
            print(sum_of_piece_score/len(generation))
        
        
        print("\n\nAverage level score per generation:\n")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"{i}.generation: ", end="", flush=True)
            
            sum_of_level_score = 0
            
            for agent in generation:
                sum_of_level_score += agent.get_score()[-1]
                
            print(sum_of_level_score/len(generation))


        
        
