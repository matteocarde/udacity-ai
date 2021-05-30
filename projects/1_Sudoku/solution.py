from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
first_diagonal_unit = [r[0] + r[1] for r in zip(rows, cols)]
second_diagonal_unit = [r[0] + r[1] for r in zip(rows[::-1], cols)]
# TODO: Update the unit list to add the new diagonal units
unitlist = row_units + column_units + square_units + [first_diagonal_unit, second_diagonal_unit]

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """

    out = values.copy()
    # for boxA in values.keys():
    #     for boxB in peers[boxA]:
    #         if values[boxA] == values[boxB] and len(values[boxA]) == 2:
    #             for peer in peers[boxA] & peers[boxB]:
    #                 for digit in values[boxA]:
    #                     out[peer] = out[peer].replace(digit, "")
    for unit in unitlist:
        twins = {}
        for box in unit:
            if len(values[box]) != 2:
                continue
            twins[values[box]] = twins.get(values[box], [])
            twins[values[box]].append(box)

        for twinCouple in twins.values():
            if len(twinCouple) == 2:
                for other in set(unit) - set(twinCouple):
                    for digit in values[twinCouple[0]]:
                        out[other] = out[other].replace(digit, "")
    return out


def eliminate(values):
    solved = [box for box in values.keys() if (len(values[box]) == 1)]
    for k in solved:
        for peer in peers[k]:
            values[peer] = values[peer].replace(values[k], '')
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    result = reduce_puzzle(values)
    if result is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        print("I chose {0} for box {1}".format(value, s))
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        else:
            print(format("No solutions found !! Back tracking"))


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
