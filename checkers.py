import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching!

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):

        self.board = board
        self.parent = None
        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="") 
            print("")
        print("")

def get_opp_char(player): # returns the opponent's character
    '''Return the opponent's character for the given player. TODO - what 
    doess this even mean/do?'''
    if player in ['b', 'B']: # if the player is black
        return ['r', 'R'] # return red
    else: # if the player is red
        return ['b', 'B'] # return black

def get_next_turn(curr_turn): 
    '''Return the next turn for the given player. TODO - what about kings?'''
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def is_terminal(state, player):
    '''Return True if the given state is a terminal state for the given player,
    and False otherwise. A state is a terminal state if the given player has no
    legal moves left, or if the given player has won or lost the game (no pieces
    left for one of the players).'''
    red_points = 0
    black_points = 0

    for i in range(8):
        for j in range(8):
            if state.board[i][j] == 'r':
                red_points += 1
            elif state.board[i][j] == 'b':
                black_points += 1
            elif state.board[i][j] == 'R':
                red_points += 2
            elif state.board[i][j] == 'B':
                black_points += 2

    if red_points == 0 or black_points == 0: # if one of the players has no pieces left
        return True
    elif gen_successors(state, player) == []: # if the player has no legal moves left
        return True
    else:
        return False

def utility(state, player, maxp, depth=1):
    '''Return the utility of the player for a given TERMINAL state. The depth
    is the current depth that the state is at, defaulted to 1. maxp is the 
    maximum player in alpha beta pruning.'''
    red_points = 0
    black_points = 0

    for i in range(8):
        for j in range(8):
            if state.board[i][j] == 'r':
                red_points += 1
            elif state.board[i][j] == 'b':
                black_points += 1
            elif state.board[i][j] == 'R':
                red_points += 2
            elif state.board[i][j] == 'B':
                black_points += 2

    if red_points == 0: # red loses, black wins
        if maxp == 'r':
            return -1000000/depth
            # return -float('inf')
        else:
            return 1000000/depth
            # return float('inf')
    elif black_points == 0: # red wins, black loses
        if maxp == 'b':
            return -1000000/depth
            # return -float('inf')
        else:
            return 1000000/depth
            # return float('inf')
    elif maxp == player:
        return -1000000/depth   # if this a terminal state, I must not have any moves left then
    else:
        return 1000000/depth # a winning state
        # return -float('inf')    
    # elif gen_successors(state, player) == []: # no moves left for the turn, that player loses 
    #     return -float('inf')

def evaluate(state, max): #TODO - optimize if time?
    '''Return the heuristic estimate of the given NON-TERMINAL state for the 
    given player's utility. This is used when the depth limit is reached.
    A king is worth 2 points, and a regular piece is worth 1. The heuristic is 
    the difference between the points for the given player and the points for 
    the opponent. 

    - max: the player whose turn it is (the maximizing player)
    - state: the state to evaluate

    TODO - add more features and preferences that they hinted for 
    whaat represents a better state!! (location, centre, safe points, # of 
    possible moves, etc.) IF TIME
    
    TODO - make more efficient!!'''

    red_points = 0
    black_points = 0

    for i in range(8):
        for j in range(8):
            if state.board[i][j] == 'r':
                red_points += 1
            elif state.board[i][j] == 'b':
                black_points += 1
            elif state.board[i][j] == 'R':
                red_points += 2
            elif state.board[i][j] == 'B':
                black_points += 2
    
    if max == 'r':
            return red_points - black_points
    else:
        return black_points - red_points

def alpha_beta_search(state, player): #TODO - is this even right? FIX
    '''Perform alpha-beta pruning on the given state for the given player using
    a PRE-SPECIFIED depth limit (TODO - pick good one). TODO: Use gen_successors here
    to have a list of moves to judge?? When the program reaches the depth limit, 
    apply the evaluation function. Return the best move.'''
    # if state in cache:
    #     return cache[state]
    v = max_value(state, -float('inf'), float('inf'), 1, player, state, player) #TODO change to opponent's player??
    # cache[state] = v[0]
    # print(v)
    return v[0]

