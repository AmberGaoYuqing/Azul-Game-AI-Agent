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
    
        # Pattern score difference
        pattern_score_diff = self.get_pattern_score(state, player_id) - self.get_pattern_score(state, opponent_id)

        unfilled_diff = self.deduct_unfilled_pattern_line(state, player_id) - self.deduct_unfilled_pattern_line(state, opponent_id) 

        # Centre reword difference
        centre_diff = self.centre_score(state, player_id) - self.centre_score(state, opponent_id)
    
        # Total score is the sum of actual score difference, incomplete line penalty difference, and pattern score difference
        total_score = (
            actual_score_diff
            + pattern_score_diff
            + unfilled_diff
            + centre_diff
        )

        return total_score

    # Calculate the actual score of a player
    def get_actual_score(self, state, player_id):
        return state.agents[player_id].ScoreRound()[0] + state.agents[player_id].EndOfGameScore()
    
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

    def deduct_unfilled_pattern_line(self, state, player_id):
        """
        Deduct points for unfilled pattern lines. The 
        more unfilled lines, the higher the penalty.
        """
        score = 0  
        count = 0  
        for i in range(len(state.agents[player_id].lines_number)):
            if state.agents[player_id].lines_number[i] != i + 1:
                count += 1
        score -= count * count  # Penalty for the number of unfilled lines, squared for severity
        return score

    def centre_score(self, state, id):
        score = 0
        agent_state = state.agents[id]
        for x in range(0,5):
            for y in range(0,5):
                if x == 2 and y == 2:
                    if agent_state.grid_state[x][y] == 1:
                        score += 2
                elif x > 0 and x < 4 and y > 0 and y < 4:
                    if agent_state.grid_state[x][y] == 1:
                        score += 1
        return score