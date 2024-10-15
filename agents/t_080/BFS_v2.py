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
        

    def SelectAction(self, actions, rootstate):
        start_time = time.time()
        selected_actions = []
        queue = deque([ (deepcopy(rootstate),[]) ]) # Initialise queue. First node = root state and an empty path.
        
        # Conduct BFS starting from rootstate.
        while len(queue) and time.time()-start_time < THINKTIME:
            state, path = queue.popleft() # Pop the next node (state, path) in the queue.
            new_actions = self.GetActions(state) # Obtain new actions available to the agent in this state.
            
            for a in new_actions: # Then, for each of these actions...
                next_state = deepcopy(state)              
                next_path  = path + [a]                   
                goal, gain = self.DoAction(next_state, a) # Carry out this action on the state and check if the goal is reached
                if goal:
                    return next_path[0]  # If a goal is reached, return the first action leading to it
                heapq.heappush(selected_actions, (-gain, id(next_path[0]), next_path[0])) # Track the best action by score

                queue.append((next_state, next_path)) # Otherwise, keep exploring
        
        if len(selected_actions): return heapq.heappop(selected_actions)[2] # Return the best action found
        return random.choice(actions) # If no goal was found in the time limit, return a random action.



    def GainScores(self, state, agent_id, action):
        # Compute the score based on the player's state after performing an action
        if action == "ENDROUND": return (False, float('-inf'))

        plr_state = state.agents[agent_id]
        wall = deepcopy(plr_state.grid_state)
        gain =  self.CalculateRoundScore(plr_state, wall)
        
        goal_reached = (gain > 0)  # Treat positive score gain as reaching a goal
        return (goal_reached, gain)

    def CalculateRoundScore(self, player_state, player_wall):
        """
        Calculate the round score for the player based on their wall state and penalties.
        Takes into account penalties for unfilled pattern lines, floor penalties, 
        and bonuses for contiguous tiles on the player's wall.
        """
        score = 0
        
        def deduct_unfilled_pattern_line(player_state):
            """
            Deduct points for unfilled pattern lines. The 
            more unfilled lines, the higher the penalty.
            """
            score = 0
            count = 0
            for i in range(len(player_state.lines_number)):
                if player_state.lines_number[i] != i + 1:
                    count += 1
            score -= count * count  # Penalty for the number of unfilled lines, squared for severity
            return score

        def floor_penalty(player_state):
            """
            Calculate the penalty for tiles placed on the floor.
            """
            penalties = 0
            for i in range(len(player_state.floor)):
                penalties += player_state.floor[i] * player_state.FLOOR_SCORES[i] 
            return penalties

        def get_pattern_score(player_state):
            score = 0
            for row in player_state.grid_state:
                if all(row): 
                    score += 2  # Bonus for completing a row
            for col in range(len(player_state.grid_state[0])):
                if all(player_state.grid_state[row][col] != 0 for row in range(5)):
                    score += 7  # Bonus for completing a column
            return score

        # Add the neighbor score, unfilled pattern line penalty, and floor penalty to the total score
        score += deduct_unfilled_pattern_line(player_state)
        score += floor_penalty(player_state)
        score += get_pattern_score(player_state)
        score += player_state.ScoreRound()[0]  # Round score from game mechanics
        score += player_state.EndOfGameScore()  # End of game score from game mechanics

        return score
