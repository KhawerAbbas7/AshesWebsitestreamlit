import streamlit as st
import requests
import streamlit.components.v1 as components

logo = "40ef4cf2ee6a72db2a5af55c231192bd.png"
BASE = "http://51.75.118.79:20375"
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
      padding: 2rem 3rem 4rem;
      max-width: 1080px;
      background: #111111;
      box-shadow: 0 0 0 1px #222, 0 8px 32px rgba(0,0,0,0.6);
      margin-top: 2rem;
      border-top: 3px solid #CC0000;
    }

    h1 {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 2.8rem;
      letter-spacing: 2px;
      margin: 0;
      color: #CC0000;
      line-height: 1;
    }

    h2, h3 {
      font-weight: 700;
      color: #e8e8e8;
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

    .stTextInput > div > input::placeholder {
      color: #555;
    }

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

    table.custom-table tr:hover td {
      background: #161616;
    }

    table.custom-table th.num,
    table.custom-table td.num {
      text-align: right;
    }

    table.custom-table td.bold {
      font-weight: 700;
      color: #fff;
    }

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

    .match-scorecard-btn > div > button {
      margin-top: -0.6rem !important;
      border-radius: 0 0 2px 2px !important;
      width: 100% !important;
    }

    /* Scrollbar */
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
  with c1: st.image(logo, width=48)
  with c2:
    st.title("Ashes")
    st.caption("Match Center")

def render_custom_inning(inning):
  batters = inning.get("batters", [])
  bowlers = inning.get("bowlers", [])
  html = ""
  if batters:
    html += """
      <table class='custom-table'>
        <thead>
          <tr>
            <th>Batters</th>
            <th class='num'>R</th>
            <th class='num'>B</th>
            <th class='num'>4s</th>
            <th class='num'>6s</th>
            <th class='num'>SR</th>
          </tr>
        </thead>
        <tbody>
    """
    for b in batters:
      name = b.get("playerName", "—")
      status = b.get('dismissedBy', '')
      html += f"""
        <tr>
          <td>
            <div style='font-weight:700;color:#e8e8e8;'>{name}</div>
            <div style='font-size:0.7rem;color:#555;text-transform:uppercase;font-family:DM Mono,monospace;'>{status}</div>
          </td>
          <td class='num bold'>{b.get('runs', 0)}</td>
          <td class='num'>{b.get('balls', 0)}</td>
          <td class='num'>{b.get('fours', 0)}</td>
          <td class='num'>{b.get('sixes', 0)}</td>
          <td class='num'>{b.get('strikeRate', 0.0):.1f}</td>
        </tr>
      """
    html += "</tbody></table>"
  if bowlers:
    html += """
      <table class='custom-table' style='margin-top:1.5rem;'>
        <thead>
          <tr>
            <th>Bowlers</th>
            <th class='num'>O</th>
            <th class='num'>R</th>
            <th class='num'>W</th>
            <th class='num'>ECON</th>
          </tr>
        </thead>
        <tbody>
    """
    for b in bowlers:
      html += f"""
        <tr>
          <td><div style='font-weight:700;color:#e8e8e8;'>{b.get('playerName', '—')}</div></td>
          <td class='num'>{b.get('overs', '0.0')}</td>
          <td class='num'>{b.get('runs', 0)}</td>
          <td class='num bold'>{b.get('wickets', 0)}</td>
          <td class='num'>{b.get('economy', 0.0):.2f}</td>
        </tr>
      """
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
          f'<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:#444;letter-spacing:0.5px;">{inn.get("overs", "0.0")} OV</div>'
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

def page_list():
  render_header()
  st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
  query = st.text_input("Query", placeholder="Search matches...", label_visibility="collapsed", key="query_input")
  show_filters = st.session_state.get("show_filters", False)
  if st.button("⚙ Filters" if not show_filters else "✕ Hide Filters", key="filter_toggle", type="secondary"):
    st.session_state["show_filters"] = not show_filters
    st.rerun()
  guild_id = ""
  channel_id = ""
  player_id = ""
  if st.session_state.get("show_filters", False):
    f1, f2, f3 = st.columns(3)
    with f1: guild_id = st.text_input("Server", placeholder="Server ID", label_visibility="collapsed")
    with f2: channel_id = st.text_input("Channel", placeholder="Channel ID", label_visibility="collapsed")
    with f3: player_id = st.text_input("Player", placeholder="Player ID", label_visibility="collapsed")
  matches = fetch_matches(query, channel_id, guild_id, player_id)
  if not matches:
    st.markdown("<p style='color:#333;font-size:1rem;font-weight:700;text-align:center;margin-top:4rem;text-transform:uppercase;font-family:DM Mono,monospace;letter-spacing:3px;'>No Results Found</p>", unsafe_allow_html=True)
    return
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
    ta_str = f"<span style='font-family:DM Mono,monospace;color:#CC0000;font-size:0.95rem;margin-left:0.4rem;font-weight:500;'>{' & '.join(ta_scores)}</span>" if ta_scores else ""
    tb_str = f"<span style='font-family:DM Mono,monospace;color:#CC0000;font-size:0.95rem;margin-left:0.4rem;font-weight:500;'>{' & '.join(tb_scores)}</span>" if tb_scores else ""
    res_text = get_result_text(match)
    guild = match.get("guildName", "")
    channel = match.get("channelName", "")
    time_span = f'<span class="ts" data-ts="{ts}"></span>' if ts else ""
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
      <div style="background:#161616;border:1px solid #1e1e1e;border-left:3px solid #CC0000;padding:1rem 1.2rem;font-family:'DM Sans',sans-serif;">
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;font-weight:500;color:#444;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:0.4rem;">{time_span} {guild} · {channel}</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:1.5px;color:#e8e8e8;margin-bottom:0.5rem;">
          {team_a} {ta_str} <span style="color:#2a2a2a;font-size:0.9rem;margin:0 0.4rem;">VS</span> {team_b} {tb_str}
        </div>
        <div style="display:inline-flex;align-items:center;background:#111;border:1px solid #1e1e1e;color:#aaa;font-family:'DM Mono',monospace;font-size:0.68rem;font-weight:500;padding:0.25rem 0.7rem;border-radius:2px;text-transform:uppercase;letter-spacing:0.5px;">
          <span style="color:#CC0000;margin-right:6px;font-weight:500;">RES</span>{res_text}
        </div>
      </div>
      <script>
        document.querySelectorAll('.ts').forEach(function(el) {{
          el.textContent = new Date(parseInt(el.getAttribute('data-ts')) * 1000).toLocaleString([], {{dateStyle:'medium', timeStyle:'short'}}) + ' ·';
        }});
      </script>
    """, height=105)
    st.markdown("<div class='match-scorecard-btn'>", unsafe_allow_html=True)
    if st.button("Scorecard →", key=f"sc_{mid}", use_container_width=True):
      st.query_params["id"] = mid
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

params = st.query_params
match_id = params.get("id", None)
if match_id:
  page_scorecard(match_id)
else:
  page_list()