def max_value(state, alpha, beta, depth, player, ogs,maxp): #TODO - assign depth limit, utility not even used here!!
    '''Return the maximum utility value for the given state, alpha, beta, 
    player, and depth. 
    - ogs is the original state (root of the game tree)
    - maxp is the player maximizing their utility over one iteration/game tree
    - player is who's turn it is at each level of the game tree
    '''
    max_depth = 8 # TODO - pick good one
    if is_terminal(state, player):
        return (state, utility(state, player, maxp, depth))
    if depth == max_depth: #or is_terminal(state, player)==True: # reached the depth limit. TODO - how to differentiate between terminal and non-terminal states?
        return (state, evaluate(state, maxp)) # estimate player's utility
    v = (None, -float('inf')) 

    successors = gen_successors(state, player) 
    # Do node ordering for successors list: 
    successors.sort(key=lambda x: evaluate(x, maxp), reverse=True) # sort by descending utility for max player 

    for action in successors:
        m = min_value(action, alpha, beta, depth + 1, get_next_turn(player), ogs,maxp)
        if m[1] >= v[1]:
            v = m # overwrite the parent's value and state if the child value is better with the child value

        if v[1] >= beta:
            if state == ogs: # check that we don't go up too far 
                return v
            return state, v[1] # non-terminal state (don't overwrite value, only do state)
        alpha = max(alpha, v[1])
    if state == ogs:
        return v # return the current state with its terminal value
    return state, v[1]

def min_value(state, alpha, beta, depth, player, ogs,maxp): #TODO - assign depth limit, check when switching players 
    '''Return the minimum utility value for the given state, alpha, beta,
    player, and depth. ogs is the original state (root of the game tree).'''
    max_depth = 8 # TODO - pick good one
    if is_terminal(state, player):
        return (state, utility(state, player, maxp, depth))
    if depth == max_depth: #or is_terminal(state, player)==True: # reached the depth limit. TODO - how to differentiate between terminal and non-terminal states?
        return (state, evaluate(state, maxp)) # estimate player's utility
    
    v = (None, float('inf')) # initialize every min node
    # v = evaluate(state, player) # terminal state?

    successors = gen_successors(state, player) 
    # Do node ordering for successors list: 
    successors.sort(key=lambda x: evaluate(x, maxp), reverse=False) # sort by ascending utility for min player 

    for action in successors:
        action.parent = state
        m = max_value(action, alpha, beta, depth + 1, get_next_turn(player), ogs,maxp)
        if m[1] <= v[1]:
            v = m
        if v[1] <= alpha:
            if state == ogs: # check that we don't go up too far
                return v
            return state, v[1] # non-terminal state
        beta = min(beta, v[1])
    if state == ogs: # check that we don't go up too far
        return v # return one of the direct children of original state
    return state, v[1]

