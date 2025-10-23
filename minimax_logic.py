# minimax_logic.py
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

# Tic-Tac-Toe board evaluation functions
def winner(board):
    win_positions = [(0,1,2),(3,4,5),(6,7,8),
                     (0,3,6),(1,4,7),(2,5,8),
                     (0,4,8),(2,4,6)]
    for a,b,c in win_positions:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

def minimax(board, depth, alpha, beta, is_max):
    res = winner(board)
    if res == 'X':
        return 1
    elif res == 'O':
        return -1
    elif res == 'Draw':
        return 0

    if is_max:
        best = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                val = minimax(board, depth+1, alpha, beta, False)
                board[i] = ' '
                best = max(best, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                val = minimax(board, depth+1, alpha, beta, True)
                board[i] = ' '
                best = min(best, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
        return best

# Helper for parallel
def minimax_child(board, i, alpha):
    b = deepcopy(board)
    b[i] = 'X'
    val = minimax(b, 0, alpha, float('inf'), False)
    return val, i

def with ProcessPoolExecutor() as executor:
    results = list(executor.map(lambda i: minimax_child(board, i, alpha), moves[1:]))
    # Helper global variable to pass board and alpha
_global_board = None
_global_alpha = None

def _init_globals(board, alpha):
    global _global_board, _global_alpha
    _global_board = board
    _global_alpha = alpha

def _worker(i):
    from copy import deepcopy
    b = deepcopy(_global_board)
    b[i] = 'X'
    from minimax_logic import minimax  # Import here for safety in subprocess
    val = minimax(b, 0, _global_alpha, float('inf'), False)
    return val, i

def parallel_best_move(board):
    moves = [i for i in range(9) if board[i] == ' ']
    if not moves:
        return -1

    # Evaluate first move to setup alpha
    first = moves[0]
    board[first] = 'X'
    best_val = minimax(board, 0, -float('inf'), float('inf'), False)
    board[first] = ' '
    best_move = first
    alpha = best_val

    with ProcessPoolExecutor(initializer=_init_globals, initargs=(board, alpha)) as executor:
        results = list(executor.map(_worker, moves[1:]))

    for val, idx in results:
        if val > best_val:
            best_val = val
            best_move = idx
    return best_move
