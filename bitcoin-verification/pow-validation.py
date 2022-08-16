

# -*- coding: utf-8 -*-
"""

@author: Peter/Je Sen
"""
import random
from datetime import datetime
import numpy as np
import csv
from dataclasses import dataclass
import argparse

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

# file = input("File Name (with extension):")

errorSum = 0

parser = argparse.ArgumentParser(description='Process csv file.')
parser.add_argument('file', metavar='file/dir', type=str,
                    help='file to analyze')
args = parser.parse_args()

with open(args.file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1 #Skip header
        else:
            DifficultyLevel = float(row[0])
            Result = float(row[1])
            HashRate = float(row[2])
            print(f'Diff = {row[0]}, Hash Rate = {row[2]} Expected Result = {row[1]}.')
            line_count += 1

            #Automatically calculate scale factor
            sf = 10
            DifficultyLevel_scaled = DifficultyLevel/sf
            while (DifficultyLevel_scaled > 100000):
                sf=sf*10
                DifficultyLevel_scaled = DifficultyLevel/sf

            #Scale Difficulty and Hash Rate
            DifficultyLevel = DifficultyLevel/sf
            HashRate = HashRate/sf
                  
            node = Node(0) # create Node object 
            node.hashRate= HashRate
            node.target = 0xFFFF * ((2**208)/DifficultyLevel)
            node.prob_success_trial = (node.target/(2**256))
            node.prob_failure_trial = 1 - node.prob_success_trial
            node.prob_success_node = (1 - node.prob_failure_trial)*node.hashRate
            node.prob_failure_node = 1 - node.prob_success_node

            np.random.seed(200)
            numSim = 10000    # Initialize numSim 
            TimeRecord = np.zeros(numSim) # Declare TimeRecord as an array
            TimeRecord_average = np.zeros(numSim) # Declare TimeRecord_average as an array

            for sim in range(0, numSim):
                y = 0
                fork=0
                counter = 1
                while y == 0:
                    
                    if np.random.random() < node.prob_success_node:     # if the sampled probability is less than the ProbSuccess_Node, then the solution is considered found
                        y = 1
                        fork+=1
                        node.flag+=1

                    counter = counter + 1       # Each count is 1 second
                
                
                #Method 1: stop simulation by visual inspection
                TimeRecord[sim] = counter
                TimeRecord_average[sim] = np.sum(TimeRecord / (sim+1)) # plot this to see the variation
                COV = np.std(TimeRecord_average) / np.mean(TimeRecord_average)
                if (sim%1000==0):
                    print("Current COV and iteration",COV, sim+1)

            print("Average time = ", TimeRecord_average[sim-1]/60)
            errorSum = errorSum + abs(TimeRecord_average[sim-1]/60-Result)
            MAE = errorSum/(line_count-1)
            print("Mean Average Error = ", MAE)
            print("====")