def move(state, move, jump=False):
    '''Return the state that results from applying the given move to the 
    given state. The move is represented as a tuple from p1 to p2 (y1, x1, y2, x2).
    If the move is a jump, the piece in between is removed.'''

    state.board[move[2]][move[3]] = state.board[move[0]][move[1]] # either 'r', 'b', 'R', or 'B'
    state.board[move[0]][move[1]] = '.'

    if jump == True:
        state.board[(move[2] + move[0])//2][(move[3] + move[1])//2] = '.' # remove the jumped piece
    
    if jump != True: # only promote a piece to king if it's a simple move here (recursion must be broken in jumps; fixed in try_jumps)
        # if red piece reaches top of board, make it a king
        if move[2] == 0 and state.board[move[2]][move[3]] == 'r':
            state.board[move[2]][move[3]] = 'R'
        # if black piece reaches bottom of board, make it a king
        elif move[2] == 7 and state.board[move[2]][move[3]] == 'b':
            state.board[move[2]][move[3]] = 'B'

    return state #same as the result(s, action) function from the pseudocode?

def possible_simple_moves(state, turn):
    '''Return a list of possible SIMPLE moves for the given player in the given 
    state. The turn can be either 'r', 'b' to indicate whos turn it is.

    The function passes in a list of size-4 tuples: (y1, x1, y2, x2) where (y1, x1)
    is the starting position and (y2, x2) is the ending position to move. The 
    successor state is added to a list, moves. The moves list is ordered by 
    utility of each state, best to worst for the respective turn.
    '''
    moves = []

    for i in range(state.height):
        for j in range(state.width):
                if turn == 'b':
                    if state.board[i][j] == 'b' or state.board[i][j] == 'B':
                        if i + 1 < state.height and j + 1 < state.width: # move diagonal right down
                            if state.board[i + 1][j + 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i + 1, j + 1))
                                moves.append(new_state)
                        if i + 1 < state.height and j - 1 >= 0: # move diagonal left down
                            if state.board[i + 1][j - 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i + 1, j - 1))
                                moves.append(new_state)
                    if state.board[i][j] == 'B': # keep as 'if' statement so will still check all 4 directions for king
                        if i - 1 >= 0 and j + 1 < state.width: # move diagonal right up
                            if state.board[i - 1][j + 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i - 1, j + 1))
                                moves.append(new_state)
                        if i - 1 >= 0 and j - 1 >= 0: # move diagonal left up
                            if state.board[i - 1][j - 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i - 1, j - 1))
                                moves.append(new_state)
                elif turn == 'r':
                    if state.board[i][j] == 'r' or state.board[i][j] == 'R':
                        if i - 1 >= 0 and j + 1 < state.width: # move diagonal right up
                            if state.board[i - 1][j + 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i - 1, j + 1))
                                moves.append(new_state)
                        if i - 1 >= 0 and j - 1 >= 0: # move diagonal left up
                            if state.board[i - 1][j - 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i - 1, j - 1))
                                moves.append(new_state)
                    if state.board[i][j] == 'R': # keep as 'if' statement so will still check all 4 directions for king
                        if i + 1 < state.height and j + 1 < state.width: # move diagonal right down
                            if state.board[i + 1][j + 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i + 1, j + 1))
                                moves.append(new_state)
                        if i + 1 < state.height and j - 1 >= 0: # move diagonal left down
                            if state.board[i + 1][j - 1] == '.':
                                new_state = copy.deepcopy(state)
                                move(new_state, (i, j, i + 1, j - 1))
                                moves.append(new_state)

    return moves # a list of simple successor states

def try_jumps(state, turn): #TODO : optimize with node ordering/state caching
    '''Given a state and whose turn it is, iterate through the board. If it is 
    a piece belonging to the turn, send it to multi-jumps to evaluate if there
    are any jumps possible. If there are, multi-jumps will return final state(s),
    and these will be appended to the jumped list. Node ordering is also 
    implemented to order the list of successsors by best to worst for its
    respective player.
    
    This function returns a list of all possible fully jumped states. If the list
    is empty, then there are no jumps available for that turn. Then the simple
    moves must be checked.'''

    jumped = [] # list of all possible fully jumped states (entire sequences; final states)

    # Recursive case: checking if jumps are available
    for y in range(state.height):
        for x in range(state.width):
            if turn == 'r':
                if state.board[y][x] == 'r' or state.board[y][x] == 'R':
                    # print("trying coordinates ", y, x)
                    jumped+=try_multi_jumps(state, (y,x),state, l=[])
                    # print("jumped list: ", jumped)
            elif turn == 'b':
                if state.board[y][x] == 'b' or state.board[y][x] == 'B':
                    jumped+=try_multi_jumps(state, (y,x),state,l=[])

    # In move function, a jump to the last row DOES NOT promote piece to king.
    # This is done here to prevent their turn continuing once promoted:
    for s in jumped: # for every successor state
        if turn == 'r':
            # print("top row should be: ", s.board[0])
            for j in range(8): # check top row for reds
                if s.board[0][j] == 'r':
                    # print("promoted a red to king!")
                    s.board[0][j] = 'R' 
        if turn == 'b':
            for j in range(8): # check bottom row for blacks 
                if s.board[7][j] == 'b':
                    s.board[7][j] = 'B'
    
    return jumped # Base case: no possible jumps at all, so jumped = []

