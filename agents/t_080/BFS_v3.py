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
        selected_actions = []
        goal_in_ture = False
        queue = deque([ (deepcopy(rootstate),[]) ]) # Initialise queue. First node = root state and an empty path.
        
        # Conduct BFS starting from rootstate.
        while len(queue) and time.time()-start_time < THINKTIME:
            state, path = queue.popleft() # Pop the next node (state, path) in the queue.
            new_actions = self.GetActions(state) # Obtain new actions available to the agent in this state.
            
            for a in new_actions: # Then, for each of these actions...
                next_state = deepcopy(state)              
                next_path  = path + [a]                   
                goal, gain = self.DoAction(next_state, a) # Carry out this action on the state, return goal_reached, score gained
                if goal:
                    # If the current action reached the goal, record the initial action & sort by negate gain (gain always > 0)
                    heapq.heappush(selected_actions, (-gain, TieBreaker(), next_path[0]))
                    goal_in_ture = True
                else:
                    queue.append((next_state, next_path))
                    # if can't fill a full line, choose action that lowest the lost
                    heapq.heappush(selected_actions, (0, TieBreaker(-gain), next_path[0]))
            if goal_in_ture: break   # If a goal was found in this turn, stop searching.

        if len(selected_actions): return heapq.heappop(selected_actions)[2]
        return random.choice(actions) # If no goal was found in the time limit, return a random action.
        

    def GainScores(self, state, agent_id, action):
        if action == "ENDROUND": return (False, float('-inf'))
        _, _, tg = action
        if tg.pattern_line_dest+1 != tg.number:
            goal_reached = False

        plr_state = state.agents[agent_id]
        wall = deepcopy(plr_state.grid_state)
        gain =  self.CalculateRoundScore(plr_state, wall)

        goal_reached = (gain > 0)
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
        score += player_state.ScoreRound()[0] # Round score from game mechanics
        score += player_state.EndOfGameScore() # End of game score from game mechanics

        return score 



class TieBreaker:
    def __init__(self, key=None):
        self.key = key
        self.timestamp = time.time()  

    def __lt__(self, other):
        if self.key is None or other.key is None:
            return False
        if self.key == other.key:
            return self.timestamp < other.timestamp
        return self.key < other.key

    def __eq__(self, other):
        if self.key is None or other.key is None:
            return False
        return self.key == other.key and self.timestamp == other.timestamp

    def __str__(self):
        return f"{self.key} at {self.timestamp:.6f}"