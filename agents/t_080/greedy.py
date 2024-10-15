from Azul.azul_model import AzulGameRule as GameRule
from copy import deepcopy

THINKTIME = 0.9
NUM_PLAYERS = 2

class myAgent():
    def __init__(self, _id):
        self.id = _id
        self.game_rule = GameRule(NUM_PLAYERS)

    def GetActions(self, state):
        """
        Get all legal actions for the agent given the current game state.
        """
        return self.game_rule.getLegalActions(state, self.id)
    
    def DoAction(self, state, action):
        """
        Apply an action to the state, modifying the state in-place.
        """
        self.game_rule.generateSuccessor(state, action, self.id)
    
    def SelectAction(self, actions, game_state):
        """
        Select the best action to perform from a list of actions.
        """
        return self.get_best_action(game_state, self.id)

    def get_best_action(self, state, id):
        """
        Determine the best action by simulating each possible action and 
        evaluating its outcome based on the calculated score.
        """
        actions = self.game_rule.getLegalActions(state, id)
        best_reward = -float('inf')
        best_action = None

        for action in actions:
            next_state = deepcopy(state)
            self.game_rule.generateSuccessor(next_state, action, id)
            reward = self.CalculateRoundScore(next_state, next_state.agents[id].grid_state, id)
            if reward > best_reward:
                best_reward = reward
                best_action = action

        return best_action if best_action else random.choice(actions)

    def CalculateRoundScore(self, next_state, player_wall, id):
        """
        Calculate the score for the player based on the current state of their wall,
        applying penalties for unfilled pattern lines and calculating bonus scores.
        """
        score = 0

        player_state = next_state.agents[id]

        def deduct_unfilled_pattern_line(player_state):
            """
            Deduct points for any unfilled pattern lines on the player's wall.
            The penalty increases quadratically with the number of unfilled lines.
            """
            count = 0
        
            for i in range(len(player_state.lines_number)):
                if player_state.lines_number[i] != i + 1:
                    count += 1
            return -count*count  # Penalty is squared for each unfilled line

        def floor_penalty(player_state):
            """
            Calculate penalties based on tiles placed on the floor line,
            which typically incurs negative points.
            """
            penalties = 0
            for i in range(len(player_state.floor)):
                penalties += player_state.floor[i] * player_state.FLOOR_SCORES[i]
            return penalties

        def center_score(player_state):
            score = 0
            for x in range(0,5):
                for y in range(0,5):
                    if x == 2 and y == 2:
                        if player_state.grid_state[x][y] == 1:
                            score += 2
                    elif x > 0 and x < 4 and y > 0 and y < 4:
                        if player_state.grid_state[x][y] == 1:
                            score += 1
            return score

        def get_pattern_score(player_state):
            score = 0
            for row in player_state.grid_state:
                if all(row): 
                    score += 2  # Bonus for completing a row
            for col in range(len(player_state.grid_state[0])):
                if all(player_state.grid_state[row][col] != 0 for row in range(5)):
                    score += 7  # Bonus for completing a column
            return score
            
        if next_state.next_first_agent == id:
            score += 1

        score += deduct_unfilled_pattern_line(player_state)
        score += floor_penalty(player_state)
        score += center_score(player_state)
        score += get_pattern_score(player_state)
        score += player_state.ScoreRound()[0] # Round score from game mechanics
        score += player_state.EndOfGameScore() # End of game score from game mechanics


        return score