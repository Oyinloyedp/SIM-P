

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
    nodeID: int
    flag: int = 0
    hashRate: float = 0
    target: float = 0.0
    prob_success_trial: float = 0.0
    prob_failure_trial: float = 0.0
    prob_success_node: float = 0.0
    prob_failure_node: float = 0.0


# NETWORK DIFFICULTY
sf = 10
DifficultyLevel = 2979636.61693807/sf
NumberofNodes = 5
List = [2700705241011.51/sf, 1050274260393.37/sf,3150822781180.1/sf, 12303212764608/sf, 2550666060955.32/sf]

length = len(List)
# create dict to store Node objects
nodes = dict.fromkeys(range(1, NumberofNodes+1))
for i in range(1, NumberofNodes+1):
    node = Node(i)  # create Node object
    node.hashRate = List[i-1]
    node.target = 0xFFFF * ((2**208)/DifficultyLevel)
    print("Target is", node.target)
    node.prob_success_trial = (node.target/(2**256))
    print("success Trial is", node.prob_success_trial)
    node.prob_failure_trial = 1 - node.prob_success_trial
    print("Failure Trial is", node.prob_failure_trial)
    node.prob_success_node = (1 - node.prob_failure_trial)*node.hashRate
    print("Probability of Success", node.prob_success_node)
    node.prob_failure_node = 1 - node.prob_success_node
    nodes[i] = node  # add created node object to dict

# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('POW 6th January 2013.xlsx')
bold_format = workbook.add_format({'bold': True})  # Workbook formating.
cell_format = workbook.add_format()  # Workbook formating
cell_format.set_text_wrap(True)  # Workbook formating

np.random.seed(200)
numSim = 10000    # Initialize numSim
TimeRecord = np.zeros((numSim, 1))  # Declare TimeRecord as an array
# Declare TimeRecord_average as an array
TimeRecord_average = np.zeros((numSim, 1))
# create file to write COV values
open('./COVFILE.csv', 'w', newline='').close()
for sim in range(1, numSim):
    y = 0
    fork = 0
    counter = 1
    while y == 0:

        for i in range(1, NumberofNodes+1):
            node = nodes[i]  # get Node object from dict
            # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
            if np.random.random() < node.prob_success_node:
                y = 1
                fork += 1
                node.flag += 1
        else:
            counter = counter + 1       # Each count is 1 second

   # Method 1: stop simulation by visual inspection
    TimeRecord[sim] = counter
    if sim > 1:
        # plot this to see the variation
        TimeRecord_average[sim-1, 0] = np.sum(TimeRecord[1:sim] / sim)

    # Method 2: stop simulation by calculating the coefficient of variation; std/mean
    with open('./COV3.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if sim > 1:
        COV = np.std(TimeRecord_average[1:sim-1]) / \
            np.mean(TimeRecord_average[1:sim-1])
        # csvwriter.writerow([COV])
        print("About to stop now", COV)
        # 5% is good criteria for my study to stop the simulation, a lower percentage can be used, based on visual inspection of the plot above.
        if sim > 10000 and COV < 0.05:
            break


# Create worksheet and write to it
worksheet = workbook.add_worksheet('Node Infomation')
worksheet.write('A1', 'Node ID', bold_format)  # Write to worksheet
worksheet.write('B1', 'Node HashRate', bold_format)
worksheet.write(
    'C1', 'Node Probablity of finding the right nonce', bold_format)
worksheet.write('D1', 'Node Winnings', bold_format)

rowIndex = 2  # Write to row two


for i in range(1, NumberofNodes+1):
    node = nodes[i]
    worksheet.write('A' + str(rowIndex), node.nodeID)
    worksheet.write('B' + str(rowIndex), node.hashRate)
    worksheet.write('C' + str(rowIndex), node.prob_success_node)
    worksheet.write('D' + str(rowIndex), node.flag)
    rowIndex += 1


# Add another worksheet
worksheet = workbook.add_worksheet('Average Time')
# Start from the first cell.
# Index Rows and columns as zero.
row = 0
column = 0
# iterating through content list
for item in TimeRecord_average:
    worksheet.write(row, column, item)     # write operation perform
    row += 1    # incrementing the value of row by one
    # with each iterations.


workbook.close()
