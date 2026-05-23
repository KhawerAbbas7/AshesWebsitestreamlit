import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components
logo="40ef4cf2ee6a72db2a5af55c231192bd.png"
st.set_page_config(page_title="Ashes",page_icon=logo,layout="wide")
def show_local_time(ts):
  components.html(f"""
  <div style="font-size:14px;color:#aaa;">
    <span id="time"></span>
  </div>

  <script>
    const ts = {ts};
    const d = new Date(ts < 1e12 ? ts*1000 : ts);
    document.getElementById("time").innerText = d.toLocaleString();
  </script>
  """, height=40)
if "page" not in st.session_state:
  st.session_state.page="list"
if "selected_match" not in st.session_state:
  st.session_state.selected_match=None

@st.cache_data(ttl=30)
def fetch_matches(query=None):
  try:
    params={"recent":10}
    if query:
      params["query"]=query
    r=requests.get("http://51.75.118.79:20375/matches/getrecent",params=params,timeout=5)
    return r.json()
  except:
    return {"Matches":[]}

data=fetch_matches()
matches=data.get("Matches",[])

col1,col2=st.columns([1,8])
with col1:
  st.image(logo,width=60)
with col2:
  st.title("Ashes")
  st.caption("Discord Bot Match Dashboard")

query=st.text_input("Search matches")

if st.session_state.page=="list":
  filtered=matches
  if query:
    data=fetch_matches(query)
    filtered=data.get("Matches",[])
  for match in filtered:
    col1,col2,col3=st.columns([4,1,1])
    ts=match.get("timestamp",0)
    
    with col1:
      st.subheader(f"{match['teamAName']} vs {match['teamBName']}")
      st.write(match["channelName"])
      st.caption(match["guildName"])
    with col2:
      st.metric("Winner",match["winner"])
    with col3:
      if st.button("View",key=match["id"]):
        st.session_state.selected_match=match
        st.session_state.page="details"
        st.rerun()
    st.divider()

if st.session_state.page=="details":
  match=st.session_state.selected_match
  if st.button("⬅ Back"):
    st.session_state.page="list"
    st.rerun()
  st.title("Match Details")
  st.divider()
  st.subheader(f"{match['teamAName']} vs {match['teamBName']}")
  st.write("Channel:",match["channelName"])
  st.write("Guild:",match["guildName"])
  st.write("Winner:",match["winner"])
  ts=match["timestamp"]
  dt=datetime.fromtimestamp(ts/1000 if ts>10**12 else ts)
  st.write("Time:")
  show_local_time(match["timestamp"])