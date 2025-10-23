from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

# --- Helper to evaluate a move in a separate process ---
def minimax_child_wrapper(args):
    board, alpha, i = args
    b = deepcopy(board)
    b[i] = 'X'
    from minimax_logic import minimax  # local import for multiprocessing safety
    val = minimax(b, 0, alpha, float('inf'), False)
    return val, i

# --- Determine winner or draw ---
def winner(board):
    win_positions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in win_positions:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

# --- Minimax recursive logic with alpha-beta pruning ---
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
                val = minimax(board, depth + 1, alpha, beta, False)
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
                val = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ' '
                best = min(best, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
        return best

# --- Evaluate a single child node (used for sequential/YBWC) ---
def minimax_child(board, i, alpha):
    b = deepcopy(board)
    b[i] = 'X'
    val = minimax(b, 0, alpha, float('inf'), False)
    return val, i

# --- Main parallel minimax driver ---
def parallel_best_move(board):
    moves = [i for i in range(9) if board[i] == ' ']
    if not moves:
        return -1

    # Evaluate first move serially (YBWC: Young Brothers Wait Concept)
    first = moves[0]
    b_first = deepcopy(board)
    b_first[first] = 'X'
    best_val = minimax(b_first, 0, -float('inf'), float('inf'), False)
    best_move = first
    alpha = best_val

    # Parallelize remaining moves
    if len(moves) > 1:
        args = [(board, alpha, i) for i in moves[1:]]
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(minimax_child_wrapper, args))

        for val, idx in results:
            if val > best_val:
                best_val = val
                best_move = idx

    return best_move
