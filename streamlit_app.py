import streamlit as st
import requests 
logo= "40ef4cf2ee6a72db2a5af55c231192bd.png"
st.set_page_config(layout="wide")
st.set_page_config(
  page_title="Ashes",
  page_icon=logo,
  layout="wide"
)
col1, col2 = st.columns([1, 8])
with col1:
  st.image(logo, width=60)
with col2:
  st.markdown("## Ashes")

st.write("Discord Bot For Ages")
data = requests.get("https://api.codetabs.com/v1/proxy?quest=http://51.75.118.79:20375/matches/getrecent")
st.write(data)
name = st.text_input("Enter your name")
if name:
  st.success(f"Welcome, {name}!")