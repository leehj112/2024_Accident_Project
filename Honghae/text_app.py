import streamlit as st

st.title("Take input from the user")
user_input = st.text_input("Say something:")

if user_input:
    st.write("You said", user_input)
