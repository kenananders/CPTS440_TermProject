import random
from itertools import combinations_with_replacement
from queue import PriorityQueue

def MakeBoard(neighbors):  #tested
        solution = {}
        #initialize 10 X 10 board
        mine_positions = []
        n = 0
        number1 = -1
        number2 = -1
        random.seed(random.random())
        while  n < 10:   #randomly choose 10 mine positions      
            number1 = random.randint(0, 9)
            number2 = random.randint(0, 9)
            random.seed(random.random())
            if (number1, number2) not in mine_positions:
                mine_positions.append((number1, number2))
                solution[(number1, number2)] = True
                n = n + 1
        for r in range(10):  # for each row
            for c in range(10):  # for each column
                if (r,c) not in solution.keys():
                    mine_number = 0
                    for neighbor in neighbors[r,c]:
                        if neighbor in mine_positions:
                            mine_number = mine_number + 1
                    solution[(r, c)] = mine_number   #Calculate numbers based on mine positions
        for key in solution.keys():
            print (key) 
            print (solution[key])
        return solution  


def FindNeighbors():  #tested
    neighbors = dict([])  # build a dictionary of adjacent positions
    neighbors[(0, 0)] = set([(a, b) for a in range(0, 2) for b in range (0, 2)]) #corners
    neighbors[(0, 0)].discard((0, 0))
    neighbors[(9, 9)] = set([(a, b) for a in range(8, 10) for b in range (8, 10)])
    neighbors[(9, 9)].discard((9, 9))
    neighbors[(0, 9)] = set([(a, b) for a in range(0, 2) for b in range (8, 10)])
    neighbors[(0, 9)].discard((0, 9))
    neighbors[(9, 0)] = set([(a, b) for a in range(8, 10) for b in range (0, 2)])
    neighbors[(9, 0)].discard((9, 0))
    for c in range(1, 10):   #first row
        neighbors[(0, c)] = set([(a, b) for a in range(0, 2) for b in range (c-1, c+2)])
        neighbors[(0, c)].discard((0, c))
    for r in range(1, 10):   #first column
        neighbors[(r, 0)] = set([(a, b) for a in range(r-1, r + 2) for b in range (0, 2)])
        neighbors[(r, 0)].discard((r, 0))
    for c in range(0, 9):   #last row
        neighbors[(9, c)] = set([(a, b) for a in range(8, 10) for b in range (c-1, c+2)])
        neighbors[(9, c)].discard((9, c))
    for r in range(0, 9):   #last column
        neighbors[(r, 9)] = set([(a, b) for a in range(r-1, r + 2) for b in range (8, 10)])
        neighbors[(r, 9)].discard((r, 9))
    for r in range(1,9):
        for c in range(1,9):  # for each position
            neighbors[(r, c)] = set([(a, b) for a in range(r-1, r+2) for b in range(c-1, c+2)])
            neighbors[(r, c)].discard((r, c))
    for key in neighbors.keys():
        print (key) 
        print (neighbors[key])
    return neighbors



def GetRandomSquare():  #tested
    random.seed(random.random())      
    number1 = random.randint(0, 9)
    number2 = random.randint(0, 9)
    print((number1, number2))
    return (number1, number2)


def Normalize(values):
        value1 = values[0]/(values[0] + values[1])
        value2 = values[1]/(values[0] + values[1])
        return(value1, value2)
    
       

