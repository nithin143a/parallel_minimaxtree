from concurrent.futures import ProcessPoolExecutor

# ✅ helper must be top-level so it's picklable
def minimax_child_wrapper(args):
    board, move, alpha = args
    return minimax_child(board, move, alpha)

def parallel_best_move(board):
    moves = [i for i in range(9) if board[i] == ' ']
    if not moves:
        return -1

    alpha = float('-inf')
    best_score = float('-inf')
    best_move = -1

    # Evaluate the first move serially (YBWC)
    first_move = moves[0]
    best_score = minimax_child(board, first_move, alpha)
    best_move = first_move
    alpha = max(alpha, best_score)

    # Parallelize the remaining moves
    if len(moves) > 1:
        with ProcessPoolExecutor() as executor:
            args_list = [(board, move, alpha) for move in moves[1:]]
            results = list(executor.map(minimax_child_wrapper, args_list))

        for move, score in zip(moves[1:], results):
            if score > best_score:
                best_score = score
                best_move = move

    return best_move
