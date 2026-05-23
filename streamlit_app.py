import streamlit as st
import requests,json
from datetime import datetime
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
data = requests.get("http://51.75.118.79:20375/matches/getrecent").json()
for match in data["Matches"]:
  col1, col2 = st.columns([3, 1])
  ts = match["timestamp"]
  dt = datetime.fromtimestamp(ts / 1000 if ts > 10**12 else ts)
  with col1:
    st.subheader(f"{match['teamAName']} vs {match['teamBName']}")
    st.write(match["channelName"])
    st.caption(match["guildName"])
  with col2:
    st.metric("Winner", match["winner"])
    st.caption(dt.strftime("%Y-%m-%d %H:%M")))
