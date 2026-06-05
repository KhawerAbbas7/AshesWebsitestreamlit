import streamlit as st
import requests
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

logo = "40ef4cf2ee6a72db2a5af55c231192bd.png"
BASE = "http://129.80.180.202:20375"
st.set_page_config(page_title="Ashes", page_icon=logo, layout="wide")
st.markdown("""
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif;
      background: #0a0a0a;
      color: #e8e8e8;
    }

    .block-container {
      padding: 1.5rem 2rem 4rem;
      max-width: 1080px;
      background: #111111;
      box-shadow: 0 0 0 1px #222, 0 8px 32px rgba(0,0,0,0.6);
      margin-top: 1rem;
      border-top: 3px solid #CC0000;
    }

    /* Hide default streamlit image caption gap */
    [data-testid="stImage"] { margin-bottom: 0 !important; }

    h1 {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 2.6rem;
      letter-spacing: 3px;
      margin: 0 !important;
      padding: 0 !important;
      color: #CC0000;
      line-height: 1;
    }

    /* Collapse gap under h1 */
    h1 + div, h1 + p { margin-top: 0 !important; }

    h2, h3 {
      font-weight: 700;
      color: #e8e8e8;
    }

    /* Caption under title */
    [data-testid="stCaptionContainer"] p {
      font-family: 'DM Mono', monospace !important;
      font-size: 0.65rem !important;
      color: #444 !important;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-top: 0 !important;
    }

    .stButton > button {
      background: #CC0000;
      border: none;
      color: #fff;
      font-family: 'DM Mono', monospace;
      font-size: 0.75rem;
      font-weight: 500;
      padding: 0.45rem 1.1rem;
      border-radius: 2px;
      text-transform: uppercase;
      letter-spacing: 1px;
      transition: background 0.15s, box-shadow 0.15s;
    }

    .stButton > button:hover {
      background: #e60000;
      box-shadow: 0 0 12px rgba(204,0,0,0.4);
      color: #fff;
    }

    .stTextInput > div > input {
      background: #1a1a1a;
      border: 1px solid #2a2a2a;
      color: #e8e8e8;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.9rem;
      border-radius: 2px;
      padding: 0.5rem 0.8rem;
    }

    .stTextInput > div > input::placeholder { color: #555; }

    .stTextInput > div > input:focus {
      border-color: #CC0000;
      box-shadow: 0 0 0 1px #CC0000;
    }

    table.custom-table {
      width: 100%;
      border-collapse: collapse;
      background: #111;
      margin-bottom: 1rem;
    }

    table.custom-table th {
      border-bottom: 1px solid #222;
      padding: 0.6rem;
      color: #555;
      font-family: 'DM Mono', monospace;
      font-size: 0.7rem;
      text-transform: uppercase;
      text-align: left;
      font-weight: 500;
      letter-spacing: 1px;
    }

    table.custom-table td {
      border-bottom: 1px solid #1a1a1a;
      padding: 0.6rem;
      font-size: 0.85rem;
      color: #ccc;
    }

    table.custom-table tr:hover td { background: #161616; }

    table.custom-table th.num,
    table.custom-table td.num { text-align: right; }

    table.custom-table td.bold { font-weight: 700; color: #fff; }

    .stTabs [data-baseweb="tab-list"] {
      gap: 4px;
      margin-bottom: 1rem;
      background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
      font-family: 'DM Mono', monospace;
      font-weight: 500;
      font-size: 0.8rem;
      padding: 10px 16px;
      border-radius: 2px 2px 0 0;
      background: #1a1a1a;
      color: #555;
      border: 1px solid #222;
      border-bottom: none;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .stTabs [aria-selected="true"] {
      background: #111;
      color: #CC0000;
      border-top: 2px solid #CC0000;
      border-left: 1px solid #333;
      border-right: 1px solid #333;
      border-bottom: 1px solid #111;
      margin-bottom: -1px;
    }

    .stTabs [data-baseweb="tab-border"] {
      background-color: #222 !important;
      height: 1px;
    }

    button[data-testid="stBaseButton-secondary"] {
      background: #1a1a1a !important;
      border: 1px solid #2a2a2a !important;
      color: #aaa !important;
      font-family: 'DM Mono', monospace !important;
      font-size: 0.75rem !important;
      letter-spacing: 0.5px !important;
    }

    button[data-testid="stBaseButton-secondary"]:hover {
      background: #222 !important;
      border-color: #444 !important;
      color: #e8e8e8 !important;
    }

    /* Scorecard button flush under card — override all Streamlit button defaults */
    .card-wrap { margin-bottom: 0 !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #111; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #CC0000; }
  </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def fetch_matches(query=None, channel_id=None, guild_id=None, player_id=None):
  try:
    params = {"recent": 20}
    if query: params["query"] = query
    if channel_id: params["channelId"] = channel_id
    if guild_id: params["guildId"] = guild_id
    if player_id: params["playerId"] = player_id
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

@st.cache_data(ttl=10)
def fetch_live_matches():
  try:
    r = requests.get(f"{BASE}/matches/live", timeout=5)
    return r.json().get("matches", [])
  except Exception:
    return []

@st.cache_data(ttl=10)
def fetch_live_match(match_id):
  try:
    r = requests.get(f"{BASE}/matches/{match_id}/live", timeout=8)
    return r.json()
  except Exception:
    return {}

@st.cache_data(ttl=120)
def fetch_leaderboard(category):
  try:
    r = requests.get(f"{BASE}/leaderboard", params={"category": category, "limit": 15}, timeout=8)
    return r.json()
  except Exception:
    return {}

def get_result_text(match):
  w = match.get("winner", "—")
  if w.lower() in ["drawn", "—", "tie", "tied"]: return w
  inns = match.get("innings", [])
  if not inns: return w
  maxWick = max([i['wickets'] for i in inns])
  if len(inns) > 2:
    l = match.get("teamBName") if w == match.get("teamAName") else match.get("teamAName")
    wr = sum(i.get("runs", 0) for i in inns if i.get("battingTeam") == w)
    lr = sum(i.get("runs", 0) for i in inns if i.get("battingTeam") == l)
    if len(inns) == 3 and sum(1 for i in inns if i.get("battingTeam") == w) == 1:
      return f"{w} won by an innings and {wr - lr} run(s)"
    if inns[-1].get("battingTeam") == w:
      return f"{w} won by {maxWick - inns[-1].get('wickets', 0)} wicket(s)"
    return f"{w} won by {wr - lr} runs"
  return w

def render_header():
  c1, c2 = st.columns([1, 11])
  with c1:
    st.markdown("<div style='padding-top:4px;'>", unsafe_allow_html=True)
    st.image(logo, width=44)
    st.markdown("</div>", unsafe_allow_html=True)
  with c2:
    st.markdown("""
      <div style='padding-top:2px;'>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;letter-spacing:3px;color:#CC0000;line-height:1;margin:0;">ASHES</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:2.5px;margin-top:2px;">Match Center</div>
      </div>
    """, unsafe_allow_html=True)

def render_custom_inning(inning):
  batters = inning.get("batters", [])
  bowlers = inning.get("bowlers", [])
  html = ""
  if batters:
    html += "<table class='custom-table'><thead><tr><th>Batters</th><th class='num'>R</th><th class='num'>B</th><th class='num'>4s</th><th class='num'>6s</th><th class='num'>SR</th></tr></thead><tbody>"
    for b in batters:
      name = b.get("playerName", "—")
      status = b.get('dismissedBy', '')
      html += f"<tr><td><div style='font-weight:700;color:#e8e8e8;'>{name}</div><div style='font-size:0.7rem;color:#555;text-transform:uppercase;font-family:DM Mono,monospace;'>{status}</div></td><td class='num bold'>{b.get('runs',0)}</td><td class='num'>{b.get('balls',0)}</td><td class='num'>{b.get('fours',0)}</td><td class='num'>{b.get('sixes',0)}</td><td class='num'>{b.get('strikeRate',0.0):.1f}</td></tr>"
    html += "</tbody></table>"
  if bowlers:
    html += "<table class='custom-table' style='margin-top:1.5rem;'><thead><tr><th>Bowlers</th><th class='num'>O</th><th class='num'>R</th><th class='num'>W</th><th class='num'>ECON</th></tr></thead><tbody>"
    for b in bowlers:
      html += f"<tr><td><div style='font-weight:700;color:#e8e8e8;'>{b.get('playerName','—')}</div></td><td class='num'>{b.get('overs','0.0')}</td><td class='num'>{b.get('runs',0)}</td><td class='num bold'>{b.get('wickets',0)}</td><td class='num'>{b.get('economy',0.0):.2f}</td></tr>"
    html += "</tbody></table>"
  st.markdown(html, unsafe_allow_html=True)

def page_scorecard(match_id):
  render_header()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  if st.button("← Matches"):
    st.query_params.clear()
    st.rerun()
  with st.spinner("Loading scorecard..."):
    match = fetch_match(match_id)
    scorecard = fetch_scorecard(match_id)
  if not match or "error" in match:
    st.error(f"Match data unavailable: {match_id}")
    return
  team_a = match.get("teamAName", "Team A")
  team_b = match.get("teamBName", "Team B")
  res_text = get_result_text(match)
  channel = match.get("channelName", "—")
  guild = match.get("guildName", "—")
  mvp = match.get("mvp")
  innings_summary = match.get("innings", [])
  ta_scores = []
  tb_scores = []
  for inn in innings_summary:
    w = inn.get("wickets", 0)
    score = f"{inn.get('runs', 0)}" if w == 10 else f"{inn.get('runs', 0)}/{w}"
    if inn.get("isDeclared"): score += "d"
    if inn.get("battingTeam") == team_a: ta_scores.append(score)
    elif inn.get("battingTeam") == team_b: tb_scores.append(score)
  ta_str = " & ".join(ta_scores)
  tb_str = " & ".join(tb_scores)
  st.markdown(f"""
    <div style="margin:1.5rem 0;text-align:center;border-bottom:1px solid #222;padding-bottom:1.5rem;">
      <div style="font-family:'DM Mono',monospace;font-size:0.65rem;font-weight:500;color:#444;text-transform:uppercase;letter-spacing:2px;margin-bottom:1rem;">{guild} · {channel}</div>
      <div style="display:flex;justify-content:center;align-items:center;gap:2rem;flex-wrap:wrap;">
        <div style="text-align:right;flex:1;min-width:200px;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;color:#e8e8e8;letter-spacing:2px;line-height:1;">{team_a}</div>
          <div style="font-family:'DM Mono',monospace;font-size:1.5rem;font-weight:500;color:#CC0000;margin-top:0.3rem;">{ta_str}</div>
        </div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#333;letter-spacing:3px;">VS</div>
        <div style="text-align:left;flex:1;min-width:200px;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;color:#e8e8e8;letter-spacing:2px;line-height:1;">{team_b}</div>
          <div style="font-family:'DM Mono',monospace;font-size:1.5rem;font-weight:500;color:#CC0000;margin-top:0.3rem;">{tb_str}</div>
        </div>
      </div>
    </div>
  """, unsafe_allow_html=True)
  mc1, mc2, mc3 = st.columns([2, 2, 4])
  with mc1:
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
      <div style="background:#161616;border:1px solid #222;border-top:2px solid #CC0000;padding:1rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;font-weight:500;color:#444;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:0.5rem;">Result</div>
        <div style="font-family:'DM Sans',sans-serif;font-size:0.9rem;font-weight:700;color:#e8e8e8;">🏆 {res_text}</div>
      </div>
    """, height=85)
  with mc2:
    avatar = mvp.get("avatar", "") if mvp else ""
    name = mvp.get("name", "—") if mvp else "—"
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
      <div style="background:#161616;border:1px solid #222;border-top:2px solid #555;padding:1rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;font-weight:500;color:#444;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:0.5rem;">Player of the Match</div>
        <div style="display:flex;align-items:center;gap:0.5rem;">
          <img src="{avatar}" style="width:24px;height:24px;border-radius:50%;object-fit:cover;border:1px solid #333;" onerror="this.style.display='none'">
          <span style="font-family:'DM Sans',sans-serif;font-size:1rem;font-weight:700;color:#e8e8e8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</span>
        </div>
      </div>
    """, height=85)
  with mc3:
    if innings_summary:
      pills = ""
      t_count = {}
      for inn in innings_summary:
        bt = inn.get("battingTeam", "Team")
        t_count[bt] = t_count.get(bt, 0) + 1
        ord_str = "1ST" if t_count[bt] == 1 else "2ND"
        w = inn.get("wickets", 0)
        score = f"{inn.get('runs', 0)}" if w == 10 else f"{inn.get('runs', 0)}/{w}"
        if inn.get("isDeclared"): score += "d"
        pills += (
          '<div style="flex:0 0 auto;min-width:90px;text-align:center;border-right:1px solid #1e1e1e;padding:0 0.8rem;">'
          f'<div style="font-family:\'DM Mono\',monospace;font-size:0.55rem;font-weight:500;color:#444;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.25rem;">{bt} {ord_str}</div>'
          f'<div style="font-family:\'DM Mono\',monospace;font-size:1.2rem;font-weight:500;color:#e8e8e8;">{score}</div>'
          f'<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:#444;letter-spacing:0.5px;">{inn.get("overs","0.0")} OV</div>'
          '</div>'
        )
      components.html(f"""
        <style>::-webkit-scrollbar{{display:none;}}</style>
        <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
        <div style="background:#161616;border:1px solid #222;padding:0.7rem;display:flex;align-items:center;overflow-x:auto;height:100%;box-sizing:border-box;-ms-overflow-style:none;scrollbar-width:none;">
          {pills}
        </div>
      """, height=85)
  innings_data = scorecard.get("innings", [])
  if not innings_data:
    st.markdown("<p style='color:#444;margin-top:2rem;font-size:0.9rem;text-align:center;font-weight:700;text-transform:uppercase;font-family:DM Mono,monospace;letter-spacing:2px;'>Scorecard data pending.</p>", unsafe_allow_html=True)
    return
  st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
  tab_titles = []
  t_count_sc = {}
  for inning in innings_data:
    bt = inning.get("battingTeam", "Team")
    t_count_sc[bt] = t_count_sc.get(bt, 0) + 1
    w = inning.get("wickets", 0)
    score = f"{inning.get('total', 0)}/{w}"
    if inning.get("isDeclared"): score += "d"
    tab_titles.append(f"{bt} {score}")
  if tab_titles:
    tabs = st.tabs(tab_titles)
    for tab, inning in zip(tabs, innings_data):
      with tab: render_custom_inning(inning)

def render_live_card(match):
  mid = match.get("id", "")
  team_a = match.get("teamAName", "Team A")
  team_b = match.get("teamBName", "Team B")
  state = match.get("state", "lobby")  # "lobby" or "live"
  guild = match.get("guildName", "")
  channel = match.get("channelName", "")
  innings_summary = match.get("innings", [])

  ta_scores = []
  tb_scores = []
  for inn in innings_summary:
    w = inn.get("wickets", 0)
    score = f"{inn.get('runs', 0)}" if w == 10 else f"{inn.get('runs', 0)}/{w}"
    if inn.get("isDeclared"): score += "d"
    if inn.get("battingTeam") == team_a: ta_scores.append(score)
    elif inn.get("battingTeam") == team_b: tb_scores.append(score)
  ta_score_str = ' & '.join(ta_scores)
  tb_score_str = ' & '.join(tb_scores)
  ta_score_html = f"<span class='score'>{ta_score_str}</span>" if ta_scores else ""
  tb_score_html = f"<span class='score'>{tb_score_str}</span>" if tb_scores else ""

  if state == "lobby":
    state_html = "<span class='state-pill lobby'>⏳ Lobby</span>"
    # Show team rosters if available
    players_a = match.get("teamAPlayers", [])
    players_b = match.get("teamBPlayers", [])
    roster_a = " · ".join([p.get("name", p) if isinstance(p, dict) else str(p) for p in players_a[:5]])
    roster_b = " · ".join([p.get("name", p) if isinstance(p, dict) else str(p) for p in players_b[:5]])
    extra_html = f"""
      <div class='roster-row'><span class='roster-label'>{team_a}</span> <span class='roster-names'>{roster_a or '—'}</span></div>
      <div class='roster-row'><span class='roster-label'>{team_b}</span> <span class='roster-names'>{roster_b or '—'}</span></div>
    """
  else:
    state_html = "<span class='state-pill live'><span class='live-dot'></span>Live</span>"
    extra_html = ""

  st.markdown("<div class='card-wrap'>", unsafe_allow_html=True)
  components.html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; }}
      body {{ background: transparent; }}
      .card {{
        background: #161616;
        border: 1px solid #1e1e1e;
        border-left: 3px solid {'#00cc66' if state == 'live' else '#886600'};
        padding: 0.85rem 1.1rem 0.8rem;
      }}
      .meta {{ font-family: 'DM Mono', monospace; font-size: 0.58rem; color: #3a3a3a; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.5rem; }}
      .teams {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.35rem; letter-spacing: 1.5px; color: #e8e8e8; margin-bottom: 0.45rem; }}
      .score {{ font-family: 'DM Mono', monospace; color: #CC0000; font-size: 0.88rem; margin-left: 0.3rem; }}
      .vs {{ color: #2a2a2a; font-size: 0.85rem; margin: 0 0.35rem; }}
      .state-pill {{
        display: inline-flex; align-items: center; gap: 5px;
        font-family: 'DM Mono', monospace; font-size: 0.6rem; font-weight: 500;
        padding: 0.15rem 0.55rem; border-radius: 2px; text-transform: uppercase; letter-spacing: 1px;
      }}
      .state-pill.live {{ background: rgba(0,204,102,0.12); color: #00cc66; border: 1px solid rgba(0,204,102,0.25); }}
      .state-pill.lobby {{ background: rgba(204,170,0,0.1); color: #ccaa00; border: 1px solid rgba(204,170,0,0.2); }}
      .live-dot {{
        width: 6px; height: 6px; border-radius: 50%; background: #00cc66;
        animation: pulse 1.2s ease-in-out infinite;
      }}
      @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.4; transform: scale(0.7); }} }}
      .roster-row {{ display: flex; gap: 0.4rem; align-items: baseline; margin-top: 0.3rem; }}
      .roster-label {{ font-family: 'DM Mono', monospace; font-size: 0.6rem; color: #555; text-transform: uppercase; letter-spacing: 1px; flex-shrink: 0; }}
      .roster-names {{ font-family: 'DM Mono', monospace; font-size: 0.62rem; color: #333; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    </style>
    <div class="card">
      <div class="meta">{state_html} {guild} · {channel}</div>
      <div class="teams">
        {team_a}{ta_score_html}
        <span class="vs">VS</span>
        {team_b}{tb_score_html}
      </div>
      {extra_html}
    </div>
  """, height=130 if state == "lobby" else 95)
  st.markdown("</div>", unsafe_allow_html=True)

  if state == "live":
    if st.button("Live →", key=f"live_{mid}", use_container_width=True):
      st.query_params["live"] = mid
      st.rerun()
  else:
    if st.button("Lobby →", key=f"lobby_{mid}", use_container_width=True):
      st.query_params["live"] = mid
      st.rerun()
  st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)


