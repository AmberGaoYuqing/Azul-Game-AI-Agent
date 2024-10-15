import time, random
from copy import deepcopy
from collections import deque
import heapq

from Azul.azul_model import AzulGameRule as GameRule

THINKTIME   = 0.9
NUM_PLAYERS = 2

# Defines this agent.
class myAgent():
    def __init__(self, _id):
        self.id = _id 
        self.game_rule = GameRule(NUM_PLAYERS) 

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)
    
    def DoAction(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)
        
        if action == "ENDROUND": return (False, float('-inf'))
        return self.GainScores(state, self.id, action)
        

    # Take a list of actions and an initial state, and perform breadth-first search within a time limit.
    # Return the first action that leads to goal, if any was found.
    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        queue = deque([ (deepcopy(rootstate),[]) ]) # Initialise queue. First node = root state and an empty path.
        
        # Conduct BFS starting from rootstate.
        while len(queue) and time.time()-start_time < THINKTIME:
            state, path = queue.popleft() # Pop the next node (state, path) in the queue.
            new_actions = self.GetActions(state) # Obtain new actions available to the agent in this state.
            
            for a in new_actions: # Then, for each of these actions...
                next_state = deepcopy(state)              
                next_path  = path + [a]                   
                goal, _ = self.DoAction(next_state, a) # Carry out this action on the state and check if the goal is reached
                if goal:
                    return next_path[0]  # If a goal is reached, return the first action leading to it
                queue.append((next_state, next_path)) # Otherwise, keep exploring
        
        return random.choice(actions) # If no goal was found in the time limit, return a random action.

    def GainScores(self, state, agent_id, action):
        # In this BFS version, we're not considering any scoring heuristics, just checking if a goal state is reached.
        if action == "ENDROUND": return (False, float('-inf'))
        return (True, 0)  # Return goal reached as True for simplicity since no scoring is considered.
