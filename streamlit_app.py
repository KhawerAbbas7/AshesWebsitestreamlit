import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components
logo = "40ef4cf2ee6a72db2a5af55c231192bd.png"
st.set_page_config(page_title="Ashes", page_icon=logo, layout="wide")
st.markdown("""
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400&display=swap');
    html, body, [class*="css"] { font-family: 'DM Mono', monospace; }
    .block-container { padding: 2rem 3rem; max-width: 1100px; }
    h1 { font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 800; letter-spacing: -1px; margin: 0; }
    h2, h3 { font-family: 'Syne', sans-serif; font-weight: 700; }
    .match-card {
      background: #0f0f0f;
      border: 1px solid #222;
      border-radius: 10px;
      padding: 1.2rem 1.5rem;
      margin-bottom: 1rem;
      transition: border-color 0.2s;
    }
    .match-card:hover { border-color: #e8c84a; }
    .match-title { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700; color: #f5f5f5; margin-bottom: 0.15rem; }
    .match-sub { font-size: 0.78rem; color: #666; }
    .winner-badge {
      display: inline-block;
      background: #1a1a0a;
      border: 1px solid #e8c84a;
      color: #e8c84a;
      font-size: 0.75rem;
      font-family: 'Syne', sans-serif;
      font-weight: 600;
      padding: 0.25rem 0.65rem;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }
    .stButton > button {
      background: transparent;
      border: 1px solid #333;
      color: #aaa;
      font-family: 'DM Mono', monospace;
      font-size: 0.75rem;
      padding: 0.35rem 0.9rem;
      border-radius: 4px;
      transition: all 0.15s;
    }
    .stButton > button:hover { border-color: #e8c44a; color: #e8c44a; background: #1a1900; }
    .stTextInput > div > input {
      background: #0f0f0f;
      border: 1px solid #2a2a2a;
      color: #ddd;
      font-family: 'DM Mono', monospace;
      font-size: 0.82rem;
      border-radius: 6px;
    }
    .stTextInput > div > input:focus { border-color: #e8c44a; box-shadow: 0 0 0 1px #e8c44a33; }
    .detail-row { display: flex; gap: 0.5rem; align-items: baseline; margin-bottom: 0.5rem; }
    .detail-label { color: #555; font-size: 0.78rem; min-width: 80px; }
    .detail-value { color: #ccc; font-size: 0.85rem; }
    .stCaption { color: #555 !important; font-size: 0.72rem !important; }
    .stDivider { border-color: #1e1e1e !important; }
    [data-testid="stMetricValue"] { font-family: 'Syne', sans-serif; font-size: 1rem !important; color: #e8c44a !important; }
    [data-testid="stMetricLabel"] { font-size: 0.7rem !important; color: #555 !important; }
  </style>
""", unsafe_allow_html=True)
def show_local_time(ts):
  components.html(f"""
  <div style="font-family:'DM Mono',monospace;font-size:0.85rem;color:#888;padding:0;">
    <span id="t"></span>
  </div>
  <script>
    const ts={ts};
    const d=new Date(ts<1e12?ts*1000:ts);
    document.getElementById("t").innerText=d.toLocaleString(undefined,{{weekday:"short",year:"numeric",month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"}});
  </script>
  """, height=30)
if "page" not in st.session_state:
  st.session_state.page = "list"
if "selected_match" not in st.session_state:
  st.session_state.selected_match = None
@st.cache_data(ttl=30)
def fetch_matches(query=None):
  try:
    params = {"recent": 10}
    if query:
      params["query"] = query
    r = requests.get("http://51.75.118.79:20375/matches/getrecent", params=params, timeout=5)
    return r.json()
  except Exception:
    return {"Matches": []}
header_col1, header_col2 = st.columns([1, 10])
with header_col1:
  st.image(logo, width=52)
with header_col2:
  st.title("Ashes")
  st.caption("Discord Bot Match Dashboard")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
if st.session_state.page == "list":
  query = st.text_input("", placeholder="Search matches…", label_visibility="collapsed")
  data = fetch_matches(query if query else None)
  matches = data.get("Matches", [])
  if not matches:
    st.markdown("<p style='color:#444;font-size:0.85rem;margin-top:2rem;text-align:center;'>No matches found.</p>", unsafe_allow_html=True)
  for match in matches:
    left, right = st.columns([7, 1])
    with left:
      st.markdown(f"""
        <div class="match-card">
          <div class="match-title">{match['teamAName']} vs {match['teamBName']}</div>
          <div class="match-sub">{match['channelName']} &nbsp;·&nbsp; {match['guildName']}</div>
          <div style="margin-top:0.6rem"><span class="winner-badge">🏆 {match['winner']}</span></div>
        </div>
      """, unsafe_allow_html=True)
    with right:
      st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)
      if st.button("View →", key=match["id"]):
        st.session_state.selected_match = match
        st.session_state.page = "details"
        st.rerun()
if st.session_state.page == "details":
  match = st.session_state.selected_match
  if st.button("← Back"):
    st.session_state.page = "list"
    st.rerun()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  st.markdown(f"<h2 style='margin-bottom:0.1rem'>{match['teamAName']} vs {match['teamBName']}</h2>", unsafe_allow_html=True)
  st.markdown("<hr style='border-color:#1e1e1e;margin:0.6rem 0 1rem'>", unsafe_allow_html=True)
  ts = match.get("timestamp", 0)
  fields = [
    ("Channel", match.get("channelName", "—")),
    ("Guild", match.get("guildName", "—")),
    ("Winner", match.get("winner", "—")),
  ]
  for label, value in fields:
    st.markdown(f"""
      <div class="detail-row">
        <span class="detail-label">{label}</span>
        <span class="detail-value">{value}</span>
      </div>
    """, unsafe_allow_html=True)
  st.markdown("<div class='detail-label' style='margin-bottom:0.25rem'>Time</div>", unsafe_allow_html=True)
  show_local_time(ts)
