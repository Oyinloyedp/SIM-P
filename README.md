# SIM-P - A Simplified Consensus Protocol Simulator

This respository contains the simulation models for Proof of Work, Proof of Reputation-X and Proof of Contribution using SIM-P.

# Installation requirements

You need Python 3.0 or higher versions installed on your machine and have the following packages installed:

pandas
pip install pandas

numpy
pip install numpy

xlsxwriter
pip install xlsxwriter

# Instructions
Run the configuration file InputsConfig.py to choose the model of interest (PoW 0, PoRX 1 and PoC 2) and to set up the related parameters. The parameters include the number of nodes, difficulty, hashrate mode(you can choose to assign hashrate randomly or input specific hashrates),reputation/success time mode(you can choose to assign reputation/success time randomly or input specific reputation/success time) and block reward/penalty parameters.  

Run the selected model by running InputsConfig.py either from the command line

python InputsConfig.py

or using any Python editor such as Spyder.

# Statistics and Results

SIM-P automatically exports the average time to find a
block, number of blocks mined per node, reward and penalty to a spreadsheet. The throughput,energy consumption and resistance against 51% attack is computed.

# Contact
Feel free to contact me oyinloyedp@gmail.com
