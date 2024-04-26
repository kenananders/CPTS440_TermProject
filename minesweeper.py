import random
from itertools import combinations_with_replacement, product
from queue import PriorityQueue


def MakeBoard(neighbors):  # tested
    solution = {}
    # initialize 10 X 10 board
    mine_positions = []
    n = 0
    number1 = -1
    number2 = -1
    random.seed(random.random())
    while n < 10:  # randomly choose 10 mine positions
        number1 = random.randint(0, 9)
        number2 = random.randint(0, 9)
        random.seed(random.random())
        if (number1, number2) not in mine_positions:
            mine_positions.append((number1, number2))
            solution[(number1, number2)] = True
            n = n + 1
    for r in range(10):  # for each row
        for c in range(10):  # for each column
            if (r, c) not in solution.keys():
                mine_number = 0
                for neighbor in neighbors[r, c]:
                    if neighbor in mine_positions:
                        mine_number = mine_number + 1
                solution[(r, c)] = mine_number  # Calculate numbers based on mine positions
    for key in solution.keys():
        print(key)
        print(solution[key])
    return solution

def FindNeighbors():  # tested
    neighbors = dict([])  # build a dictionary of adjacent positions
    neighbors[(0, 0)] = set([(a, b) for a in range(0, 2) for b in range(0, 2)])  # corners
    neighbors[(0, 0)].discard((0, 0))
    neighbors[(9, 9)] = set([(a, b) for a in range(8, 10) for b in range(8, 10)])
    neighbors[(9, 9)].discard((9, 9))
    neighbors[(0, 9)] = set([(a, b) for a in range(0, 2) for b in range(8, 10)])
    neighbors[(0, 9)].discard((0, 9))
    neighbors[(9, 0)] = set([(a, b) for a in range(8, 10) for b in range(0, 2)])
    neighbors[(9, 0)].discard((9, 0))
    for c in range(1, 10):  # first row
        neighbors[(0, c)] = set([(a, b) for a in range(0, 2) for b in range(c - 1, c + 2)])
        neighbors[(0, c)].discard((0, c))
    for r in range(1, 10):  # first column
        neighbors[(r, 0)] = set([(a, b) for a in range(r - 1, r + 2) for b in range(0, 2)])
        neighbors[(r, 0)].discard((r, 0))
    for c in range(0, 9):  # last row
        neighbors[(9, c)] = set([(a, b) for a in range(8, 10) for b in range(c - 1, c + 2)])
        neighbors[(9, c)].discard((9, c))
    for r in range(0, 9):  # last column
        neighbors[(r, 9)] = set([(a, b) for a in range(r - 1, r + 2) for b in range(8, 10)])
        neighbors[(r, 9)].discard((r, 9))
    for r in range(1, 9):
        for c in range(1, 9):  # for each position
            neighbors[(r, c)] = set([(a, b) for a in range(r - 1, r + 2) for b in range(c - 1, c + 2)])
            neighbors[(r, c)].discard((r, c))
    for key in neighbors.keys():
        print(key)
        print(neighbors[key])
    return neighbors


def GetRandomSquare():  # tested
    random.seed(random.random())
    number1 = random.randint(0, 9)
    number2 = random.randint(0, 9)
    print((number1, number2))
    return (number1, number2)


def Normalize(values):
    value1 = values[0] / (values[0] + values[1])
    value2 = values[1] / (values[0] + values[1])
    return (value1, value2)


