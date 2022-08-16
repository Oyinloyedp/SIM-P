# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 20:07:02 2021

@author: Peter
"""
import sys
sys.path.append("/downloads/simulator/InputsConfig")
from InputsConfig import DifficultyLevel
from InputsConfig import Hashrate_Mode
from InputsConfig import Simulator
from InputsConfig import NumberofNodes
from InputsConfig import numSim
from InputsConfig import successtime_Mode
import random
import numpy as np
import xlsxwriter
from datetime import datetime

from dataclasses import dataclass

# create data class for Node objects
@dataclass
class Node:
    nodeID : int
    flag : int = 0
    hashes : int =0
    successtime : int =0     #Success Time for each Node
    difficulty: int =0
    difficultyfactor:float=0.0
    hashRate : int = 0
    target : float = 0.0
    prob_success_trial : float = 0.0 
    prob_failure_trial : float = 0.0
    prob_success_node : float = 0.0
    prob_failure_node : float = 0.0

# NETWORK DIFFICULTY
DifficultyLevel= DifficultyLevel             #Network Difficulty
Hashrate_Mode=Hashrate_Mode
successtime_Mode=successtime_Mode
Simulator =Simulator
min=100000
max=1000000000000
List2=(range(0,3))
NumberofNodes = NumberofNodes #int(input("Enter the number of nodes:")) # Prompt to enter the number of nodes
MachinePower = int(input("Enter the power consumption of nodes in Watts:"))
if Simulator==2 :
   nodes = dict.fromkeys(range(1, NumberofNodes+1)) # create dict to store Node objects

for i in range(1, NumberofNodes+1):
    node = Node(i) # create Node object
    if Hashrate_Mode==1:
       node.hashRate = random.randrange(min,max)
    elif Hashrate_Mode==2:
        node.hashRate =int(input("Enter the hashrates for the corresponding Nodes:"))
    if successtime_Mode==1: 
        node.successtime = random.choice(List2) 
    elif successtime_Mode==2:
        node.successtime =int(input("Enter the Success time for the corresponding Nodes:"))
    if (node.successtime==0):
        node.difficultyfactor=1
    else:
        node.difficultyfactor=1/0.6+2.718**-(node.successtime+9)/10
    node.difficulty = DifficultyLevel * node.difficultyfactor**-1
    node.target = 0xFFFF * ((2**208)/node.difficulty)
    node.prob_success_trial = (node.target/(2**256))
    node.prob_failure_trial = 1 - node.prob_success_trial
    node.prob_success_node = (1 - node.prob_failure_trial)*node.hashRate
    node.prob_failure_node = 1 - node.prob_success_node
    nodes[i] = node # add created node object to dict
    
# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('1k_NODES_TEST_POC.xlsx')
bold_format= workbook.add_format({'bold':True}) # Workbook formating.
cell_format= workbook.add_format() # Workbook formating
cell_format.set_text_wrap(True) # Workbook formating

np.random.seed(200)
numSim =numSim   # Initialize numSim 
TimeRecord = np.zeros((numSim, 1)) # Declare TimeRecord as an array
TimeRecord_average = np.zeros((numSim, 1)) # Declare TimeRecord_average as an array
np.random.seed(200)
for sim in range(1, numSim):
    y = 0
    fork=0
    counter = 1
    while y == 0:
        for i in range(1, NumberofNodes+1):
            node = nodes[i] # get Node object from dict
            if np.random.random() < node.prob_success_node:   # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
                y= 1
                fork+=1
                node.successtime+=1
        else:
            counter = counter + 1       # Each count is 1 second
          
   # Method 1: stop simulation by visual inspection
    TimeRecord[sim] = counter
    if sim > 1:
        TimeRecord_average[sim-1,0] = np.sum(TimeRecord[1:sim] / sim) # plot this to see the variation

    # Method 2: stop simulation by calculating the coefficient of variation; std/mean
    if sim > 1:
        COV = np.std(TimeRecord_average[1:sim-1]) / np.mean(TimeRecord_average[1:sim-1])
        if (sim % 1000 == 0)
            print("Current COV:",COV)
        if sim > 10000 and COV < 0.05: # 5% is good criteria for my study to stop the simulation, a lower percentage can be used, based on visual inspection of the plot above. 
            break
    
    
#Create worksheet and write to it
worksheet = workbook.add_worksheet('Node Infomation')
worksheet.write('A1' , 'Node ID', bold_format) # Write to worksheet
worksheet.write('B1' , 'Node Success Time', bold_format)
worksheet.write('C1' , 'Network Difficulty', bold_format)
worksheet.write('D1' , 'Node Difficulty', bold_format)
worksheet.write('E1' , 'Node HashRate', bold_format)
worksheet.write('F1' , 'Node Probablity of finding the right nonce',bold_format)
worksheet.write('G1' , 'Difficulty Factor', bold_format)
rowIndex=2  #Write to row two

    
for i in range(1, NumberofNodes+1):
    node = nodes[i]
    worksheet.write('A' + str(rowIndex), node.nodeID)
    worksheet.write('B' + str(rowIndex), node.successtime)
    worksheet.write('C' + str(rowIndex), DifficultyLevel)
    worksheet.write('D' + str(rowIndex), node.difficulty)
    worksheet.write('E' + str(rowIndex), node.hashRate)
    worksheet.write('F' + str(rowIndex), node.prob_success_node)
    worksheet.write('G' + str(rowIndex), node.difficultyfactor)
    rowIndex+=1
    
#Add another worksheet
worksheet = workbook.add_worksheet('Average Time')
# Start from the first cell.
# Index Rows and columns as zero.
row = 0
column = 0
# iterating through content list
for item in TimeRecord_average :
    worksheet.write(row, column, item)     # write operation perform
    row += 1    # incrementing the value of row by one
                # with each iterations.

worksheet = workbook.add_worksheet('Possible Fork')
worksheet.write('A1' , 'List of Fork', bold_format) # Write to worksheet
rowIndex=2
worksheet.write('A' + str(rowIndex), fork)


workbook.close()
