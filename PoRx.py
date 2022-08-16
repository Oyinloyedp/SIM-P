# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 19:12:05 2021

@author: Peter
"""
import sys
sys.path.append("/downloads/simulator/InputsConfig")
from InputsConfig import DifficultyLevel
from InputsConfig import Hashrate_Mode
from InputsConfig import Simulator
from InputsConfig import NumberofNodes
from InputsConfig import numSim
from InputsConfig import Rep_Init
from InputsConfig import d_reward
from InputsConfig import d_decay
from InputsConfig import Reputation_Mode
import random
import numpy as np
from datetime import datetime
import xlsxwriter
from dataclasses import dataclass

# create data class for Node objects
@dataclass
class Node:
    nodeID : int
    flag : int = 0
    hashRate : int = 0
    Difficulty: int =0
    R:int = 0               #Nodes Reputation Score
    E_reward: float=0.0
    E_decay: float=0.0
    prob_success_trial : float = 0.0 
    prob_failure_trial : float = 0.0
    prob_success_node : float = 0.0
    prob_failure_node : float = 0.0


DifficultyLevel = DifficultyLevel             #Network Difficulty
Rep_Init=Rep_Init
d_reward= d_reward
d_decay =d_decay
Hashrate_Mode=Hashrate_Mode
Reputation_Mode=Reputation_Mode
Simulator =Simulator
Rep_Max=4000
NumberofNodes = NumberofNodes #int(input("Enter the number of nodes:")) # Prompt to enter the number of nodes
min=100000
max=1000000000000
if Simulator==1 :
   nodes = dict.fromkeys(range(1, NumberofNodes+1)) # create dict to store Node objects
for i in range(1, NumberofNodes+1):
    node = Node(i) # create Node object
    if Hashrate_Mode==1:
       node.hashRate = random.randrange(min,max)
    elif Hashrate_Mode==2:
        node.hashRate =int(input("Enter the hashrates for the corresponding Nodes:"))
    if Reputation_Mode==1: 
        node.R = random.randrange(1000,4000) 
    elif Reputation_Mode==2:
        node.R =int(input("Enter the Reputation for the corresponding Nodes:"))
    if  node.R<=Rep_Init:
        node.Difficulty = DifficultyLevel+((Rep_Init-node.R)/Rep_Init) * (DifficultyLevel/3.3333)
    else:
        node.Difficulty = DifficultyLevel-((node.R- Rep_Init)/Rep_Init) * (DifficultyLevel/3.3333)
    node.target = 0xFFFF * ((2**208)/node.Difficulty)
    node.prob_success_trial = (node.target/(2**256))
    print("Target is :", node.target)
    node.prob_failure_trial = 1 - node.prob_success_trial
    node.prob_success_node = (1 - node.prob_failure_trial)*node.hashRate
    node.prob_failure_node = 1 - node.prob_success_node
    nodes[i] = node # add created node object to dict
    
    # Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('21_NODES_51PERCENT_PORX.xlsx')
bold_format= workbook.add_format({'bold':True}) # Workbook formating.
cell_format= workbook.add_format() # Workbook formating
cell_format.set_text_wrap(True) # Workbook formating

np.random.seed(200)
numSim =numSim   # Initialize numSim 
TimeRecord = np.zeros((numSim, 1)) # Declare TimeRecord as an array
TimeRecord_average = np.zeros((numSim, 1)) # Declare TimeRecord_average as an array

fork=0
c_reward=24
c_durarion=12
s_reward=60
s_decay=2
c_decay=36
d=10
block=0

for sim in range(1, numSim):
    y = 0
    counter = 1
    while y == 0:    
        for i in range(1, NumberofNodes):
            node = nodes[i] # get Node object from dict
            if np.random.random() < node.prob_success_node:     # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
                y = 1
                node.flag+=1
                fork = 1
                block+=1
                #Reward and reward decay
            if (block % 100 ==0):
                node.E_reward = node.flag/((c_reward/c_durarion)*(node.R/Rep_Max)*s_reward)
                if node.E_reward>1:
                    node.E_reward=1
                else:
                    node.R=node.R+(1-node.E_reward)*(Rep_Max-node.R)/d
                    
                #Penalty
            if (block % 100 ==0):
                node.E_decay=node.flag/((c_decay/c_durarion)*(node.R/Rep_Max)*s_decay)
                if node.E_decay>1:
                    node.E_decay=1
                else:
                    node.R=node.R-(1-node.E_decay) *node.R/d
            if node.R>=Rep_Max and node.flag==4:
                node.R=node.R/2
                #print("solution found", node.prob_success_node)
                  
        else:
            counter = counter + 1       # Each count is 1 second


    # Method 1: stop simulation by visual inspection
    TimeRecord[sim] = counter
    if sim > 1:
        TimeRecord_average[sim-1,0] = np.sum(TimeRecord[1:sim] / sim) # plot this to see the variation

    # Method 2: stop simulation by calculating the coefficient of variation; std/mean
    if sim > 1:
        COV = np.std(TimeRecord_average[1:sim-1]) / np.mean(TimeRecord_average[1:sim-1])
        if (sim % 1000 == 0):
            print("Current COV:",COV)
        if sim > 10000 and COV < 0.05: # 5% is good criteria for my study to stop the simulation, a lower percentage can be used, based on visual inspection of the plot above. 
            break

#Create worksheet and write to it
worksheet = workbook.add_worksheet('Node Infomation')
worksheet.write('A1' , 'Node ID', bold_format) # Write to worksheet
worksheet.write('B1' , 'Node HashRate', bold_format)
worksheet.write('C1' , 'Node Probablity of finding the right nonce',bold_format)
worksheet.write('D1' , 'Node Reputation', bold_format)
worksheet.write('F1' , 'Node Winnings', bold_format)

rowIndex=2  #Write to row two
 
for i in range(1, NumberofNodes+1):
    node = nodes[i]
    worksheet.write('A' + str(rowIndex), node.nodeID)
    worksheet.write('B' + str(rowIndex), node.hashRate)
    worksheet.write('C' + str(rowIndex), node.prob_success_node)
    worksheet.write('D' + str(rowIndex), node.R)
    worksheet.write('F' + str(rowIndex), node.flag)
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
Fork=0
worksheet = workbook.add_worksheet('Fork')
worksheet.write('A1' , 'List of Fork', bold_format) # Write to worksheet
rowIndex=2
worksheet.write('A' + str(rowIndex), fork)

workbook.close()
    
    
