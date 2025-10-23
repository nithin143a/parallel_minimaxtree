# app.py
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
