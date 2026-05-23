import streamlit as st
st.set_page_config(layout="wide")
st.title("My First App")
st.write("Hello, Streamlit!")
name = st.text_input("Enter your name")
if name:
  st.success(f"Welcome, {name}!")