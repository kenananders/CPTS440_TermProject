import random
import time
from itertools import combinations_with_replacement
from queue import PriorityQueue

def MakeBoard(neighbors):
        solution = {}
        #initialize 10 X 10 board
        mine_positions = []
        n = 0
        number1 = -1
        number2 = -1
        random.seed(time)
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
        return solution  


def FindNeighbors():
    neighbors = dict([])  # build a dictionary of adjacent positions
    neighbors[(0, 0)] = set([(a, b) for a in range(0, 2) for b in range (0, 2)])
    neighbors[(0, 0)].discard((0, 0))
    for c in range(1, 10):   #first row
        neighbors[(0, c)] = set([(a, b) for a in range(0, 2) for b in range (c-1, c+2)])
        neighbors[(0, c)].discard((0, c))
    for r in range(1, 10):   #first column
        neighbors[(r, 0)] = set([(a, b) for a in range(r-1, r + 2) for b in range (0, 2)])
        neighbors[(r, 0)].discard((r, 0))
    for r in range(1,10):
        for c in range(1,10):  # for each position
            neighbors[(r, c)] = set([(a, b) for a in range(r-1, r+2) for b in range(c-1, c+2)])
            neighbors[(r, c)].discard((r, c))

    return neighbors



def GetRandomSquare():
    random.seed(random.random())      
    number1 = random.randint(0, 9)
    number2 = random.randint(0, 9)
    return (number1, number2)
    
       

class State:
    def __init__(self, solution, neighbors):
        self.solution = solution
        self.neighbors = neighbors
        self.positions = list([])  # the dictionary of all positions that have not been assigned values
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
                if mines[neighbor] == True:
                    mine_count = mine_count + 1
            return mine_count
    
   
    def CheckConsistency(self,model):
        for square in model.keys():
            for neighbor in neighbors[square]:
                if model[square] == True:
                    if neighbor not in self.positions and self.mines[neighbor] != True:  #checks to see if putting a mine in 
                        #a square would make a neighbor have too many adjacent mines
                        if self.AdjacentMines( neighbor, model) > self.mines[neighbor]:
                            return False
        return True

    def GenerateModels(self, node_list):
        models = []
        values = []
        while len(values) < 2 * len(node_list):
            values.append(True)
            values.append(False)
        comb_list = list(combinations_with_replacement(values, int(len(values)/2)))
        for j in range(0, len(comb_list)):
            model = {}
            for k in range (0, len(comb_list[j])):
                for key in node_list.keys():
                    if node_list[key] == k:
                        model[key] = comb_list[j][k]

            if model not in models:
                if self.CheckConsistency( model) == True:
                    models.append(model)
        return models






    def CalculateProbability(self,query,frontier, node_list, probabilities, prior_prob):
        models = self.GenerateModels(node_list)
        model_probs = []
        model_prob = 1
        prob_sum = 0
        for model in models:  #compares probabilities of possible models; only models consistent with
            #the given information are considered
            if self.mines[query] == True:  #calculate probability of query being a mine
                for square in frontier:
                    if square != query:  #search squares in frontier other than query
                        if model[square] == True:
                            if probabilities[node_list[square]] == 1:
                                model_prob = model_prob * prior_prob
                            else:
                                model_prob = model_prob * probabilities[node_list[square]]
                        else:
                            if probabilities[node_list[square]] == 1:
                                model_prob = model_prob * (1 - prior_prob)
                            else:
                                model_prob = model_prob *(1 - probabilities[node_list[square]])
                            
            model_probs.append(model_prob)
        for m in model_probs:
            prob_sum = prob_sum + m
        return prob_sum * prior_prob

    
       
                
    def update(self, node, frontier, node_list):  # this is called when we assign value to position (r, c)
        squares = []
        square_count = 0
        for pos in self.neighbors[node]:
           squares.append(pos)
           square_count = square_count + 1
           if len(squares) == self.mines[node]:
               for i in range(0, len(squares)):
                   self.mines[squares[i]] = True
                   frontier.get(squares[i])
                   self.positions.append(squares[i])
                   del node_list[squares[i]]
                   for pos1 in self.neighbors[squares[i]]:
                       if pos1 in self.positions:
                        if self.AdjacentMines(pos1, self.mines) == self.mines[pos1]:
                            for pos2 in self.neighbors[pos1]:
                                if pos2 in self.positions:
                                    self.mines[pos2] == self.solution[pos2]
                                    self.positions.append(pos2)
        
        return frontier, node_list
  

def Explore(state,node, neighbors, frontier, node_list, probabilities, prior_prob):
    for n in neighbors[node]:
        if n not in state.positions:
            probability = state.CalculateProbability(n, frontier, node_list, probabilities, prior_prob)
            frontier.put((1 - probability, n)) #lowest probability of mine has priority
            node_list[n] = len(node_list) 
            probabilities[len(node_list)] = probability
               
        
        
    return frontier, node_list, probability

def search(state):
    node_list = {}
    probabilities = []
    frontier = PriorityQueue()  # initialize frontier and explored tables
    while frontier.empty():
        square = GetRandomSquare()
        if state.solution[square] != True:
            frontier.put((1, square))
            node_list[square] = len(node_list) 

    while len(state.positions) < 100:
    
        node = frontier.get()[1] # select a node to be explored next
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
                        node_list[square] = len(node_list) 
    print('Found all mines')


        


neighbors = FindNeighbors() #make neighbors dictionary
solution = MakeBoard(neighbors)
state = State(solution, neighbors)
search(state)
