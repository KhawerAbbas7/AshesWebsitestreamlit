import streamlit as st
import requests
import streamlit.components.v1 as components
from datetime import datetime

logo = "40ef4cf2ee6a72db2a5af55c231192bd.png"
BASE = "http://51.75.118.79:20375"

st.set_page_config(page_title="Ashes", page_icon=logo, layout="wide")

st.markdown("""
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');
    html, body, [class*="css"] { font-family: 'DM Mono', monospace; background: #080808; }
    .block-container { padding: 2rem 3rem 4rem; max-width: 1080px; }
    h1 { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; margin: 0; color: #f0f0f0; }
    h2, h3 { font-family: 'Syne', sans-serif; font-weight: 700; color: #f0f0f0; }
    .stButton > button {
      background: transparent;
      border: 1px solid #2a2a2a;
      color: #888;
      font-family: 'DM Mono', monospace;
      font-size: 0.73rem;
      padding: 0.3rem 0.85rem;
      border-radius: 4px;
      transition: all 0.15s;
      letter-spacing: 0.3px;
    }
    .stButton > button:hover { border-color: #c9a84c; color: #c9a84c; background: #14110000; }
    .stTextInput > div > input {
      background: #0e0e0e;
      border: 1px solid #252525;
      color: #ccc;
      font-family: 'DM Mono', monospace;
      font-size: 0.82rem;
      border-radius: 6px;
      padding: 0.5rem 0.8rem;
    }
    .stTextInput > div > input:focus { border-color: #c9a84c; box-shadow: 0 0 0 1px #c9a84c44; }
    .stDataFrame { background: #0e0e0e; }
    thead tr th {
      font-family: 'Syne', sans-serif !important;
      font-size: 0.7rem !important;
      letter-spacing: 0.8px !important;
      color: #555 !important;
      text-transform: uppercase !important;
      background: #0a0a0a !important;
    }
    tbody tr td { font-size: 0.82rem !important; color: #bbb !important; }
    tbody tr:hover td { background: #141414 !important; }
    .stCaption { color: #444 !important; font-size: 0.7rem !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }
  </style>
""", unsafe_allow_html=True)

def local_time_html(ts):
  components.html(f"""
    <span style="font-family:'DM Mono',monospace;font-size:0.8rem;color:#555;" id="t"></span>
    <script>
      const ts={ts};
      const d=new Date(ts<1e12?ts*1000:ts);
      document.getElementById("t").innerText=d.toLocaleString(undefined,{{weekday:'short',year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}});
    </script>
  """, height=28)

@st.cache_data(ttl=30)
def fetch_matches(query=None):
  try:
    params = {"recent": 20}
    if query:
      params["query"] = query
    r = requests.get(f"{BASE}/matches/getrecent", params=params, timeout=5)
    return r.json().get("Matches", [])
  except Exception:
    return []

@st.cache_data(ttl=60)
def fetch_scorecard(match_id):
  try:
    r = requests.get(f"{BASE}/matches/{match_id}/scorecard", timeout=8)
    return r.json()
  except Exception:
    return {}

@st.cache_data(ttl=60)
def fetch_match(match_id):
  try:
    r = requests.get(f"{BASE}/matches/{match_id}", timeout=8)
    return r.json()
  except Exception:
    return {}

def render_header():
  c1, c2 = st.columns([1, 11])
  with c1:
    st.image(logo, width=48)
  with c2:
    st.title("Ashes")
    st.caption("Discord Bot Match Dashboard")

