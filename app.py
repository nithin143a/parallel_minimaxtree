import streamlit as st
from minimax_logic import parallel_best_move, winner

# --- Initialize session state ---
if "board" not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
if "turn" not in st.session_state:
    st.session_state.turn = "O"
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "result" not in st.session_state:
    st.session_state.result = None

# --- UI ---
st.title("🎮 Tic-Tac-Toe with Minimax AI (Parallel)")
st.subheader("Play against an AI using parallel minimax search!")

# --- Reset function ---
def reset_board():
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.turn = "O"
    st.session_state.game_over = False
    st.session_state.result = None

# --- Display board and handle moves ---
cols = st.columns(3)
for i in range(9):
    col = cols[i % 3]
    with col:
        if st.button(st.session_state.board[i] or " ", key=i, use_container_width=True):
            if not st.session_state.game_over and st.session_state.board[i] == ' ' and st.session_state.turn == 'O':
                # Player move
                st.session_state.board[i] = 'O'
                res = winner(st.session_state.board)

                if res:
                    st.session_state.game_over = True
                    st.session_state.result = res
                else:
                    # AI move
                    st.session_state.turn = 'X'
                    ai_move = parallel_best_move(st.session_state.board)
                    if ai_move != -1:
                        st.session_state.board[ai_move] = 'X'

                    res = winner(st.session_state.board)
                    if res:
                        st.session_state.game_over = True
                        st.session_state.result = res
                    else:
                        st.session_state.turn = 'O'

# --- Show result if game over ---
if st.session_state.game_over:
    st.success(f"Game Over! Result: {st.session_state.result}")
    st.button("🔁 Play Again", on_click=reset_board)
else:
    st.write(f"Your Turn: {st.session_state.turn}")

# --- Display text board below ---
st.write("### Board State:")
for i in range(0, 9, 3):
    st.write(" | ".join(st.session_state.board[i:i+3]))
