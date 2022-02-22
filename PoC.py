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

List=[100000000,10000000000,100000000000,1000000000000,10000000000000,100000000000000,255000000000000,98000000000000,49000000000000,160000000000000,23000000000000,200000000000000,5000000000000,23000000000000,43000000000000,55000000000000,59000000000000,54000000000000,52000000000000,53000000000000,51000000000000,39000000000000,38000000000000,36000000000000,35000000000000,34000000000000,32000000000000,67000000000000,63000000000000,69000000000000,61000000000000,2550000000000000,980000000000000,490000000000000,1600000000000000,230000000000000,2000000000000000,50000000000000,230000000000000,430000000000000,550000000000000,590000000000000,540000000000000,520000000000000,530000000000000,510000000000000,390000000000000,380000000000000,360000000000000,350000000000000,340000000000000,320000000000000,670000000000000,630000000000000,690000000000000,610000000000000,25500000000000,9800000000000,4900000000000,16000000000000,2300000000000,20000000000000,500000000000,2300000000000,4300000000000,5500000000000,5900000000000,5400000000000,5200000000000,5300000000000,5100000000000,3900000000000,3800000000000,3600000000000,3500000000000,3400000000000,3200000000000,6700000000000,6300000000000,6900000000000,6100000000000 ]
List2=(range(0,3))
NumberofNodes = NumberofNodes #int(input("Enter the number of nodes:")) # Prompt to enter the number of nodes
MachinePower = int(input("Enter the power consumption of nodes in Watts:"))
if Simulator==2 :
   nodes = dict.fromkeys(range(1, NumberofNodes+1)) # create dict to store Node objects

for i in range(1, NumberofNodes+1):
    node = Node(i) # create Node object
    if Hashrate_Mode==1:
       node.hashrate = random.choice(List)
    elif Hashrate_Mode==2:
        node.hashrate =int(input("Enter the hashrates for the corresponding Nodes:"))
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
    node.prob_success_node = 1 - node.prob_failure_trial**node.hashrate
    print(node.prob_success_node)
    node.prob_failure_node = 1 - node.prob_success_node
    nodes[i] = node # add created node object to dict
    
# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('21nodes51percentPOC.xlsx')
bold_format= workbook.add_format({'bold':True}) # Workbook formating.
cell_format= workbook.add_format() # Workbook formating
cell_format.set_text_wrap(True) # Workbook formating

numSim =numSim   # Initialize numSim 
TimeRecord = np.zeros((numSim, 1)) # Declare TimeRecord as an array
TimeRecord_average = np.zeros((numSim, 1)) # Declare TimeRecord_average as an array

for sim in range(1, numSim):
    y = 0
    fork=0
    counter = 1
    while y == 0:
        RandomNumber = np.random.random_sample()    # generate random numbers
        print("Random Number is ",RandomNumber)
        for i in range(1, NumberofNodes+1):
            node = nodes[i] # get Node object from dict
            if RandomNumber < node.prob_success_node:     # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
                y= 1
                fork+=1
                node.successtime+=1
                print("solution found", node.prob_success_node)
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
        if sim > 500 and COV < 0.05: # 5% is good criteria for my study to stop the simulation, a lower percentage can be used, based on visual inspection of the plot above. 
            break

#Power comsumption Calculation
powerconsumption = ((MachinePower * NumberofNodes) * counter)/10000
totalhashrate=0
for ele in range(0, len(List)):
    totalhashrate = totalhashrate + List[ele]
    
    
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
    worksheet.write('E' + str(rowIndex), node.hashrate)
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

worksheet = workbook.add_worksheet('Power Consumption')
worksheet.write('A1' , 'Total Network Hashrate', bold_format) # Write to worksheet
worksheet.write('B1' , 'Estimated Power Consumption', bold_format)
rowIndex=2
worksheet.write('A' + str(rowIndex), totalhashrate)
worksheet.write('B' + str(rowIndex), powerconsumption)

workbook.close()
