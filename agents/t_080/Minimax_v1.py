from copy import deepcopy

from template import Agent, GameRule
import random
from Azul.azul_model import AzulGameRule as GameRule
import time

NUM_PLAYERS = 2
THINKTIME = 0.9



class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.game_rule = GameRule(NUM_PLAYERS)
       

    def SelectAction(self, actions, game_state):
        """
        Iterative deepening search to gradually increase the minimax search depth.
        """
        start_time = time.time()  # Record start time
        best_action = random.choice(actions)  # # Choose a default random action
        depth = 1   # Start with depth 1 and gradually increase

        while True:
            if time.time() - start_time > THINKTIME:
                break  

            try:
                # Run minimax at the given depth
                best_action, _ = self.minimax(game_state, depth, -float('inf'), float('inf'), True, start_time)
                depth += 1  # Increase search depth
            except TimeoutError:
                break # Stop search if timeout occurs

        return best_action

    def minimax(self, state, depth, alpha, beta, maximizingPlayer, start_time):
        """
        Minimax with time limit.
        """
        # Check if the time limit has been reached
        if time.time() - start_time > THINKTIME:
            raise TimeoutError 

        # Termination condition: depth is 0 or game is finished
        if depth == 0 or not state.TilesRemaining():
            return None, self.evaluate_score(state)

        actions = self.game_rule.getLegalActions(state, self.id if maximizingPlayer else 1 - self.id)

        if maximizingPlayer:
            max_eval = -float('inf')
            best_action = random.choice(actions) # Initialize the best action

            for action in actions:
                new_state = self.game_rule.generateSuccessor(deepcopy(state), action, self.id)

                _, eval = self.minimax(new_state, depth - 1, alpha, beta, False, start_time)

                if eval > max_eval:
                    max_eval = eval
                    best_action = action

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta pruning

            return best_action, max_eval

        else:
            min_eval = float('inf')
            best_action = random.choice(actions)  # Initialize the best action

            for action in actions:
                new_state = self.game_rule.generateSuccessor(deepcopy(state), action, 1 - self.id)

                _, eval = self.minimax(new_state, depth - 1, alpha, beta, True, start_time)

                if eval < min_eval:
                    min_eval = eval
                    best_action = action

                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha pruning

            return best_action, min_eval

    def evaluate_score(self, state):
        player_id = self.id
        opponent_id = 1 if self.id == 0 else 0

        # Actual score difference
        actual_score_diff = self.get_actual_score(state, player_id) - self.get_actual_score(state, opponent_id)
        
        # Incomplete line penalty difference
        incomplete_line_penalty_diff = self.get_incomplete_line_penalty(state, player_id) - self.get_incomplete_line_penalty(state, opponent_id)
    
        # Pattern score difference
        pattern_score_diff = self.get_pattern_score(state, player_id) - self.get_pattern_score(state, opponent_id)
    
        # Total score is the sum of actual score difference, incomplete line penalty difference, and pattern score difference
        total_score = (
            actual_score_diff
            - incomplete_line_penalty_diff
            + pattern_score_diff
        )

        return total_score

    # Calculate the actual score of a player
    def get_actual_score(self, state, player_id):
        return state.agents[player_id].ScoreRound()[0] + state.agents[player_id].EndOfGameScore()
    
    # Calculate the incomplete line penalty of a player
    def get_incomplete_line_penalty(self, state, player_id):
        penalty = 0
        line_weights = [5, 4, 3, 2, 1]  
        for i in range(5):
            if state.agents[player_id].lines_number[i] != i + 1:
                penalty += line_weights[i]
        return penalty
    
    # Calculate the pattern score of a player
    def get_pattern_score(self, state, player_id):
        score = 0
        for row in state.agents[player_id].grid_state:
            if all(row): 
                score += 2  # Bonus for completing a row
        for col in range(len(state.agents[player_id].grid_state[0])):
            if all(state.agents[player_id].grid_state[row][col] != 0 for row in range(5)):
                score += 7  # Bonus for completing a column
        return score


    def evaluate_score(self, state):
        player_id = self.id
        opponent_id = 1 if self.id == 0 else 0
        
        actual_score_diff = self.get_actual_score(state, player_id) - self.get_actual_score(state, opponent_id)
     
        pattern_score_diff = self.get_pattern_score(state, player_id) - self.get_pattern_score(state, opponent_id)
       
        adjacent_tile_bonus_diff = self.get_adjacent_tile_bonus(state, player_id) - self.get_adjacent_tile_bonus(state, opponent_id)
        
        incomplete_line_penalty_diff = self.get_incomplete_line_penalty(state, player_id) - self.get_incomplete_line_penalty(state, opponent_id)
        
        floor_penalty_diff = self.get_floor_penalty(state, player_id) - self.get_floor_penalty(state, opponent_id)

        # Final score calculation
        total_score = (
            actual_score_diff
            + pattern_score_diff
            + adjacent_tile_bonus_diff
            - incomplete_line_penalty_diff
            - floor_penalty_diff
        )

        return total_score


    # Calculate pattern line score
    def get_pattern_line_score(self, state, player_id):
        score = 0
        pattern_lines = state.agents[player_id].lines_number
        line_bonus = [100, 75, 50] 
        for i in range(len(pattern_lines)):
            if pattern_lines[i] == i + 1:  
                if i < 3:  
                    score += line_bonus[i]
                else:
                    score += 25  
        return score

    # Calculate floor score
    def get_floor_penalty(self, state, player_id):
        penalty = 0
        floor_tiles = state.agents[player_id].floor
        for i in range(len(floor_tiles)):
            if floor_tiles[i] != 0:
                penalty +=(i + 1) 
        return penalty

    # Calculate column score
    def get_column_score(self, state, player_id):
        column_score =  [0] * 5
        for col in range(5):
            for row in range(5):
                if state.agents[player_id].grid_state[row][col] != 0:
                    column_score[col] += 1
        return sum(i + 7 for i in column_score)  

    # Calculate row score
    def get_row_score(self, state, player_id):
        row_score =  [0] * 5
        for row in range(5):
            for col in range(5):
                if state.agents[player_id].grid_state[row][col] != 0:
                    row_score[row] += 1
        return sum(i + 2 for i in row_score) 

    # Calculate adjacent tile bonus
    def get_adjacent_tile_bonus(self, state, player_id):
        bonus = 0
        grid = state.agents[player_id].grid_state
        for row in range(5):
            for col in range(5):
                if grid[row][col] != 0:
                    adjacent_count = 0
                    if row > 0 and grid[row - 1][col] != 0:
                        adjacent_count += 1
                    if row < 4 and grid[row + 1][col] != 0:
                        adjacent_count += 1
                    if col > 0 and grid[row][col - 1] != 0:
                        adjacent_count += 1
                    if col < 4 and grid[row][col + 1] != 0:
                        adjacent_count += 1
                    bonus += adjacent_count * 3  
        return bonus

    # Calculate the pattern score of a player
    def get_pattern_score(self, state, player_id):
        return ( 
            self.get_column_score(state, player_id)
            + self.get_pattern_line_score(state, player_id)
            + self.get_row_score(state, player_id)
        )

    # Calculate the actual score of a player
    def get_actual_score(self, state, player_id):
        return state.agents[player_id].ScoreRound()[0] + state.agents[player_id].EndOfGameScore()

    # Calculate the score difference between two players
    def get_incomplete_line_penalty(self, state, player_id):
        penalty = 0
        line_weights = [5, 4, 3, 2, 1]  
        for i in range(5):
            if state.agents[player_id].lines_number[i] != i + 1:
                penalty += line_weights[i] 
        return penalty
    
