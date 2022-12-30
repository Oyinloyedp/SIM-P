# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 20:07:02 2021

@author: Peter
"""

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
    P_cbt : float = 0.0    #Power contribution of nodes    
    prob_success_trial : float = 0.0 
    prob_failure_trial : float = 0.0
    prob_success_node :  float = 0.0
    prob_failure_node :  float = 0.0
    Panel_No: float =0.0
    C_f: float =0.0
    token: float =0.0
    Target: float =0.0          #Network Target


Difficulty= 20000
E_cpn = 7.986     #Energy consumption of nodes in watts-minutes
C_bm = 20         #Network benchmark score

NumberofNodes = int(input("Enter the number of nodes:")) # Prompt to enter the number of nodes
min=1
max=50
# nodes = dict.fromkeys(range(1, NumberofNodes+1)) # create dict to store Node objects
nodes = []

for i in range(NumberofNodes):
    node = Node(i) # create Node object
    node.Panel_No = int(input("Enter the number of panels:"))
    #random.randrange(min,max)
    node.P_cbt = node.Panel_No * 6.616
    node.C_f = node.P_cbt/E_cpn *100
    if node.C_f > C_bm:  
          node.Target = (2**256/Difficulty)
          #0xFFFF *((2**208)/Difficulty)
          node.prob_success_trial = (node.Target/(2**256))
          node.prob_failure_trial = 1 - node.prob_success_trial
          node.prob_success_node = 1 - node.prob_failure_trial**node.P_cbt
          node.prob_failure_node = 1 - node.prob_success_node
        #   nodes[i] = node # add created node object to dict 
          nodes.append(node)
        
# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('poCp_51percent.xlsx')
bold_format= workbook.add_format({'bold':True}) # Workbook formating.
cell_format= workbook.add_format() # Workbook formating
cell_format.set_text_wrap(True) # Workbook formating

clock=0
day=0
night=0
numSim =10000   # Initialize numSim 
TimeRecord = np.zeros((numSim, 1)) # Declare TimeRecord as an array
TimeRecord_average = np.zeros((numSim, 1)) # Declare TimeRecord_average as an array

          
for sim in range(1, numSim):
    # y = 0
    fork=0
    counter = 1
    # while y == 0:
    for node in nodes:
        # node = nodes[i] # get Node object from dict
        # if node.prob_success_node is not None:
        if np.random.random() < node.prob_success_node:   # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
            # y= 1
            node.flag+=1
            fork+=1
            node.token+=5 
    else:
        counter = counter + 1       # Each count is 1 second
       
   # Method 1: stop simulation by visual inspection
    TimeRecord[sim] = counter
    if sim > 1:
        TimeRecord_average[sim-1,0] = np.sum(TimeRecord[1:sim] / sim) # plot this to see the variation

    # Method 2: stop simulation by calculating the coefficient of variation; std/mean
    if sim > 1:
        COV = np.std(TimeRecord_average[1:sim-1]) / np.mean(TimeRecord_average[1:sim-1])
        print("About to stop now",COV)
        if sim > 10000 and COV < 0.05: # 5% is good criteria for my study to stop the simulation, a lower percentage can be used, based on visual inspection of the plot above. 
            break
    
    
#Create worksheet and write to it
worksheet = workbook.add_worksheet('Node Infomation')
worksheet.write('A1' , 'Node ID', bold_format) # Write to worksheet
worksheet.write('B1' , 'Node Energy Contribution', bold_format)
worksheet.write('C1' , 'Node Energy Consumption', bold_format)
worksheet.write('D1' , 'Network Difficulty', bold_format)
worksheet.write('E1' , 'Node Probablity of finding the right nonce',bold_format)
worksheet.write('F1' , 'Node winnings', bold_format)
worksheet.write('G1' , 'Token Reward', bold_format)
worksheet.write('H1' , 'Numbers of Panel', bold_format)
rowIndex=2  #Write to row two

    
for node in nodes:
    # node = nodes[i]
    worksheet.write('A' + str(rowIndex), node.nodeID)
    worksheet.write('B' + str(rowIndex), node.P_cbt)
    worksheet.write('C' + str(rowIndex), E_cpn)
    worksheet.write('D' + str(rowIndex), Difficulty)
    worksheet.write('E' + str(rowIndex), node.prob_success_node)
    worksheet.write('F' + str(rowIndex), node.flag)
    worksheet.write('G' + str(rowIndex), node.token)
    worksheet.write('H' + str(rowIndex), node.Panel_No)
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
    
