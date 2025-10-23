# app.py
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

import streamlit as st
from minimax_logic import parallel_best_move, winner

# Initialize the board in session state
if "board" not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
if "turn" not in st.session_state:
    st.session_state.turn = "O"  # User starts as O

st.title("🎮 Tic-Tac-Toe with Minimax AI (YBWC Parallel)")
st.subheader("Play against an AI that uses parallel minimax search!")

def reset_board():
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.turn = "O"

# Render game board
cols = st.columns(3)
for i in range(9):
    col = cols[i % 3]
    with col:
        if st.button(st.session_state.board[i] or " ", key=i):
            if st.session_state.board[i] == ' ' and st.session_state.turn == 'O':
                st.session_state.board[i] = 'O'
                res = winner(st.session_state.board)
                if not res:
                    st.session_state.turn = 'X'
                    ai_move = parallel_best_move(st.session_state.board)
                    if ai_move != -1:
                        st.session_state.board[ai_move] = 'X'
                    res = winner(st.session_state.board)
                if res:
                    st.success(f"Game Over! Result: {res}")
                    st.button("Restart Game", on_click=reset_board)

# Display the current board
st.write(f"Your Turn: {st.session_state.turn}")
cols = st.columns(3)
for i in range(0,9,3):
    st.write(" | ".join(st.session_state.board[i:i+3]))