def render_innings_scorecard(inning, idx):
  batting_team = inning.get("battingTeam", "—")
  bowling_team = inning.get("bowlingTeam", "—")
  total = inning.get("total", 0)
  wickets = inning.get("wickets", 0)
  overs = inning.get("overs", "0.0")
  st.markdown(f"""
    <div style="margin:1.5rem 0 0.6rem;">
      <div style="font-family:'Syne',sans-serif;font-size:0.65rem;letter-spacing:1.5px;color:#555;text-transform:uppercase;margin-bottom:0.25rem;">
        Innings {idx}
      </div>
      <div style="display:flex;align-items:baseline;gap:1rem;flex-wrap:wrap;">
        <span style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:#f0f0f0;">{batting_team}</span>
        <span style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#c9a84c;">{total}/{wickets}</span>
        <span style="font-size:0.8rem;color:#555;">({overs} ov)</span>
        <span style="font-size:0.75rem;color:#444;margin-left:auto;">bowl: {bowling_team}</span>
      </div>
    </div>
    <div style="height:1px;background:linear-gradient(to right,#c9a84c33,transparent);margin-bottom:1rem;"></div>
  """, unsafe_allow_html=True)
  batters = inning.get("batters", [])
  if batters:
    st.markdown("<div style='font-family:\"Syne\",sans-serif;font-size:0.65rem;letter-spacing:1.2px;color:#666;text-transform:uppercase;margin-bottom:0.4rem;'>Batting</div>", unsafe_allow_html=True)
    bat_data = []
    for b in batters:
      status = "†" if not b.get("dismissed") else "out"
      bat_data.append({
        "Batter": b.get("playerName", "—"),
        "R": b.get("runs", 0),
        "B": b.get("balls", 0),
        "4s": b.get("fours", 0),
        "6s": b.get("sixes", 0),
        "SR": b.get("strikeRate", 0.0),
        "": status,
      })
    st.dataframe(bat_data, use_container_width=True, hide_index=True, column_config={
      "Batter": st.column_config.TextColumn(width="large"),
      "R": st.column_config.NumberColumn(width="small"),
      "B": st.column_config.NumberColumn(width="small"),
      "4s": st.column_config.NumberColumn(width="small"),
      "6s": st.column_config.NumberColumn(width="small"),
      "SR": st.column_config.NumberColumn(format="%.1f", width="small"),
      "": st.column_config.TextColumn(width="small"),
    })
  bowlers = inning.get("bowlers", [])
  if bowlers:
    st.markdown("<div style='font-family:\"Syne\",sans-serif;font-size:0.65rem;letter-spacing:1.2px;color:#666;text-transform:uppercase;margin:1rem 0 0.4rem;'>Bowling</div>", unsafe_allow_html=True)
    bowl_data = []
    for b in bowlers:
      bowl_data.append({
        "Bowler": b.get("playerName", "—"),
        "O": b.get("overs", "0.0"),
        "R": b.get("runs", 0),
        "W": b.get("wickets", 0),
        "Econ": b.get("economy", 0.0),
      })
    st.dataframe(bowl_data, use_container_width=True, hide_index=True, column_config={
      "Bowler": st.column_config.TextColumn(width="large"),
      "O": st.column_config.TextColumn(width="small"),
      "R": st.column_config.NumberColumn(width="small"),
      "W": st.column_config.NumberColumn(width="small"),
      "Econ": st.column_config.NumberColumn(format="%.2f", width="small"),
    })

