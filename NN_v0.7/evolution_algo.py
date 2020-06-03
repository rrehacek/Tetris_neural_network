#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:33:53 2020

@author: radekrehacek
"""

from neural_net import NeuralNetwork
import copy
import numpy as np


class EvolutionAlgorithm():
    def __init__(self):
        self.number_of_agents = None
        self.number_of_generations = None
        
        self.sorted_by_level = None
        self.sorted_by_pieces = None
        
        self.new_generation = None
        
        self.list_of_neural_nets = []
        self.list_of_all_generations = []
    
    
    def populate_list_of_neural_nets(self):
        for _ in range(self.number_of_agents):
            self.list_of_neural_nets.append(NeuralNetwork())
    
    
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
        
        #Otherwise take the best agent who gained the most pieces
        else: 
            self.new_generation.append(self.sorted_by_pieces[0])
    
        
    def populate_missing_agents(self):
        #To fulfill the capacity of list, duplicate current best agent
        #and add as new agents
        while len(self.new_generation) < int(self.number_of_agents/2):
            
            #Create new agent and mutate its weights
            try:
                new_agent = copy.deepcopy(self.new_generation[0])
            except Exception as exception:
                new_agent = NeuralNetwork()
                print(f"Exception occured: {exception}")
                print(f"New agent had to be created.")
            
            self.new_generation.append(new_agent)
        
        self.list_of_neural_nets = []
        self.list_of_neural_nets = self.new_generation
    
    
    def mutate(self):
        #Introduce mutation
        for agent in self.list_of_neural_nets:
            agent.weights_left += 0.001 * np.random.randn(200, 1)
            agent.weights_down += 0.001 * np.random.randn(200, 1)
            agent.weights_right += 0.001 * np.random.randn(200, 1)
            agent.weights_rotate += 0.001 * np.random.randn(200, 1)
    
    
    def crossover(self):
        #Introduce crossover
        i = 0
        while len(self.new_generation) < self.number_of_agents:
            
            new_agent = NeuralNetwork()
            
            #Copy half of all weights from parent i and parent i+1
            new_agent.weights_left = np.concatenate((self.list_of_neural_nets[i].weights_left[:int(len(self.list_of_neural_nets[i].weights_left)/2)], \
                                                     self.list_of_neural_nets[i+1].weights_left[int(len(self.list_of_neural_nets[i+1].weights_left)/2):]))
        
            new_agent.weights_down = np.concatenate((self.list_of_neural_nets[i].weights_down[:int(len(self.list_of_neural_nets[i].weights_down)/2)], \
                                                     self.list_of_neural_nets[i+1].weights_down[int(len(self.list_of_neural_nets[i+1].weights_down)/2):]))
        
            new_agent.weights_right = np.concatenate((self.list_of_neural_nets[i].weights_right[:int(len(self.list_of_neural_nets[i].weights_right)/2)], \
                                                      self.list_of_neural_nets[i+1].weights_right[int(len(self.list_of_neural_nets[i+1].weights_right)/2):]))
        
            new_agent.weights_rotate = np.concatenate((self.list_of_neural_nets[i].weights_rotate[:int(len(self.list_of_neural_nets[i].weights_rotate)/2)], \
                                                       self.list_of_neural_nets[i+1].weights_rotate[int(len(self.list_of_neural_nets[i+1].weights_rotate)/2):]))
            
            self.new_generation.append(new_agent)
            
            i += 1
        
        print(f"Number of agents for next generation: {len(self.list_of_neural_nets)}")

        
    def final_results(self):
        #Summarize overal results
        print("\n\n-------------- Final results --------------")
        print("\nScore levels:")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"\n{i}.generation: ", end="", flush=True)
            for agent in generation:
                print(agent.get_score()[-2], end=", ", flush=True)
                
        print("\n\nScore pieces:")
        for i, generation in enumerate(self.list_of_all_generations):
            print(f"\n{i}.generation: ", end="", flush=True)
            for agent in generation:
                print(agent.get_score()[-1], end=", ", flush=True)


        
        
