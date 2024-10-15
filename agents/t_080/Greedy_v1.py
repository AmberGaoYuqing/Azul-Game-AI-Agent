from copy import deepcopy

from template import Agent, GameRule
import random
from Azul.azul_model import AzulGameRule as GameRule


NUM_PLAYERS = 2


# simple searching method to pick action which returns lowest penalty

class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.game_rule = GameRule(NUM_PLAYERS)

    def SelectAction(self, actions, rootstate):

        new_actions = self.game_rule.getLegalActions(rootstate, self.id)

        best_floor_tiles_filled = 7
        best_action = random.choice(new_actions)

        for a in new_actions:
            # have to deepcopy so won't change original rootstate
            new_state = self.game_rule.generateSuccessor(deepcopy(rootstate), a, self.id)
            floor_tiles_filled = new_state.agents[self.id].floor.count(1)

            if floor_tiles_filled < best_floor_tiles_filled:
                best_action = a
                best_floor_tiles_filled = floor_tiles_filled

        return best_action