def try_multi_jumps(state, new_coords, ogs, l=[]):
    '''Recursive function to attempt all possible FULL jump sequences for 
    a piece that has been found. The input state is the original state (ogs),
    and new_coords is a tuple with the format (y,x). (y,x) is the 
    coordinate of the discovered piece. 

    The function takes in the (y,x) of a piece and recursively checks if
    there are any  jumps available from that position. If there are, it
    continues to check for more jumps. If there are no more jumps available, it
    returns the state as a final successor of the original one.'''

    y,x = new_coords
    piece = state.board[y][x] # the piece that just moved; either 'r', 'b', 'R', or 'B'
    # print("the piece that just moved is: ", piece, "  at coordinates: ", y, x)
    multiple_jumps = False # boolean to check if there are any more jumps available from this position

    # check if there are any more jumps available from this position
    if piece == 'b':
        if y + 2 < state.height and x + 2 < state.width:
            if state.board[y + 1][x + 1] == 'r' or state.board[y + 1][x + 1] == 'R':
                if state.board[y + 2][x + 2] == '.': # black jump up right
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y + 2, x + 2), True)
                    l += try_multi_jumps(new_state, (y + 2, x + 2),ogs,l=l) # check if more jumps possible from this position (recursion)
                    multiple_jumps = True
        if y + 2 < state.height and x - 2 >= 0:
            if state.board[y + 1][x - 1] == 'r' or state.board[y + 1][x - 1] == 'R':
                if state.board[y + 2][x - 2] == '.': # black jump up left
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y + 2, x - 2), True)
                    l += try_multi_jumps(new_state, (y + 2, x - 2),ogs,l=l)
                    multiple_jumps = True
    elif piece == 'r':
        if y - 2 >= 0 and x + 2 < state.width:
            if state.board[y - 1][x + 1] == 'b' or state.board[y - 1][x + 1] == 'B':
                if state.board[y - 2][x + 2] == '.': # red jump up right
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y - 2, x + 2), True)
                    l += try_multi_jumps(new_state, (y - 2, x + 2),ogs,l=l) # for some reason y,x=0,3 changes to 4,3 here??
                    multiple_jumps = True
        if y - 2 >= 0 and x - 2 >= 0:
            if state.board[y - 1][x - 1] == 'b' or state.board[y - 1][x - 1] == 'B':
                if state.board[y - 2][x - 2] == '.': # red jump up left
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y - 2, x - 2), True) #for some reason y,x=0,3 changes to 2,5 here??
                    l += try_multi_jumps(new_state, (y - 2, x - 2),ogs,l=l)  
                    multiple_jumps = True
    elif piece == 'R':
        if y + 2 < state.height and x + 2 < state.width:
            if state.board[y + 1][x + 1] == 'b' or state.board[y + 1][x + 1] == 'B':
                if state.board[y + 2][x + 2] == '.': # red king jump up right
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y + 2, x + 2), True)
                    l += try_multi_jumps(new_state, (y + 2, x + 2),ogs,l=l)
                    multiple_jumps = True
        if y + 2 < state.height and x - 2 >= 0:
            if state.board[y + 1][x - 1] == 'b' or state.board[y + 1][x - 1] == 'B':
                if state.board[y + 2][x - 2] == '.': # red king jump up left
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y + 2, x - 2), True)
                    l += try_multi_jumps(new_state, (y + 2, x - 2),ogs,l=l)
                    multiple_jumps = True
        if y - 2 >= 0 and x + 2 < state.width:
            if state.board[y - 1][x + 1] == 'b' or state.board[y - 1][x + 1] == 'B':
                if state.board[y - 2][x + 2] == '.': # red king jump down right
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y - 2, x + 2), True)
                    l += try_multi_jumps(new_state, (y - 2, x + 2),ogs,l=l)
                    multiple_jumps = True
        if y - 2 >= 0 and x - 2 >= 0:
            if state.board[y - 1][x - 1] == 'b' or state.board[y - 1][x - 1] == 'B':
                if state.board[y - 2][x - 2] == '.': # red king jump down left
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y - 2, x - 2), True)
                    l += try_multi_jumps(new_state, (y - 2, x - 2),ogs,l=l)
                    multiple_jumps = True
    elif piece == 'B':
        if y + 2 < state.height and x + 2 < state.width:
            if state.board[y + 1][x + 1] == 'r' or state.board[y + 1][x + 1] == 'R':
                if state.board[y + 2][x + 2] == '.': # black king jump up right
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y + 2, x + 2), True)
                    l += try_multi_jumps(new_state, (y + 2, x + 2),ogs,l=l)
                    multiple_jumps = True
        if y + 2 < state.height and x - 2 >= 0:
            if state.board[y + 1][x - 1] == 'r' or state.board[y + 1][x - 1] == 'R':
                if state.board[y + 2][x - 2] == '.':
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y + 2, x - 2), True)
                    l += try_multi_jumps(new_state, (y + 2, x - 2),ogs,l=l)
                    multiple_jumps = True
        if y - 2 >= 0 and x + 2 < state.width:
            if state.board[y - 1][x + 1] == 'r' or state.board[y - 1][x + 1] == 'R':
                if state.board[y - 2][x + 2] == '.': # black king jump down right
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y - 2, x + 2), True)
                    l+= try_multi_jumps(new_state, (y - 2, x + 2),ogs,l=l)
                    multiple_jumps = True
        if y - 2 >= 0 and x - 2 >= 0:
            if state.board[y - 1][x - 1] == 'r' or state.board[y - 1][x - 1] == 'R':
                if state.board[y - 2][x - 2] == '.': # black king jump down left
                    new_state = copy.deepcopy(state)
                    new_state = move(new_state, (y, x, y - 2, x - 2), True)
                    l += try_multi_jumps(new_state, (y - 2, x - 2),ogs,l=l)
                    multiple_jumps = True
    
    if state == ogs and not multiple_jumps: # jumps not possible
        return []
    elif state == ogs: # when going back in recursion 
        return l
    elif multiple_jumps == False: # not at original state but found a final one
        return [state] # jump or multi-jump
    else:
        return [] # in between state 
    # return state # final successor  of a jump sequence

