import streamlit as st
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
#st.sidebar.image(logo, use_container_width=True)
#st.title("Ashes")
st.write("Discord Bot For Ages")
name = st.text_input("Enter your name")
if name:
  st.success(f"Welcome, {name}!")