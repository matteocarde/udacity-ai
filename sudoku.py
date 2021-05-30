def cross(a, b):
    return [s+t for s in a for t in b]


def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        values.append(all_digits if c == '.' else c)

    return dict(zip(boxes, values))


def eliminate(board):
    solved = [box for box in board.keys() if (len(board[box]) == 1)]
    for k in solved:
        for peer in peers[k]:
            board[peer] = board[peer].replace(board[k], '')
    return board


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


def is_completed(values):
    return len([box for box in values.keys() if len(values[box]) == 1]) == 81


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def search(values):
    result = reduce_puzzle(values)
    if result is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)


    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        print("I chose {0} for box {1}".format(value, s))
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        else:
            print(format("No solutions found !! Back tracking"))


# Values is a dictionary array
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123','456', '789')]

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

dic = grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')

print("Original")
print(display(dic))
print("After elimination")
print(display(eliminate(dic)))
print("After Only Choice")
print(display(only_choice(dic)))
print("After Reduction")
print(display(reduce_puzzle(dic)))
print("After Search")
print(display(search(dic)))