class State:  #state of the board as seen by a player
    def __init__(self, solution, neighbors):
        self.solution = solution
        self.neighbors = neighbors
        self.positions = list([])  # the dictionary of all positions that have been assigned values
        self.mines = dict([])
        self.initialize() # initialize empty board
        
    

    def initialize(self):
        for r in range(10):  # for each row
            for c in range(10):  # for each column
                self.mines[(r,c)] = "-"


    def AdjacentMines(self,pos, mines):  #Number of known mines next to a square
        mine_count = 0
        for neighbor in self.neighbors[pos]:
            if neighbor in self.positions:
                if self.mines[neighbor] == True:
                    mine_count = mine_count + 1
            return mine_count
    
   
    def CheckConsistency(self,model, node, value): #eliminates models that have too many mines next to a square
        model[node] = value
        for square in model.keys():
            for neighbor in neighbors[square]:
                if model[square] == True:
                    if neighbor in self.positions and self.mines[neighbor] != True:  #checks to see if putting a mine in 
                        #a square would make a neighbor have too many adjacent mines
                        if self.AdjacentMines( neighbor, model) > self.mines[neighbor]:
                            return False
        return True

    def GenerateModels(self, node, node_list):
        models = []
        values = []
        while len(values) < 2 * len(node_list):  #want to generate all possible configurations of mine 
            #(True) and no mine (False) in the frontier (same as node_list)
            values.append(True)
            values.append(False)
        unique_combinations = []
        comb_list = list(combinations_with_replacement(values, int(len(values)/2)))
        for i in range (0, len(comb_list)):
            if comb_list[i] not in unique_combinations:
                unique_combinations.append(comb_list[i])
        mine = [True, False]
        for a in range(0, len(mine)):
            for j in range(0, len(unique_combinations)):

                model = {}
                for k in range (0, len(unique_combinations[j])):
                    for key in node_list.keys():
                        if key not in model.keys():
                            model[key] = unique_combinations[j][k]

                if model not in models:
                    if self.CheckConsistency( model, node, mine[a]) == True:
                        models[a].append(model)
        for m in models:
            print(m)
        return (models[0], models[1])



    def CalculateProbability(self,query,frontier, node_list, probabilities, prior_prob):
        #see pages 500-502/section 13.6 of textbook (3rd edition)
        models = self.GenerateModels(query, node_list)
        mine_probabilities = []
        for m in range(0, len(models)):
            model_prob = 1
            prob_sum = 0
            model_probs = []
            for model in models[m]:  #compares probabilities of possible models; only models consistent with
            #the given information are considered
             #calculate probability of query being a mine
                for square in node_list.keys():
                    if square != query:  #search squares in frontier other than query
                        if model[square] == True:
                            if probabilities[node_list[square]] == 1: #one is default value
                                model_prob = model_prob * prior_prob
                            else:
                                model_prob = model_prob * probabilities[node_list[square]]
                        else:
                            if probabilities[node_list[square]] == 1:
                                model_prob = model_prob * (1 - prior_prob)
                            else:
                                model_prob = model_prob *(1 - probabilities[node_list[square]])
                            
                model_probs.append(model_prob)
            for n in model_probs:
                prob_sum = prob_sum + n
            mine_probabilities.append(prob_sum * prior_prob)   #naive Bayes calculation- probability of a mine given evidence is probability
    #of evidence given probability of a mine multiplied by the prior probability
        mine_probabilities2 = Normalize(mine_probabilities)
        return mine_probabilities2[0]
    
       
                
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
        if len(squares) == self.mines[node] - mine_count:  #if number of available neighboring squares
               #is equal to number of surrounding mines needed
               for i in range(0, len(squares)):
                   self.mines[squares[i]] = True  #in this case all these squares will be mines
                   frontier.get(squares[i])
                   print(squares[i])
                   self.positions.append(squares[i])
                   del node_list[squares[i]]
                   for pos1 in self.neighbors[squares[i]]:
                       if pos1 in self.positions:
                        if self.AdjacentMines(pos1, self.mines) == self.mines[pos1]:  #if a square
                            #already has the required mines next to it, all surrounding squares 
                            #will be safe
                            for pos2 in self.neighbors[pos1]:
                                if pos2 in self.positions:
                                    self.mines[pos2] == self.solution[pos2]
                                    self.positions.append(pos2)
                                    del node_list[pos2]
                                    print(pos2)
        
        return frontier, node_list
  

def Explore(state,node, neighbors, frontier, node_list, probabilities, prior_prob):
    if state.mines[node] == 0: #no neighbors have mines, so they are all safe
        for neighbor in neighbors[node]:
            state.mines[neighbor] = state.solution[neighbor]
            state.positions.append(neighbor)
            if neighbor in node_list.keys():
                del node_list[neighbor]
            for n in neighbors[neighbor]:
                probability = state.CalculateProbability(n, frontier, node_list, probabilities, prior_prob)
                frontier.put((1-probability, n))
                node_list[n] = len(node_list) + len(state.positions)
                probabilities[len(node_list) - 1 + len(state.positions)] = probability
               
    else:
        for n in neighbors[node]:
            if n not in state.positions:
                probability = state.CalculateProbability(n, frontier, node_list, probabilities, prior_prob)
                frontier.put((1 - probability, n)) #lowest probability of mine has priority
                node_list[n] = len(node_list) + len(state.positions)
                probabilities[len(node_list)  + len(state.positions)] = probability
               
        
    #del node_list[node]   
    return frontier, node_list, probability

def search(state):
    node_list = {}
    probabilities = {}
    frontier = PriorityQueue()  # initialize frontier and explored tables
    while frontier.empty():
        square = GetRandomSquare()
        if state.solution[square] != True:
            frontier.put((1, square))
            node_list[square] = len(node_list) + len(state.positions)
            probabilities[len(node_list) - 1  + len(state.positions)] = 1

            #state.mines[square] = state.solution[square]
            #state.positions.append(square)
            #state.update(square, frontier, node_list)

    while len(state.positions) < 100:
    
        node = frontier.get()[1] # select a node to be explored next
        state.mines[node] = state.solution[node]
        print(node)
        state.positions.append(node)
        del node_list[node]
        frontier, node_list = state.update(node, frontier, node_list)
        frontier, node_list, probabilities = Explore(state, node, neighbors, frontier, node_list, probabilities, 0.1)
        if frontier.empty():
            while frontier.empty():
                square = GetRandomSquare()
                if square not in state.positions:
                    if solution[square] == True:
                        print("Lost the game")
                        return
                    else:
                        frontier.put((1, square))
                        node_list[square] = len(node_list) + len(state.positions)
                        probabilities[len(node_list) - 1  + len(state.positions)] = 1
    print('Found all mines')


        


neighbors = FindNeighbors() #make neighbors dictionary
solution = MakeBoard(neighbors)
state = State(solution, neighbors)
search(state)
