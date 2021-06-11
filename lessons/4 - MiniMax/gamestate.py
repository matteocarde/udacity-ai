# TODO: implement the __init__ class below by adding properties
# that meet the three requirements specified

import copy

PLAYER_O = 0
PLAYER_X = 1
INF = float("inf")

RAYS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

class GameState:

    def __init__(self):
        """The GameState class constructor performs required
        initializations when an instance is created. The class
        should:

        1) Keep track of which cells are open/closed
        2) Identify which player has initiative
        3) Record the current location of each player

        Parameters
        ----------
        self:
            instance methods automatically take "self" as an
            argument in python

        Returns
        -------
        None
        """
        # You can define attributes like this:
        # self.value = 73  # an arbitrary number
        # reassign it to a string (variable type is dynamic in Python)
        # self.value = "some string"
        # self.foo = []  # create an empty list
        self._nOfRows = 2
        self._nOfCols = 3

        self._cells = [(r, c) for r in range(self._nOfRows) for c in range(self._nOfCols)]
        self._blocked = dict(zip(self._cells, [False for i in range(len(self._cells))]))
        self._blocked[(self._nOfRows - 1, self._nOfCols - 1)] = True

        self._players = [PLAYER_O, PLAYER_X]
        self._turn = PLAYER_O
        self._locations = {
            PLAYER_O: None,
            PLAYER_X: None
        }

    def actions(self):
        """ Return a list of legal actions for the active player

        You are free to choose any convention to represent actions,
        but one option is to represent actions by the (row, column)
        of the endpoint for the token. For example, if your token is
        in (0, 0), and your opponent is in (1, 0) then the legal
        actions could be encoded as (0, 1) and (0, 2).
        """
        return self.liberties(self._locations[self._turn])

    def player(self):
        """ Return the id of the active player

        Hint: return 0 for the first player, and 1 for the second player
        """
        return self._turn

    def copy(self):
        return copy.deepcopy(self)

    def result(self, action):
        """ Return a new state that results from applying the given
        action in the current state

        Hint: Check out the deepcopy module--do NOT modify the
        objects internal state in place
        """
        next_state: GameState = self.copy()
        next_state._blocked[action] = next_state._turn
        next_state._turn = PLAYER_X if next_state._turn is PLAYER_O else PLAYER_O

        return next_state

    def terminal_test(self):
        """ return True if the current state is terminal,
        and False otherwise

        Hint: an Isolation state is terminal if _either_
        player has no remaining liberties (even if the
        player is not active in the current state)
        """
        return not self._has_liberties(PLAYER_X) or not self._has_liberties(PLAYER_O)

    def liberties(self, loc):
        """ Return a list of all open cells in the
        neighborhood of the specified location.  The list
        should include all open spaces in a straight line
        along any row, column or diagonal from the current
        position. (Tokens CANNOT move through obstacles
        or blocked squares in queens Isolation.)

        Note: if loc is None, then return all empty cells
        on the board
        """
        if not loc:
            return [key for key in self._blocked.keys() if self._blocked[key] is False]

        allowed = []

        for (dx, dy) in RAYS:
            _x, _y = loc
            while 0 <= _x + dx < self._nOfCols and 0 <= _y + dy < self._nOfRows:
                _x, _y = _x + dx, _y + dy
                if self._blocked[(_x, _y)]: break
                allowed.append((_x, _y))

        return allowed

    def utility(self, player_id):
        """ return +inf if the game is terminal and the
        specified player wins, return -inf if the game
        is terminal and the specified player loses, and
        return 0 if the game is not terminal
        """
        if not self.terminal_test(): return 0
        player_id_is_active = (player_id == self.player())
        active_has_liberties = self._has_liberties(self.player())
        active_player_wins = (active_has_liberties == player_id_is_active)
        return INF if active_player_wins else -INF

    def _has_liberties(self, player):
        return any(self.liberties(self._locations[player]))


def min_value(game_state: GameState):
    """ Return the game state utility if the game is over,
    otherwise return the minimum value over all legal successors

    # HINT: Assume that the utility is ALWAYS calculated for
            player 1, NOT for the "active" player
    """

    if game_state.terminal_test():
        return game_state.utility(PLAYER_O)
    v = INF
    for action in game_state.actions():
        v = min(v, max_value(game_state.result(action)))

    return v


def max_value(game_state: GameState):
    """ Return the game state utility if the game is over,
    otherwise return the maximum value over all legal successors

    # HINT: Assume that the utility is ALWAYS calculated for
            player 1, NOT for the "active" player
    """
    if game_state.terminal_test():
        return game_state.utility(PLAYER_O)
    v = -INF
    for action in game_state.actions():
        v = max(v, min_value(game_state.result(action)))

    return v

if __name__ == "__main__":
    g = GameState()
    actions = [((0, 0), INF), ((1, 0), -INF), ((2, 0), INF), ((0, 1), INF), ((1, 1), -INF)]

    for (a, ev) in actions:
        minV = min_value(g.result(a))
        if minV == ev:
            print("Looks like everything works! {} == {}".format(minV, ev))
        else:
            print("Uh oh! Not all the scores matched. {} != {}".format(minV, ev))
