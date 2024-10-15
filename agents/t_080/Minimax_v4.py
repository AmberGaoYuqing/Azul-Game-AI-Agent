import time, random, math
from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy

NUM_PLAYERS = 2
THINKTIME = 0.9


class myAgent():
    def __init__(self, _id):
        super().__init__()
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS)

    def SelectAction(self, actions, game_state):
        """
        Iterative deepening search to gradually increase the minimax search depth.
        """
        start_time = time.time()  # Record start time
        best_action = random.choice(actions)  # Default random action
        depth = 1  # Start with depth 1 and gradually increase

        while True:
            if time.time() - start_time > THINKTIME:
                break  # Break if the time limit is exceeded

            try:
                # Run minimax at the given depth
                best_action, _ = self.minimax(game_state, depth, -float('inf'), float('inf'), True, start_time)
                depth += 1  # Increase search depth
            except TimeoutError:
                break  # Stop search if timeout occurs

        return best_action

    def _get_best_actions(self, game_state):
        """
        Get the ordered actions based on desirability.
        """
        actions = self.game_rule.getLegalActions(game_state, self.id)
        action_dict = {}

        for action in actions:
            # Validate the action before using it
            tg = action.tile_grab if hasattr(action, 'tile_grab') else None
            if not tg:
                continue

            tile_type = tg.tile_type
            num_to_pattern_line = tg.num_to_pattern_line
            pattern_line_dest = tg.pattern_line_dest
            num_to_floor_line = tg.num_to_floor_line

            # Skip actions that don't place tiles on a pattern line
            if pattern_line_dest == -1:
                continue

            desirability = num_to_pattern_line - num_to_floor_line

            # Save the more desirable action
            if (tile_type, pattern_line_dest) not in action_dict or desirability > action_dict[(tile_type, pattern_line_dest)][0]:
                action_dict[(tile_type, pattern_line_dest)] = (desirability, action)

        # Return sorted actions by desirability
        sorted_actions = [val[1] for _, val in sorted(action_dict.items(), reverse=True, key=lambda x: x[1][0])]
        return sorted_actions if sorted_actions else actions

    def minimax(self, state, depth, alpha, beta, maximizingPlayer, start_time):
        """
        Minimax algorithm with alpha-beta pruning and a time limit.
        """
        if time.time() - start_time > THINKTIME:
            raise TimeoutError  # Raise timeout error if time exceeds

        # Termination condition: depth is 0 or no tiles remain
        if depth == 0 or not state.TilesRemaining():
            return None, self.evaluate_score(state)

        actions = self._get_best_actions(state)

        if maximizingPlayer:
            max_eval = -float('inf')
            best_action = random.choice(actions)  # Initialize best action

            for action in actions:
                # Validate action using the game rules
                try:
                    new_state = self.game_rule.generateSuccessor(deepcopy(state), action, self.id)
                except AssertionError:
                    continue  # Skip invalid actions

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
            best_action = random.choice(actions)  # Initialize best action

            for action in actions:
                try:
                    new_state = self.game_rule.generateSuccessor(deepcopy(state), action, 1 - self.id)
                except AssertionError:
                    continue  # Skip invalid actions

                _, eval = self.minimax(new_state, depth - 1, alpha, beta, True, start_time)

                if eval < min_eval:
                    min_eval = eval
                    best_action = action

                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha pruning

            return best_action, min_eval

    def evaluate_score(self, state):
        """
        Comprehensive evaluation of the game state.
        """
        player_id = self.id
        opponent_id = 1 if self.id == 0 else 0

        # Calculate score difference
        actual_score_diff = self.get_actual_score(state, player_id) - self.get_actual_score(state, opponent_id)
        
        # Calculate incomplete pattern line penalty difference
        incomplete_line_penalty_diff = self.get_incomplete_line_penalty(state, player_id) - self.get_incomplete_line_penalty(state, opponent_id)
    
        # Calculate pattern score difference
        pattern_score_diff = self.get_pattern_score(state, player_id) - self.get_pattern_score(state, opponent_id)

        # Calculate unfilled pattern line penalty difference
        unfilled_diff = self.deduct_unfilled_pattern_line(state, player_id) - self.deduct_unfilled_pattern_line(state, opponent_id)
    
        # Total score calculation
        total_score = (
            actual_score_diff
            + pattern_score_diff
            + unfilled_diff
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

    def deduct_unfilled_pattern_line(self, state, player_id):
        """
        Deduct points for unfilled pattern lines.
        """
        score = 0  
        count = 0  
        for i in range(len(state.agents[player_id].lines_number)):
            if state.agents[player_id].lines_number[i] != i + 1:
                count += 1
        score -= count * count  # Penalty for the number of unfilled lines, squared for severity
        return score
