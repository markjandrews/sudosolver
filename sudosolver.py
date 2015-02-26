import sys

positions = []
solve_log = []

class Position(object):

    def __init__(self, location=None, value=0):
        self.value = value
        self.available = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.location = location

    def __repr__(self):
        return 'Position(%s, %s)' % (str(self.location), self.value)

def rowcol_to_box(row, col):
    return 3 * int((row-1)/3) + int((col-1)/3) + 1

def to_result(positions):
    sorted_positions = sorted(positions, key=lambda x : x.location)

    result = []
    for row in range(0, 9):
        line = []
        for col in range(0, 9):
            value = sorted_positions[row*9 + col].value
            if value is None:
                value = 0
            line.append(str(value))

        result.append(''.join(line))

    return '\n'.join(result)


def get_allocated(positions, location):

    result_set = set()
    for i in range(3):
        result_set |= set([x.value for x in positions if x.location[i] == location[i] and x.value != 0])

    return result_set

def solve(positions):

    while True:
        sorted_positions = sorted(positions, key=lambda x : len(x.available))

        next_position = next((x for x in sorted_positions if x.value == 0), None)
        if next_position is None:
            break

        result_set = get_allocated(positions, next_position.location)
        next_position.available -= result_set

        if len(next_position.available) > 0:
            next_position.value = next_position.available.pop()
            solve_log.append((next_position.location, next_position.available.copy()))
            next_position.available = set()
        else:
            location, available = solve_log.pop()
            prev_position = next(x for x in positions if x.location == location)
            prev_position.available = available
            prev_position.value = 0
            next_position.available = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    return to_result(positions)


def main(argv):

    with open(argv[0], 'rb') as inf:
        data = ''.join(inf.read().splitlines())

    for row in range(1, 10):
        for col in range(1, 10):
            box = rowcol_to_box(row, col)
            position = Position()
            position.value = int(data[(row-1)*9 + col - 1])
            position.location = (row, col, box)

            # Simple check for duplicate value
            if len({position.value} - get_allocated(positions, position.location)) == 0:
                raise Exception('Found duplicate value in row/col/box of %s' % position)

            if position.value != 0:
                position.available = []

            positions.append(position)

    solved_positions = solve(positions)
    print(solved_positions)

if __name__ == '__main__':
    main(sys.argv[1:])