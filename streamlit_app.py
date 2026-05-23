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
    .stButton > button:hover { border-color: #c9a84c; color: #c9a84c; background: transparent; }
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
    thead tr th {
      font-family: 'Syne', sans-serif !important;
      font-size: 0.68rem !important;
      letter-spacing: 0.8px !important;
      color: #555 !important;
      text-transform: uppercase !important;
      background: #0a0a0a !important;
    }
    tbody tr td { font-size: 0.82rem !important; color: #bbb !important; }
    tbody tr:hover td { background: #141414 !important; }
    .stCaption { color: #444 !important; font-size: 0.7rem !important; }
  </style>
""", unsafe_allow_html=True)

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

def render_innings(inning, idx):
  batting_team = inning.get("battingTeam", "—")
  bowling_team = inning.get("bowlingTeam", "—")
  total = inning.get("total", 0)
  wickets = inning.get("wickets", 0)
  overs = inning.get("overs", "0.0")
  st.markdown(f"""
    <div style="margin:1.8rem 0 0.8rem;">
      <div style="font-family:'Syne',sans-serif;font-size:0.6rem;letter-spacing:1.8px;color:#444;text-transform:uppercase;margin-bottom:0.4rem;">Innings {idx}</div>
      <div style="display:flex;align-items:baseline;gap:1rem;flex-wrap:wrap;">
        <span style="font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:700;color:#f0f0f0;">{batting_team}</span>
        <span style="font-family:'Syne',sans-serif;font-size:1.7rem;font-weight:800;color:#c9a84c;">{total}/{wickets}</span>
        <span style="font-size:0.78rem;color:#444;">({overs} ov)</span>
        <span style="font-size:0.7rem;color:#333;margin-left:auto;font-style:italic;">vs {bowling_team}</span>
      </div>
    </div>
    <div style="height:1px;background:linear-gradient(to right,#c9a84c55,#c9a84c11,transparent);margin-bottom:1rem;"></div>
  """, unsafe_allow_html=True)
  batters = inning.get("batters", [])
  if batters:
    st.markdown("<div style='font-family:\"Syne\",sans-serif;font-size:0.6rem;letter-spacing:1.5px;color:#555;text-transform:uppercase;margin-bottom:0.35rem;'>Batting</div>", unsafe_allow_html=True)
    bat_data = [{
      "Batter": b.get("playerName", "—"),
      "R": b.get("runs", 0),
      "B": b.get("balls", 0),
      "4s": b.get("fours", 0),
      "6s": b.get("sixes", 0),
      "SR": b.get("strikeRate", 0.0),
      "Status": "not out" if not b.get("dismissed") else "out",
    } for b in batters]
    st.dataframe(bat_data, use_container_width=True, hide_index=True, column_config={
      "Batter": st.column_config.TextColumn(width="large"),
      "R": st.column_config.NumberColumn(width="small"),
      "B": st.column_config.NumberColumn(width="small"),
      "4s": st.column_config.NumberColumn(width="small"),
      "6s": st.column_config.NumberColumn(width="small"),
      "SR": st.column_config.NumberColumn(format="%.1f", width="small"),
      "Status": st.column_config.TextColumn(width="medium"),
    })
  bowlers = inning.get("bowlers", [])
  if bowlers:
    st.markdown("<div style='font-family:\"Syne\",sans-serif;font-size:0.6rem;letter-spacing:1.5px;color:#555;text-transform:uppercase;margin:1.2rem 0 0.35rem;'>Bowling</div>", unsafe_allow_html=True)
    bowl_data = [{
      "Bowler": b.get("playerName", "—"),
      "O": b.get("overs", "0.0"),
      "R": b.get("runs", 0),
      "W": b.get("wickets", 0),
      "Econ": b.get("economy", 0.0),
    } for b in bowlers]
    st.dataframe(bowl_data, use_container_width=True, hide_index=True, column_config={
      "Bowler": st.column_config.TextColumn(width="large"),
      "O": st.column_config.TextColumn(width="small"),
      "R": st.column_config.NumberColumn(width="small"),
      "W": st.column_config.NumberColumn(width="small"),
      "Econ": st.column_config.NumberColumn(format="%.2f", width="small"),
    })

def page_scorecard(match_id):
  render_header()
  st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
  if st.button("← All Matches"):
    st.query_params.clear()
    st.rerun()
  st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
  with st.spinner("Loading match…"):
    match = fetch_match(match_id)
    scorecard = fetch_scorecard(match_id)
  if not match or "error" in match:
    st.error(f"Match not found: {match_id}")
    return
  team_a = match.get("teamAName", "Team A")
  team_b = match.get("teamBName", "Team B")
  winner = match.get("winner", "—")
  channel = match.get("channelName", "—")
  guild = match.get("guildName", "—")
  mvp = match.get("mvp")
  innings_summary = match.get("innings", [])
  st.markdown(f"""
    <div style="margin-bottom:1rem;">
      <div style="font-family:'Syne',sans-serif;font-size:0.58rem;letter-spacing:2px;color:#3a3a3a;text-transform:uppercase;margin-bottom:0.4rem;">{guild} · #{channel}</div>
      <h2 style="font-size:1.75rem;margin:0;line-height:1.15;color:#f0f0f0;">{team_a} <span style="color:#252525;">vs</span> {team_b}</h2>
    </div>
  """, unsafe_allow_html=True)
  mc1, mc2, mc3 = st.columns([2, 2, 4])
  with mc1:
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700&display=swap" rel="stylesheet">
      <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:8px;padding:0.85rem 1rem;">
        <div style="font-size:0.58rem;letter-spacing:1.2px;color:#3a3a3a;text-transform:uppercase;margin-bottom:0.35rem;font-family:sans-serif;">Winner</div>
        <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#c9a84c;">&#127942; {winner}</div>
      </div>
    """, height=70)
  with mc2:
    avatar = mvp.get("avatar", "") if mvp else ""
    name = mvp.get("name", "—") if mvp else "—"
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600&display=swap" rel="stylesheet">
      <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:8px;padding:0.85rem 1rem;">
        <div style="font-size:0.58rem;letter-spacing:1.2px;color:#3a3a3a;text-transform:uppercase;margin-bottom:0.35rem;font-family:sans-serif;">MVP</div>
        <div style="display:flex;align-items:center;gap:0.5rem;">
          <img src="{avatar}" style="width:20px;height:20px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
          <span style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:600;color:#e0e0e0;">{name}</span>
        </div>
      </div>
    """, height=70)
  with mc3:
    if innings_summary:
      pills = ""
      for inn in innings_summary:
        pills += (
          '<div style="flex:1;min-width:110px;">'
          '<div style="font-size:0.58rem;letter-spacing:1px;color:#3a3a3a;text-transform:uppercase;margin-bottom:0.2rem;font-family:sans-serif;">' + str(inn["battingTeam"]) + '</div>'
          '<div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:#ddd;">' + str(inn["runs"]) + '/' + str(inn["wickets"]) +
          ' <span style="font-size:0.7rem;color:#444;font-weight:400;">(' + str(inn["overs"]) + ')</span></div>'
          '</div>'
        )
      components.html(f"""
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700&display=swap" rel="stylesheet">
        <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:8px;padding:0.85rem 1rem;display:flex;gap:1.5rem;flex-wrap:wrap;">
          {pills}
        </div>
      """, height=70)
  st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
  st.markdown("<div style='height:2px;background:linear-gradient(90deg,#c9a84c44,#c9a84c88,#c9a84c44);border-radius:2px;'></div>", unsafe_allow_html=True)
  innings_data = scorecard.get("innings", [])
  if not innings_data:
    st.markdown("<p style='color:#333;margin-top:2rem;font-size:0.85rem;text-align:center;'>No scorecard data available yet.</p>", unsafe_allow_html=True)
    return
  for i, inning in enumerate(innings_data, 1):
    render_innings(inning, i)
    if i < len(innings_data):
      st.markdown("<div style='height:1px;background:#111;margin:0.5rem 0 0;'></div>", unsafe_allow_html=True)

def page_list():
  render_header()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  query = st.text_input("", placeholder="Search by team, channel, or winner…", label_visibility="collapsed")
  matches = fetch_matches(query if query else None)
  st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
  if not matches:
    st.markdown("<p style='color:#2a2a2a;font-size:0.85rem;text-align:center;margin-top:3rem;'>No matches found.</p>", unsafe_allow_html=True)
    return
  for match in matches:
    mid = match["id"]
    c1, c2 = st.columns([11, 1])
    with c1:
      st.markdown(f"""
        <div style="background:#0b0b0b;border:1px solid #191919;border-radius:8px;padding:0.9rem 1.2rem;margin-bottom:0.05rem;">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
            <div>
              <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#e8e8e8;margin-bottom:0.15rem;">
                {match['teamAName']} <span style="color:#252525;font-weight:300;">vs</span> {match['teamBName']}
              </div>
              <div style="font-size:0.7rem;color:#383838;">{match['channelName']} &nbsp;·&nbsp; {match['guildName']}</div>
            </div>
            <div style="display:inline-flex;align-items:center;background:#0f0f00;border:1px solid #c9a84c33;color:#c9a84c;font-size:0.68rem;font-family:'Syne',sans-serif;font-weight:600;padding:0.18rem 0.55rem;border-radius:3px;letter-spacing:0.4px;white-space:nowrap;">
              🏆 {match['winner']}
            </div>
          </div>
        </div>
      """, unsafe_allow_html=True)
    with c2:
      st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
      if st.button("View", key=mid):
        st.query_params["id"] = mid
        st.rerun()
    st.markdown("<div style='height:0.15rem'></div>", unsafe_allow_html=True)

params = st.query_params
match_id = params.get("id", None)

if match_id:
  page_scorecard(match_id)
else:
  page_list()