def page_live(match_id):
  st_autorefresh(interval=10000, key="live_autorefresh")
  render_header()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  col_back, col_ref = st.columns([2, 10])
  with col_back:
    if st.button("← Live Matches"):
      del st.query_params["live"]
      st.rerun()
  with col_ref:
    if st.button("⟳ Refresh", key="live_refresh"):
      st.cache_data.clear()
      st.rerun()

  with st.spinner("Loading live data..."):
    match = fetch_live_match(match_id)

  if not match or "error" in match:
    st.error(f"Live match unavailable: {match_id}")
    return

  team_a = match.get("teamAName", "Team A")
  team_b = match.get("teamBName", "Team B")
  guild = match.get("guildName", "—")
  channel = match.get("channelName", "—")
  innings_summary = match.get("innings", [])

  # Score header
  ta_scores, tb_scores = [], []
  for inn in innings_summary:
    w = inn.get("wickets", 0)
    score = f"{inn.get('runs', 0)}" if w == 10 else f"{inn.get('runs', 0)}/{w}"
    if inn.get("isDeclared"): score += "d"
    if inn.get("battingTeam") == team_a: ta_scores.append(score)
    elif inn.get("battingTeam") == team_b: tb_scores.append(score)
  ta_str = " & ".join(ta_scores)
  tb_str = " & ".join(tb_scores)

  st.markdown(f"""
    <div style="margin:1.2rem 0 0;padding-bottom:1.2rem;border-bottom:1px solid #1e1e1e;">
      <div style="display:flex;justify-content:center;align-items:center;gap:2rem;flex-wrap:wrap;">
        <div style="text-align:right;flex:1;min-width:160px;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#e8e8e8;letter-spacing:2px;line-height:1;">{team_a}</div>
          <div style="font-family:'DM Mono',monospace;font-size:1.3rem;font-weight:500;color:#CC0000;margin-top:0.2rem;">{ta_str or '—'}</div>
        </div>
        <div>
          <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(0,204,102,0.1);border:1px solid rgba(0,204,102,0.2);border-radius:2px;padding:0.2rem 0.7rem;">
            <span style="width:7px;height:7px;border-radius:50%;background:#00cc66;display:inline-block;animation:pulse 1.2s infinite;"></span>
            <span style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#00cc66;text-transform:uppercase;letter-spacing:1.5px;">Live</span>
          </div>
          <div style="font-family:'DM Mono',monospace;font-size:0.55rem;color:#333;text-transform:uppercase;letter-spacing:1.5px;text-align:center;margin-top:0.4rem;">{guild} · {channel}</div>
        </div>
        <div style="text-align:left;flex:1;min-width:160px;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#e8e8e8;letter-spacing:2px;line-height:1;">{team_b}</div>
          <div style="font-family:'DM Mono',monospace;font-size:1.3rem;font-weight:500;color:#CC0000;margin-top:0.2rem;">{tb_str or '—'}</div>
        </div>
      </div>
    </div>
    <style>@keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.3; }} }}</style>
  """, unsafe_allow_html=True)

  live_tab, scorecard_tab = st.tabs(["🔴 Live", "📋 Scorecard"])

  # ── LIVE TAB ─────────────────────────────────────────────────────────────
  with live_tab:
    current_inning = match.get("currentInning", {})
    batters = current_inning.get("currentBatters", match.get("currentBatters", []))
    bowlers = current_inning.get("currentBowlers", match.get("currentBowlers", []))
    commentary = match.get("commentary", [])

    # Current batters
    if batters:
      st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:0.6rem;margin-top:1rem;">
          Batting
        </div>
      """, unsafe_allow_html=True)
      batter_html = "<table class='custom-table'><thead><tr><th>Batter</th><th class='num'>R</th><th class='num'>B</th><th class='num'>SR</th></tr></thead><tbody>"
      for b in batters:
        name = b.get("playerName", b.get("name", "—"))
        runs = b.get("runs", 0)
        balls = b.get("balls", 0)
        sr = b.get("strikeRate", (runs / balls * 100) if balls else 0.0)
        on_strike = b.get("onStrike", False)
        strike_marker = " <span style='color:#CC0000;font-size:0.7rem;'>*</span>" if on_strike else ""
        batter_html += f"<tr><td><span style='font-weight:700;color:#e8e8e8;'>{name}{strike_marker}</span></td><td class='num bold'>{runs}</td><td class='num'>{balls}</td><td class='num'>{sr:.1f}</td></tr>"
      batter_html += "</tbody></table>"
      st.markdown(batter_html, unsafe_allow_html=True)

    # Current bowlers
    if bowlers:
      st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:0.6rem;margin-top:1.2rem;">
          Bowling
        </div>
      """, unsafe_allow_html=True)
      bowler_html = "<table class='custom-table'><thead><tr><th>Bowler</th><th class='num'>O</th><th class='num'>R</th><th class='num'>W</th></tr></thead><tbody>"
      for b in bowlers:
        name = b.get("playerName", b.get("name", "—"))
        overs = b.get("overs", "0.0")
        runs = b.get("runs", 0)
        wkts = b.get("wickets", 0)
        bowling = b.get("isBowling", False)
        bowling_marker = " <span style='color:#00cc66;font-size:0.7rem;'>↗</span>" if bowling else ""
        bowler_html += f"<tr><td><span style='font-weight:700;color:#e8e8e8;'>{name}{bowling_marker}</span></td><td class='num'>{overs}</td><td class='num'>{runs}</td><td class='num bold'>{wkts}</td></tr>"
      bowler_html += "</tbody></table>"
      st.markdown(bowler_html, unsafe_allow_html=True)

    if not batters and not bowlers:
      st.markdown("<p style='color:#333;font-size:0.85rem;margin-top:2rem;text-align:center;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;'>Awaiting play</p>", unsafe_allow_html=True)

    # Commentary
    if commentary:
      st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:0.6rem;margin-top:1.8rem;padding-top:1.2rem;border-top:1px solid #1a1a1a;">
          Recent Commentary
        </div>
      """, unsafe_allow_html=True)
      for i, entry in enumerate(commentary[:10]):
        ball = entry.get("ball", entry.get("over", ""))
        text = entry.get("text", entry.get("commentary", str(entry)))
        is_wicket = "wicket" in text.lower() or "out" in text.lower() or "wkt" in text.lower()
        is_boundary = any(x in text.lower() for x in ["four", "six", "boundary", "4!", "6!"])
        accent = "#CC0000" if is_wicket else ("#f5a623" if is_boundary else "#1e1e1e")
        ball_label = f"<span style='font-family:DM Mono,monospace;font-size:0.62rem;color:#444;flex-shrink:0;min-width:3rem;'>{ball}</span>" if ball else ""
        st.markdown(f"""
          <div style="display:flex;gap:0.8rem;align-items:flex-start;padding:0.55rem 0.8rem;border-left:2px solid {accent};background:#141414;margin-bottom:3px;border-radius:0 2px 2px 0;">
            {ball_label}
            <span style="font-size:0.83rem;color:{'#ff4444' if is_wicket else ('#f5a623' if is_boundary else '#888')};line-height:1.4;">{text}</span>
          </div>
        """, unsafe_allow_html=True)

  # ── SCORECARD TAB ─────────────────────────────────────────────────────────
  with scorecard_tab:
    innings_data = match.get("innings", [])
    if not innings_data:
      st.markdown("<p style='color:#444;margin-top:2rem;font-size:0.9rem;text-align:center;font-weight:700;text-transform:uppercase;font-family:DM Mono,monospace;letter-spacing:2px;'>Innings not yet started.</p>", unsafe_allow_html=True)
    else:
      tab_titles = []
      t_count_sc = {}
      for inning in innings_data:
        bt = inning.get("battingTeam", "Team")
        t_count_sc[bt] = t_count_sc.get(bt, 0) + 1
        w = inning.get("wickets", 0)
        score = f"{inning.get('total', inning.get('runs', 0))}/{w}"
        if inning.get("isDeclared"): score += "d"
        ord_str = "1st" if t_count_sc[bt] == 1 else "2nd"
        tab_titles.append(f"{bt} {ord_str} — {score}")
      if tab_titles:
        tabs = st.tabs(tab_titles)
        for tab, inning in zip(tabs, innings_data):
          with tab: render_custom_inning(inning)


def page_leaderboard():
  render_header()
  st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
  if st.button("← Matches"):
    st.query_params.clear()
    st.rerun()

  CATEGORIES = {
    "Most Runs":               "most_runs",
    "Most Wickets":            "most_wickets",
    "Most Matches":            "most_matches",
    "Most MVPs":               "most_mvps",
    "Highest Batting AVG":     "highest_bat_avg",
    "Highest Batting SR":      "highest_bat_sr",
    "Best Bowling AVG":        "best_bowl_avg",
    "Best Bowling ECO":        "best_bowl_eco",
    "Best Bowling SR":         "best_bowl_sr",
    "Most 30s":                "most_30s",
    "Most 50s":                "most_50s",
    "Most 4s":                 "most_4s",
    "Most 6s":                 "most_6s",
    "Most 3-fers":             "most_3fers",
    "Most 5-fers":             "most_5fers",
    "Most Hattricks":          "most_hattricks",
    "Fastest 50s":             "fastest_50s",
    "Fastest 30s":             "fastest_30s",
    "Best Batting Inning":     "best_bat_inning",
    "Best Bowling Inning":     "best_bowl_inning",
    "Highest SR in an Inning": "highest_sr_inning",
    "Best Partnerships (Inning)":  "best_partnerships_inning",
    "Best Partnerships (Overall)": "best_partnerships_overall",
    "Highest Match Aggregates":    "highest_match_aggregate",
  }

  selected_label = st.selectbox(
    "Category",
    list(CATEGORIES.keys()),
    label_visibility="collapsed",
    key="lb_category"
  )
  category_key = CATEGORIES[selected_label]

  with st.spinner("Loading..."):
    result = fetch_leaderboard(category_key)

  if not result or "error" in result:
    st.markdown("<p style='color:#444;font-size:0.9rem;text-align:center;margin-top:2rem;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;'>No data available.</p>", unsafe_allow_html=True)
    return

  title = result.get("title", selected_label)
  note = result.get("note")
  cols = result.get("cols", [])
  data = result.get("data", [])

  st.markdown(f"""
    <div style="margin:1rem 0 0.5rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#e8e8e8;letter-spacing:2px;line-height:1;">{title}</div>
      {f'<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">{note}</div>' if note else ''}
    </div>
  """, unsafe_allow_html=True)

  if not data:
    st.markdown("<p style='color:#333;font-size:0.85rem;text-align:center;margin-top:2rem;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;'>No entries yet.</p>", unsafe_allow_html=True)
    return

  # Build table HTML
  # Determine display columns dynamically from first row
  sample = data[0]
  is_partnership = 'player2' in sample
  is_match = 'matchId' in sample

  th_cells = "<th>#</th>"
  if is_partnership:
    th_cells += "<th>Batters</th>"
  elif is_match:
    th_cells += "<th>Match</th>"
  else:
    th_cells += "<th>Player</th>"

  # remaining numeric/string cols (skip player keys, rank, matchId)
  skip = {'rank', 'player', 'player2', 'playerAvatar', 'player2Avatar', 'matchId'}
  extra_cols = [k for k in sample.keys() if k not in skip]
  for col in extra_cols:
    th_cells += f"<th class='num'>{col.upper()}</th>"

  rows_html = ""
  for entry in data:
    rank = entry.get("rank", "")
    if is_partnership:
      name = f"{entry.get('player','—')} &amp; {entry.get('player2','—')}"
    elif is_match:
      mid = entry.get('matchId','—')
      name = f"<span style='font-family:DM Mono,monospace;font-size:0.7rem;color:#555;'>{mid[:12]}…</span>"
    else:
      name = entry.get("player", "—")

    td_rank = f"<td style='color:#444;font-family:DM Mono,monospace;font-size:0.75rem;'>{rank}</td>"
    td_name = f"<td class='bold'>{name}</td>"
    td_extras = ""
    for col in extra_cols:
      val = entry.get(col, "—")
      td_extras += f"<td class='num'>{val}</td>"

    rows_html += f"<tr>{td_rank}{td_name}{td_extras}</tr>"

  table_html = f"""
    <table class='custom-table'>
      <thead><tr>{th_cells}</tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  """
  st.markdown(table_html, unsafe_allow_html=True)


def page_list():
  render_header()
  st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

  main_tab, live_tab, lb_tab = st.tabs(["📁 Matches", "🔴 Live", "🏆 Leaderboard"])

  with live_tab:
    st_autorefresh(interval=15000, key="live_list_autorefresh")
    col_ref, _ = st.columns([2, 10])
    with col_ref:
      if st.button("⟳ Refresh", key="live_list_refresh"):
        st.cache_data.clear()
        st.rerun()
    live_matches = fetch_live_matches()
    if not live_matches:
      st.markdown("""
        <div style='text-align:center;margin-top:3rem;'>
          <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#333;text-transform:uppercase;letter-spacing:3px;'>No Live Matches</div>
          <div style='font-family:DM Mono,monospace;font-size:0.55rem;color:#222;text-transform:uppercase;letter-spacing:2px;margin-top:0.5rem;'>Check back soon</div>
        </div>
      """, unsafe_allow_html=True)
    else:
      st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
      for m in live_matches:
        render_live_card(m)

  with lb_tab:
    if st.button("Open Full Leaderboard →", key="lb_goto", use_container_width=False):
      st.query_params["page"] = "leaderboard"
      st.rerun()

  with main_tab:
    query = st.text_input("Query", placeholder="Search matches...", label_visibility="collapsed", key="query_input")

    show_filters = st.session_state.get("show_filters", False)

    st.markdown(f"<div id='filter-anchor' data-open='{'1' if show_filters else '0'}'></div>", unsafe_allow_html=True)

    col_btn, col_rest = st.columns([2, 8])
    with col_btn:
      label = "✕ Hide Filters" if show_filters else "⚙ Filters"
      if st.button(label, key="filter_toggle", type="secondary"):
        st.session_state["show_filters"] = not show_filters
        st.rerun()

    st.markdown("""
      <style>
        .filter-drawer {
          overflow: hidden;
          transition: max-height 0.38s cubic-bezier(0.4,0,0.2,1),
                      opacity 0.28s ease,
                      margin-top 0.3s ease;
        }
        .filter-drawer.closed {
          max-height: 0 !important;
          opacity: 0;
          margin-top: 0 !important;
          pointer-events: none;
        }
        .filter-drawer.open {
          max-height: 120px;
          opacity: 1;
          margin-top: 0.5rem;
        }
        #filter-anchor[data-open='1'] ~ div button[kind="secondary"],
        #filter-anchor[data-open='1'] ~ div button[data-testid="stBaseButton-secondary"] {
          border-color: #CC0000 !important;
          color: #CC0000 !important;
        }
        .card-wrap { margin-bottom: 0 !important; }
        .card-wrap + div [data-testid="stButton"] > button {
          margin-top: 0 !important;
          border-top: none !important;
          border-radius: 0 0 2px 2px !important;
          background: #1a1a1a !important;
          border-color: #1e1e1e !important;
          color: #555 !important;
          font-size: 0.72rem !important;
          letter-spacing: 1.5px !important;
          width: 100% !important;
          padding: 0.5rem !important;
        }
        .card-wrap + div [data-testid="stButton"] > button:hover {
          background: #CC0000 !important;
          color: #fff !important;
          border-color: #CC0000 !important;
        }
      </style>
    """, unsafe_allow_html=True)

    drawer_class = "open" if show_filters else "closed"
    st.markdown(f"<div class='filter-drawer {drawer_class}'>", unsafe_allow_html=True)
    if show_filters:
      f1, f2, f3 = st.columns(3)
      with f1: guild_id = st.text_input("Server", placeholder="Server ID", label_visibility="collapsed", key="fi_guild")
      with f2: channel_id = st.text_input("Channel", placeholder="Channel ID", label_visibility="collapsed", key="fi_channel")
      with f3: player_id = st.text_input("Player", placeholder="Player ID", label_visibility="collapsed", key="fi_player")
    else:
      guild_id = ""
      channel_id = ""
      player_id = ""
    st.markdown("</div>", unsafe_allow_html=True)

    matches = fetch_matches(query, channel_id, guild_id, player_id)
    if not matches:
      st.markdown("<p style='color:#333;font-size:1rem;font-weight:700;text-align:center;margin-top:4rem;text-transform:uppercase;font-family:DM Mono,monospace;letter-spacing:3px;'>No Results Found</p>", unsafe_allow_html=True)
      return

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    for match in matches:
      mid = match["id"]
      team_a = match.get("teamAName", "Team A")
      team_b = match.get("teamBName", "Team B")
      ts = match.get("timestamp", 0)
      ta_scores = []
      tb_scores = []
      for inn in match.get("innings", []):
        w = inn.get("wickets", 0)
        score = f"{inn.get('runs', 0)}" if w == 10 else f"{inn.get('runs', 0)}/{w}"
        if inn.get("isDeclared"): score += "d"
        if inn.get("battingTeam") == team_a: ta_scores.append(score)
        elif inn.get("battingTeam") == team_b: tb_scores.append(score)
      res_text = get_result_text(match)
      guild = match.get("guildName", "")
      channel = match.get("channelName", "")
      time_span = f'<span class="ts" data-ts="{ts}"></span>' if ts else ""
      ta_score_str = ' & '.join(ta_scores)
      tb_score_str = ' & '.join(tb_scores)
      ta_score_html = f"<span class='score'>{ta_score_str}</span>" if ta_scores else ""
      tb_score_html = f"<span class='score'>{tb_score_str}</span>" if tb_scores else ""

      st.markdown(f"<div class='card-wrap'>", unsafe_allow_html=True)
      components.html(f"""
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
          * {{ box-sizing: border-box; margin: 0; padding: 0; }}
          body {{ background: transparent; }}
          .card {{
            background: #161616;
            border: 1px solid #1e1e1e;
            border-left: 3px solid #CC0000;
            padding: 0.85rem 1.1rem 0.8rem;
          }}
          .meta {{ font-family: 'DM Mono', monospace; font-size: 0.58rem; color: #3a3a3a; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.35rem; }}
          .teams {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.35rem; letter-spacing: 1.5px; color: #e8e8e8; margin-bottom: 0.45rem; }}
          .score {{ font-family: 'DM Mono', monospace; color: #CC0000; font-size: 0.88rem; margin-left: 0.3rem; }}
          .vs {{ color: #2a2a2a; font-size: 0.85rem; margin: 0 0.35rem; }}
          .result-pill {{
            display: inline-flex; align-items: center;
            background: #111; border: 1px solid #1e1e1e;
            color: #777; font-family: 'DM Mono', monospace;
            font-size: 0.63rem; padding: 0.2rem 0.65rem;
            border-radius: 2px; text-transform: uppercase; letter-spacing: 0.5px;
          }}
          .res-label {{ color: #CC0000; margin-right: 5px; }}
        </style>
        <div class="card">
          <div class="meta">{time_span} {guild} · {channel}</div>
          <div class="teams">
            {team_a}{ta_score_html}
            <span class="vs">VS</span>
            {team_b}{tb_score_html}
          </div>
          <div class="result-pill"><span class="res-label">RES</span>{res_text}</div>
        </div>
        <script>
          document.querySelectorAll('.ts').forEach(function(el) {{
            var d = new Date(parseInt(el.getAttribute('data-ts')) * 1000);
            el.textContent = d.toLocaleString([], {{dateStyle:'medium', timeStyle:'short'}}) + ' ·';
          }});
        </script>
      """, height=112)
      st.markdown("</div>", unsafe_allow_html=True)

      if st.button("Scorecard →", key=f"sc_{mid}", use_container_width=True):
        st.query_params["id"] = mid
        st.rerun()

      st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)


params = st.query_params
match_id = params.get("id", None)
live_id = params.get("live", None)
page = params.get("page", None)
if match_id:
  page_scorecard(match_id)
elif live_id:
  page_live(live_id)
elif page == "leaderboard":
  page_leaderboard()
else:
  page_list()
