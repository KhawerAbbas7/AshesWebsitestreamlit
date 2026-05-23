import streamlit as st
st.set_page_config(layout="wide")
st.title("Ashes")
st.write("Discord Bot For Ages")
name = st.text_input("Enter your name")
if name:
  st.success(f"Welcome, {name}!")