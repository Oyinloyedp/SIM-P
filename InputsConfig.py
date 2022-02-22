# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 20:40:37 2021

@author: Peter
"""


""" Select the simulator to be run.
     0 : Proof of Work (PoW)
    1 : Proof of Reputation X (PoRx)
    2 : Proof) of Contribution
    """
Simulator=0


''' Input configurations for PoW '''
if Simulator == 0:
        import PoW
        ''' Node Parameters '''
        NumberofNodes = 1000  # the total number of nodes in the network
   
        """ Select the Hashrate Mode.
        1 : Random Hashrate from 10^9 to 10^12
        2 : Enter Hashrate for the specified Number of Nodes
        """
        Hashrate_Mode=1
        ''' Simulation Parameters '''
        numSim = 500  # the Number of simulation (in seconds)
        
        ''' Difficulty Level Parameters '''
        DifficultyLevel = 20000  # Network Difficulty
 
    
        ''' Input configurations for Proof of Reputation X (PoRx) '''
elif Simulator==1:
    
        import PoRx
        ''' Node Parameters '''
        NumberofNodes = 21  # the total number of nodes in the network
   
        """ Select the Hashrate Mode.
        1 : Random Hashrate from 10^9 to 10^12
        2 : Enter Hashrate for the specified Number of Nodes
        """
        Hashrate_Mode=2
        
        ''' Simulation Parameters '''
        numSim = 1000000  # the Number of simulation (in seconds)
        
        ''' Global Difficulty Level  '''
        DifficultyLevel = 20000  # Network Difficulty
        
        ''' Reputation Parameters  '''
        Rep_Init= 1000  # Initial Reputation Value
        d_reward= 100
        d_decay =30
    
        """ Select your prefered reputation Mode.
        1 : Random repuation from 1000 TO 3000
        2 : Enter reputation for the specified Number of Nodes
        """
        Reputation_Mode=1       

elif Simulator==2:
    
        import PoC
        ''' Node Parameters '''
        NumberofNodes = 21  # the total number of nodes in the network
   
        """ Select the Hashrate Mode.
        1 : Random Hashrate from 10^8 to 10^15
        2 : Enter Hashrate for the specified Number of Nodes
        """
        Hashrate_Mode=2
        
        ''' Simulation Parameters '''
        numSim = 1000000  # the Number of simulation (in seconds)
        
        ''' Global Difficulty Level  '''
        DifficultyLevel = 20000  # Network Difficulty
        
        ''' Success time  '''
        """ Select your prefered success time Mode.
        1 : Random success time from 0 to 3
        2 : Enter success time for the specified Number of Nodes
        """
        successtime_Mode=1     
   