import streamlit as st

st.title("My First Web App")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}! 👋")

st.button("Click me")