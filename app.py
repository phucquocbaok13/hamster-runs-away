import random
import streamlit as st

st.set_page_config(page_title="Tro choi Do So", page_icon="🎮")

st.title("🎮 Tro choi: Do So Tu 1 den 100")
st.write(
    "He thong da chon mot so ngau nhiên tu 1 den 100. Hay thu doan xem do la so nao!"
)

# Khoi tao trang thai tro choi
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

# O nhap so tu nguoi choi
guess = st.number_input(
    "Nhap so ban doan:",
    min_value=1,
    max_value=100,
    step=1,
    disabled=st.session_state.game_over,
)

if st.button("Kiem tra", disabled=st.session_state.game_over):
    st.session_state.attempts += 1

    if guess < st.session_state.target_number:
        st.warning("So cua ban nho hon ket qua! Hay thu so lon hon.")
    elif guess > st.session_state.target_number:
        st.warning("So cua ban lon hon ket qua! Hay thu so nho hon.")
    else:
        st.balloons()
        st.success(
            f"Chuc mung! Ban da doan dung so {st.session_state.target_number} sau {st.session_state.attempts} lan thu!"
        )
        st.session_state.game_over = True

# Nut choi lai
if st.button("Choi lai"):
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.rerun()
