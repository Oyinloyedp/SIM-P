

# -*- coding: utf-8 -*-
"""

@author: Peter
"""
import random
from datetime import datetime
import numpy as np
import xlsxwriter
import csv
from dataclasses import dataclass

# create data class for Node objects
@dataclass
class Node:
    nodeID : int
    flag : int = 0
    hashRate : float = 0
    target : float = 0.0
    prob_success_trial : float = 0.0 
    prob_failure_trial : float = 0.0
    prob_success_node : float = 0.0
    prob_failure_node : float = 0.0

# NETWORK DIFFICULTY
sf=100000000
DifficultyLevel = 11890594958795.8/sf
NumberofNodes= 7
List=[13588813833966600000/sf,4726543942249240000/sf,4726543942249240000/sf,14770449819528900000/sf,4726543942249240000/sf,44311349458586600000/sf,5317361935030390000/sf]

length= len(List)
nodes = dict.fromkeys(range(1, NumberofNodes+1)) # create dict to store Node objects
for i in range(1, NumberofNodes+1):
    node = Node(i) # create Node object 
    node.hashRate= List[i-1]
    node.target = 0xFFFF * ((2**208)/DifficultyLevel)
    print("Target is", node.target)
    node.prob_success_trial = (node.target/(2**256))
    print("success Trial is", node.prob_success_trial)
    node.prob_failure_trial = 1 - node.prob_success_trial
    print("Failure Trial is", node.prob_failure_trial)
    node.prob_success_node = (1 - node.prob_failure_trial)*node.hashRate
    print("Probability of Success",node.prob_success_node)
    node.prob_failure_node = 1 - node.prob_success_node
    nodes[i] = node # add created node object to dict
    
# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('POW 25th September 2019.xlsx')
bold_format= workbook.add_format({'bold':True}) # Workbook formating.
cell_format= workbook.add_format() # Workbook formating
cell_format.set_text_wrap(True) # Workbook formating

np.random.seed(200)
numSim = 10000    # Initialize numSim 
TimeRecord = np.zeros((numSim, 1)) # Declare TimeRecord as an array
TimeRecord_average = np.zeros((numSim, 1)) # Declare TimeRecord_average as an array
open('./COVFILE.csv', 'w', newline='').close() # create file to write COV values
for sim in range(1, numSim):
    y = 0
    fork=0
    counter = 1
    while y == 0:
        
        for i in range(1, NumberofNodes+1):
            node = nodes[i] # get Node object from dict
            if np.random.random() < node.prob_success_node:     # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
                y = 1
                fork+=1
                node.flag+=1
        else:
            counter = counter + 1       # Each count is 1 second
    
    
   # Method 1: stop simulation by visual inspection
    TimeRecord[sim] = counter
    if sim > 1:
        TimeRecord_average[sim-1,0] = np.sum(TimeRecord[1:sim] / sim) # plot this to see the variation
    
    #Method 2: stop simulation by calculating the coefficient of variation; std/mean
    with open('./COV3.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if sim > 1:
        COV = np.std(TimeRecord_average[1:sim-1]) / np.mean(TimeRecord_average[1:sim-1])
            #csvwriter.writerow([COV])
        print("About to stop now",COV)
        if sim > 10000 and COV < 0.05: # 5% is good criteria for my study to stop the simulation, a lower percentage can be used, based on visual inspection of the plot above. 
            break


#Create worksheet and write to it
worksheet = workbook.add_worksheet('Node Infomation')
worksheet.write('A1' , 'Node ID', bold_format) # Write to worksheet
worksheet.write('B1' , 'Node HashRate', bold_format)
worksheet.write('C1' , 'Node Probablity of finding the right nonce',bold_format)
worksheet.write('D1' , 'Node Winnings', bold_format)

rowIndex=2  #Write to row two

    
for i in range(1, NumberofNodes+1):
    node = nodes[i]
    worksheet.write('A' + str(rowIndex), node.nodeID)
    worksheet.write('B' + str(rowIndex), node.hashRate)
    worksheet.write('C' + str(rowIndex), node.prob_success_node)
    worksheet.write('D' + str(rowIndex), node.flag)
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


workbook.close()