def gen_successors(state, turn):
    '''Return a list of successors for the given player in the given state.
    If a jump is possible, only jumps should be returned.
        
    TODO - implement additional optimizations (node ordering, caching, etc.)'''

    jump_successors = try_jumps(state, turn) # a list of final jump successor states

    if jump_successors == []: # no jumps possible; return simple moves
        simple_successors = possible_simple_moves(state, turn) # a list of simple successor states
        return simple_successors

    else: # jumps are possible
        return jump_successors

def convert_to_str(state):
    '''Given a state (8x8 grid), convert it to a string of 64 characters 
    with the correct board formatting.'''
    res = ""
    for i in range(8):
        for j in range(8):
            res += state.board[i][j]
            if (j+1) % 8 == 0:
                res += "\n"
    
    res += "\n"

    return res

def play(state, turn='r', outputfile="output.txt"):
    '''Play a game of checkers given the initial state, and red always goes 
    first. Alternate between alpha beta pruning, and write out each turn's
    action in the outputfile.'''

    res = ""
    file = open(outputfile, "w")
    res += convert_to_str(state) # add the initial state 
    move_count = 0

    while not is_terminal(state, turn):
        state = alpha_beta_search(state, turn) # returns best action for that player
        turn = get_next_turn(turn) # switch turns
        res += convert_to_str(state)
        move_count += 1
        print("move: ", move_count)
        state.display() # display the board
        print()
        #TODO: later write each state (including initial) into output file
    
    file.write(res)
    file.close()
    print("number of moves: ", move_count)
    pass

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    # args = parser.parse_args()
    
    # initial_board = read_from_file(args.inputfile)
    initial_board = read_from_file('input.txt')

    state = State(initial_board)
    turn = 'r'
    ctr = 0

    print("initial state: ")
    state.display()

    # print("string conversion: ", convert_to_str(state))
    # print("test")

    # print("utility of initial state: ", utility(state, turn))
    # print("evaluation of initial state: ", evaluate(state, turn))

    # print("try multi-jump iterative: ")
    # for s in try_multi_jumps(state, (4,7), state): 
    #     s.display(

    # print("attempting jumps for ", turn, ":")
    # for jump in try_jumps(state, turn):
    #     print("utility of below state: ", evaluate(jump, turn))
    #     jump.display()

    # print("possible simple moves for ", turn, ":")
    # for m in possible_simple_moves(state, turn):
    #     print("utility of below state: ", evaluate(m, turn))
    #     m.display()

    # print("successors of initial state: ")
    # for s in gen_successors(state, turn):
    #     print("evaluation of below state: ", evaluate(s, turn))
    #     s.display()

    # print("testing alpha beta: ")
    # alpha_beta_search(state, turn).display()

    print("testing checkers simulation: ")
    time1 = time.time()
    play(state, 'r')
    time2 = time.time()
    print("elapsed time: ", time2 - time1)

    print(utility(state, 'r', 'b', 1))

    # sys.stdout = open(args.outputfile, 'w') #TODO later uncomment to write to output file 

    sys.stdout = sys.__stdout__

