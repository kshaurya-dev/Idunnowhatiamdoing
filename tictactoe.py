import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0

def minimax(board):
    current_player = player(board)

    # Helper function to find the best score for X
    def max_value(board):
        if terminal(board):
            return utility(board), None
        
        best_score = -math.inf
        best_move = None
        for move in actions(board):
            score, _ = min_value(result(board, move))
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    # Helper function to find the best score for O
    def min_value(board):
        if terminal(board):
            return utility(board), None
        
        best_score = math.inf
        best_move = None
        for move in actions(board):
            score, _ = max_value(result(board, move))
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    if terminal(board):
        return None

    if current_player == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)
    
    return move