def page_scorecard(match_id):
  render_header()
  st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
  if st.button("← All Matches"):
    st.query_params.clear()
    st.rerun()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  match = fetch_match(match_id)
  scorecard = fetch_scorecard(match_id)
  if "error" in match or not match:
    st.error("Match not found.")
    return
  team_a = match.get("teamAName", "Team A")
  team_b = match.get("teamBName", "Team B")
  winner = match.get("winner", "—")
  channel = match.get("channelName", "—")
  guild = match.get("guildName", "—")
  mvp = match.get("mvp")
  st.markdown(f"""
    <div style="margin-bottom:0.25rem;">
      <div style="font-family:'Syne',sans-serif;font-size:0.6rem;letter-spacing:2px;color:#444;text-transform:uppercase;margin-bottom:0.5rem;">{guild} · {channel}</div>
      <h2 style="font-size:1.8rem;margin:0;line-height:1.1;">{team_a} <span style="color:#333;">vs</span> {team_b}</h2>
    </div>
  """, unsafe_allow_html=True)
  mc1, mc2, mc3 = st.columns([2, 2, 3])
  with mc1:
    st.markdown(f"""
      <div style="background:#0e0e0e;border:1px solid #1a1a1a;border-radius:8px;padding:0.8rem 1rem;">
        <div style="font-size:0.6rem;letter-spacing:1.2px;color:#444;text-transform:uppercase;margin-bottom:0.3rem;">Winner</div>
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#c9a84c;">🏆 {winner}</div>
      </div>
    """, unsafe_allow_html=True)
  with mc2:
    if mvp:
      st.markdown(f"""
        <div style="background:#0e0e0e;border:1px solid #1a1a1a;border-radius:8px;padding:0.8rem 1rem;">
          <div style="font-size:0.6rem;letter-spacing:1.2px;color:#444;text-transform:uppercase;margin-bottom:0.3rem;">MVP</div>
          <div style="display:flex;align-items:center;gap:0.5rem;">
            <img src="{mvp.get('avatar','')}" style="width:22px;height:22px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
            <span style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:600;color:#f0f0f0;">{mvp.get('name','—')}</span>
          </div>
        </div>
      """, unsafe_allow_html=True)
  with mc3:
    innings_list = match.get("innings", [])
    if innings_list:
      summary_html = '<div style="background:#0e0e0e;border:1px solid #1a1a1a;border-radius:8px;padding:0.8rem 1rem;display:flex;gap:1.5rem;flex-wrap:wrap;">'
      for inn in innings_list:
        summary_html += f"""
          <div>
            <div style="font-size:0.58rem;letter-spacing:1px;color:#444;text-transform:uppercase;">{inn['battingTeam']}</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#e0e0e0;">{inn['runs']}/{inn['wickets']} <span style="font-size:0.72rem;color:#555;font-weight:400;">({inn['overs']})</span></div>
          </div>
        """
      summary_html += '</div>'
      st.markdown(summary_html, unsafe_allow_html=True)
  st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
  st.markdown("<div style='height:2px;background:linear-gradient(to right,#c9a84c22,#c9a84c55,#c9a84c22);border-radius:2px;'></div>", unsafe_allow_html=True)
  innings_data = scorecard.get("innings", [])
  if not innings_data:
    st.markdown("<p style='color:#444;margin-top:2rem;font-size:0.85rem;'>No scorecard data available.</p>", unsafe_allow_html=True)
    return
  for i, inning in enumerate(innings_data, 1):
    render_innings_scorecard(inning, i)
    if i < len(innings_data):
      st.markdown("<div style='height:1px;background:#141414;margin:1.5rem 0;'></div>", unsafe_allow_html=True)

def page_list():
  render_header()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  query = st.text_input("", placeholder="Search matches…", label_visibility="collapsed")
  matches = fetch_matches(query if query else None)
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  if not matches:
    st.markdown("<p style='color:#333;font-size:0.85rem;text-align:center;margin-top:3rem;'>No matches found.</p>", unsafe_allow_html=True)
    return
  for match in matches:
    ts = match.get("timestamp", 0)
    mid = match["id"]
    c1, c2 = st.columns([10, 1])
    with c1:
      st.markdown(f"""
        <div style="background:#0b0b0b;border:1px solid #1c1c1c;border-radius:8px;padding:1rem 1.2rem;margin-bottom:0.1rem;transition:border-color 0.2s;">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
            <div>
              <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#eee;">{match['teamAName']} <span style="color:#2a2a2a;font-weight:400;">vs</span> {match['teamBName']}</div>
              <div style="font-size:0.72rem;color:#444;margin-top:0.2rem;">{match['channelName']} · {match['guildName']}</div>
            </div>
            <div style="text-align:right;">
              <div style="display:inline-block;background:#111;border:1px solid #c9a84c44;color:#c9a84c;font-size:0.7rem;font-family:'Syne',sans-serif;font-weight:600;padding:0.2rem 0.6rem;border-radius:3px;letter-spacing:0.5px;">🏆 {match['winner']}</div>
            </div>
          </div>
        </div>
      """, unsafe_allow_html=True)
    with c2:
      st.markdown("<div style='height:0.85rem'></div>", unsafe_allow_html=True)
      if st.button("View", key=mid):
        st.query_params["id"] = mid
        st.rerun()
    st.markdown("<div style='height:0.1rem'></div>", unsafe_allow_html=True)

params = st.query_params
match_id = params.get("id", None)

if match_id:
  page_scorecard(match_id)
else:
  page_list()
