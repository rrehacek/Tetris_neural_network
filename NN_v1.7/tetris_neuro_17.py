# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:18:10 2020

@author: Radek
"""

import pygame
import random
from universal_neural_net import NeuralNetwork
from evolution_algo import EvolutionAlgorithm
import time

 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....', 
      '.....', 
      '..00.', 
      '.00..', 
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
 
class Piece(object):
    rows = 20  # y
    columns = 10  # x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3
 
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 
 
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions
 
 
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 
 
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
 
def get_shape():
    global shapes, shape_colors
 
    return Piece(5, 0, random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
 
 
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines
 
 
def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    score = 0
    level = 0
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            level += 1
            score += 400
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return score, level
 
 
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))
 
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
 
def draw_window(surface):
    surface.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()
 

def draw_neural_net(win, grid, net, activation_treshold):
    
    #Get grid inputs
    # inputs = []
    # for row in grid:
    #     for cell in row:
    #         inputs.append(1 if cell != (0,0,0) else 0)
    
    # after_activation_outputs = net.after_activation_outputs
    outputs = net.get_outputs()
    
    win_height = win.get_height()
    win_width = win.get_width()
    
    #From 10 to "(win_width/2)-300"
    x_start_point = 10
    x_end_point = (win_width/2)-300
    
    y_start_point = 10
    y_end_point = win_height-10
    
    h = y_end_point - y_start_point
    
    #Height of one square (input)
    y_scale = int(h/len(net.inputs))
    
    
    #Height of one square (input)
    out_y_scale = int(h/len(outputs))/5
    space_between = 10
    
    
    for index, inp in enumerate(net.inputs):
        if inp == 1:
            color = (0,255,0)
        elif inp > 1 and inp < 5:
            color = (150,255,0)
        elif inp > 4 and inp < 10:
            color = (150,255,150)
        elif inp > 9 and inp < 15:
            color = (255,255,150)
        elif inp > 14 and inp < 30:
            color = (255,255,255)
        else:
            color = (70,70,70)
        
        if index > 199:
            scaler = 7
        else:
            scaler = 0
        
        pygame.draw.rect(win, color, [ x_start_point, ((h - len(net.inputs)*y_scale)/2)+(y_scale*index),y_scale+scaler, y_scale])
    
    
    for index, out in enumerate(outputs):
        if out > activation_treshold:
            color = (0,255,0)
        else:
            color = (70,70,70)
         
        pygame.draw.rect(win, color, [ x_end_point, ((h - (len(outputs)*y_scale))/2)+((out_y_scale+space_between)*index), out_y_scale, out_y_scale])
     
    
    

    
def main(win, net):
    global grid
 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    
    activation_treshold = 0.2
    score_of_fallen_pieces = 0
    level = 0
    score = 0
   
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    
    start_time = time.time()
    
    while run:
        fall_speed = 0.01
 
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
                score_of_fallen_pieces += 1
                score += 100

            
        #Neural network code
        
        #Get input vector (each cell as an input)
        net.read_inputs(grid)
        net.forward_neurons()
        net.forward_activation_function()
        nn_key_outputs = net.get_outputs()
        

        if nn_key_outputs[0] > activation_treshold:
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
        
        if nn_key_outputs[1] > activation_treshold:
            while valid_space(current_piece, grid):
                current_piece.y += 1
            current_piece.y -= 1
            
        if nn_key_outputs[2] > activation_treshold:
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
         
        if nn_key_outputs[3] > activation_treshold:
            current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
            if not valid_space(current_piece, grid):
                current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                net.get_weights()
                pygame.display.quit()
                quit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
 
                if event.key == pygame.K_SPACE:
                   while valid_space(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
                   # print(convert_shape_format(current_piece)) # todo fix
                   
                if event.key == pygame.K_r:
                    run = False
                    
                if event.key == pygame.K_q:
                    evolution.final_results()
                    
                if event.key == pygame.K_t:
                    run = False
                    evolution.terminate = True
                    
                if event.key == pygame.K_p:
                    pause = True
                    while pause == True:
                        for ev in pygame.event.get():
                            if ev.type == pygame.KEYDOWN:
                                if ev.key == pygame.K_p:
                                    pause = False
 
        shape_pos = convert_shape_format(current_piece)
 
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
 
            # call four times to check for multiple clear rows
            sc, lvl = clear_rows(grid, locked_positions)
            score += sc
            level += lvl
 
        draw_window(win)
        draw_next_shape(next_piece, win)
        draw_neural_net(win, grid, net, activation_treshold)
        pygame.display.update()
 
        # Check if user lost
        if check_lost(locked_positions):
            run = False


 
    score_time_elapsed = time.time() - start_time
    
    
    print(f"Score: {score}, pieces: {score_of_fallen_pieces}, ", end="", flush=True)
    print(f"level: {level}")
    
    win.fill((0,0,0))
    draw_text_middle("You lost", 60, (255, 255, 255), win)
    pygame.display.update()
    pygame.event.pump()     #For some reasont without this line it does not update
    pygame.time.delay(100)
    
    
    if level > 0:
        pass
    
    net.save_score(score_time_elapsed, score_of_fallen_pieces, level, score)
    return net



def play_tetris(net):
    
    win.fill((0,0,0))
    draw_text_middle('Let the game begin', 60, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(100)
    net = main(win, net)
                

#-----------------------------------------------------------------------------
 
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')



evolution = EvolutionAlgorithm()

evolution.number_of_agents = 10

evolution.number_of_generations = 5

evolution.number_of_neurons = 10

evolution.populate_list_of_neural_nets()



for generation in range(evolution.number_of_generations):
    
    print(f"\n---------- Current generation: {generation+1} -----------\n")
    
    #Let them play one by one
    for index, net in enumerate(evolution.list_of_neural_nets):
        print(f"{index+1}.agent, ", end="", flush=True)
        play_tetris(net)
        if evolution.terminate == True:
            break

    
    if evolution.terminate == True:
        break
    
    evolution.save_last_generation()
    
    evolution.choose_the_best_agent()

    evolution.crossover()
    
    evolution.mutate()
    

        
    
evolution.final_results()


#To run agent again from previous generation
#play_tetris(evolution.list_of_all_generations[0][1])




    














