import math

import random
from sample_players import DataPlayer

_WIDTH = 11
_HEIGHT = 9


class CustomPlayer(DataPlayer):
    def get_action(self, state):
        """ Choose an action available in the current state

        See RandomPlayer and GreedyPlayer for examples.

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        **********************************************************************
        NOTE: since the caller is responsible for cutting off search, calling
              get_action() from your own code will create an infinite loop!
              See (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal minimax move at a fixed search depth of 3 plies
        print(state.ply_count)
        if state.ply_count < 45:
            self.queue.put(max(state.actions(), key=lambda x: self.score(state.result(x))))
        else:
            self.queue.put(self.minimax(state, depth=6))

    def minimax(self, state, depth):

        def max_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        def min_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        alpha = float("-inf")
        beta = float("+inf")
        return max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))

    def ind2xy(self, ind):
        """ Convert from board index value to xy coordinates

        The coordinate frame is 0 in the bottom right corner, with x increasing
        along the columns progressing towards the left, and y increasing along
        the rows progressing towards teh top.
        """
        return ind % (_WIDTH + 2), ind // (_WIDTH + 2)

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def scoreGreedy(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]

        center = _WIDTH / 2, _HEIGHT / 2
        if state.ply_count < 3:
            opp = center
        else:
            opp = self.ind2xy(opp_loc)

        me = self.ind2xy(own_loc)

        d_center = (center[0] - me[0])**2 + (center[1] - me[1])**2
        d_opp = (opp[0] - me[0])**2 + (opp[1] - me[1])**2

        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = len(state.liberties(own_loc))
        opp_liberties = len(state.liberties(opp_loc))

        if opp_liberties > own_liberties:
            score = 1000 * d_center**2 * (opp_liberties - own_liberties)
        else:
            score = (d_center + d_opp)**2*max(1, own_liberties - opp_liberties)

        return score
