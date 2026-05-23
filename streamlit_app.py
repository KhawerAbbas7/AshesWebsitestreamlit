import streamlit as st
import requests
from datetime import datetime

logo = "40ef4cf2ee6a72db2a5af55c231192bd.png"

st.set_page_config(
  page_title="Ashes",
  page_icon=logo,
  layout="wide"
)

@st.cache_data(ttl=30)
def fetch_matches(query:str= None):
  try:
    if query:
      r = requests.get(f"http://51.75.118.79:20375/matches/getrecent?recent=10&query={query}", timeout=5)
    else:
      r = requests.get("http://51.75.118.79:20375/matches/getrecent?recent=10", timeout=5)
    return r.json()
  except:
    return {"Matches": []}

col1, col2 = st.columns([1, 10])

with col1:
  st.image(logo, width=60)

with col2:
  st.title("Ashes")
  st.caption("Discord Bot Match Dashboard")

st.divider()

data = fetch_matches()

matches = data.get("Matches", [])

if not matches:
  st.info("No recent matches found.")
else:
  for match in matches:

    ts = match.get("timestamp", 0)
    dt = datetime.fromtimestamp(ts / 1000 if ts > 10**12 else ts)

    with st.container():
      col1, col2, col3 = st.columns([4, 1, 2])

      with col1:
        st.subheader(f"{match.get('teamAName')} vs {match.get('teamBName')}")
        st.write(f"📢 {match.get('channelName')}")
        st.caption(match.get("guildName"))

      with col2:
        st.metric("Winner", match.get("winner", "N/A"))

      with col3:
        st.caption("Match Time")
        st.write(dt.strftime("%d %b %Y, %I:%M %p"))

      st.divider()