class State:  # state of the board as seen by a player
    def __init__(self, solution, neighbors):
        self.solution = solution
        self.neighbors = neighbors
        self.positions = list([])  # the dictionary of all positions that have been assigned values
        self.mines = dict([])
        self.initialize()  # initialize empty board

    def initialize(self):
        for r in range(10):  # for each row
            for c in range(10):  # for each column
                self.mines[(r, c)] = "-"

    def AdjacentMines(self, pos, mines):  # Number of known mines next to a square
        mine_count = 0
        for neighbor in self.neighbors[pos]:
            if neighbor in self.positions:
                if self.mines[neighbor] == True:
                    mine_count = mine_count + 1
            return mine_count

    def GenerateModels(self, node, node_list):
        models = []
        # generate all possible t/f combinations for the node list
        for model in product([True, False], repeat=len(node_list)):
            model_dict = dict(zip(node_list.keys(), model))
            # check if this model is consistent, with added check for node existence
            if node in model_dict and self.CheckConsistency(model_dict, node, model_dict[node]):
                models.append(model_dict)
        return models

    def CheckConsistency(self, model, node, value):
        model[node] = value
        for square in model:
            mines_count = sum(model.get(neighbor, False) for neighbor in self.neighbors[square])
            if mines_count > self.solution[square]:  # the number of mines cannot exceed the hint
                return False
        return True

    def CalculateProbability(self, query, frontier, node_list, probabilities):
        # check if the node exists in the node list
        if query not in node_list:
            print(f"Node {query} does not exist in node list. Skipping.")
            return 0.0  # Return a neutral probability as we know there are no bombs

        models = self.GenerateModels(query, node_list)
        total_models = len(models)
        mine_models = sum(1 for m in models if m[query] == True)

        if total_models == 0:
            return 0.0

        probability_of_mine = mine_models / total_models
        return probability_of_mine

    def update(self, node, frontier, node_list):  # this is called when we assign value to position (r, c)
        squares = []
        square_count = 0
        mine_count = 0
        for pos in self.neighbors[node]:
            if pos not in self.positions:
                squares.append(pos)
                square_count = square_count + 1
            else:
                if self.mines[pos] == True:
                    mine_count = mine_count + 1
        if len(squares) == self.mines[node] - mine_count:  # if number of available neighboring squares
            # is equal to number of surrounding mines needed
            for i in range(0, len(squares)):
                self.mines[squares[i]] = True  # in this case all these squares will be mines
                frontier.get(squares[i])
                print(squares[i])
                self.positions.append(squares[i])
                del node_list[squares[i]]
                for pos1 in self.neighbors[squares[i]]:
                    if pos1 in self.positions:
                        if self.AdjacentMines(pos1, self.mines) == self.mines[pos1]:  # if a square
                            # already has the required mines next to it, all surrounding squares
                            # will be safe
                            for pos2 in self.neighbors[pos1]:
                                if pos2 in self.positions:
                                    self.mines[pos2] == self.solution[pos2]
                                    self.positions.append(pos2)
                                    del node_list[pos2]
                                    print(pos2)

        return frontier, node_list

def Explore(state, node, frontier, node_list, probabilities):
    # check if the node is a mine or safe area
    if state.solution[node] == 0:
        # all adjacent nodes are safe if the current node's mine count is 0
        for neighbor in state.neighbors[node]:
            if 0 <= neighbor[0] <= 9 and 0 <= neighbor[1] <= 9:  # ensures that invalid board values are discarded
                if neighbor not in state.positions:
                    state.mines[neighbor] = state.solution[neighbor]
                    state.positions.append(neighbor)
                    node_list.pop(neighbor, None)  # remove the neighbor from node_list
                    frontier.put((0, neighbor))  # safe nodes have the highest priority
    else:
        # calculate probability for each unvisited neighbor
        for neighbor in state.neighbors[node]:
            if 0 <= neighbor[0] <= 9 and 0 <= neighbor[1] <= 9:  # ensures that invalid board values are discarded
                if neighbor not in state.positions:
                    probability = state.CalculateProbability(neighbor, frontier, node_list, probabilities)
                    frontier.put((1 - probability, neighbor))  # prioritize by lowest probability of being a mine
                    node_list[neighbor] = probability  # update or add to node list
                    probabilities[neighbor] = probability

    return frontier, node_list

def search(state):
    node_list = {}
    probabilities = {}
    frontier = PriorityQueue()

    # start of game by picking square
    while True:
        square = GetRandomSquare()
        if state.solution[square] != True:
            frontier.put((1, square))
            node_list[square] = 1  # initialize tracking in node_list
            break

    while not frontier.empty() and len(state.positions) < 100:
        # node with the lowest probability of having a mine
        _, node = frontier.get()
        state.mines[node] = state.solution[node]
        state.positions.append(node)
        node_list.pop(node, None)  # remove node from node_list
        frontier, node_list = Explore(state, node, frontier, node_list, probabilities)

        # if the frontier is empty, try to find a new starting point
        if frontier.empty():
            for _ in range(100):  # try up to 100 times to find a new start
                square = GetRandomSquare()
                if square not in state.positions and state.solution[square] != True:
                    frontier.put((1, square))
                    node_list[square] = 1  # track new node
                    break

    if len(state.positions) == 100:
        print('All safe squares revealed.')
    else:
        print('Game ended without revealing all safe squares.')


neighbors = FindNeighbors()  # make neighbors dictionary
solution = MakeBoard(neighbors)
state = State(solution, neighbors)
search(state)