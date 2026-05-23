import streamlit as st
import requests
import streamlit.components.v1 as components
import uuid
logo = "40ef4cf2ee6a72db2a5af55c231192bd.png"
BASE = "http://51.75.118.79:20375"
st.set_page_config(page_title="Ashes", page_icon=logo, layout="wide")
st.markdown("""
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background: #f4f4f4; color: #000; }
    .block-container { padding: 2rem 3rem 4rem; max-width: 1080px; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 2rem; border-top: 4px solid #CC0000; }
    h1 { font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; margin: 0; color: #CC0000; text-transform: uppercase; }
    h2, h3 { font-weight: 700; color: #000; }
    .stButton > button { background: #CC0000; border: none; color: #fff; font-family: 'Roboto', sans-serif; font-size: 0.8rem; font-weight: 700; padding: 0.4rem 1rem; border-radius: 2px; text-transform: uppercase; transition: background 0.2s; }
    .stButton > button:hover { background: #990000; color: #fff; }
    .stTextInput > div > input { background: #fff; border: 1px solid #ccc; color: #000; font-family: 'Roboto', sans-serif; font-size: 0.9rem; border-radius: 2px; padding: 0.5rem 0.8rem; }
    .stTextInput > div > input:focus { border-color: #CC0000; box-shadow: 0 0 0 1px #CC0000; }
    table.custom-table { width: 100%; border-collapse: collapse; background: #fff; margin-bottom: 1rem; }
    table.custom-table th { border-bottom: 2px solid #e0e0e0; padding: 0.6rem; color: #666; font-size: 0.75rem; text-transform: uppercase; text-align: left; font-weight: 700; }
    table.custom-table td { border-bottom: 1px solid #eee; padding: 0.6rem; font-size: 0.85rem; color: #000; }
    table.custom-table th.num, table.custom-table td.num { text-align: right; }
    table.custom-table td.bold { font-weight: 900; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; margin-bottom: 1rem; }
    .stTabs [data-baseweb="tab"] { font-family: 'Roboto', sans-serif; font-weight: 700; font-size: 0.9rem; padding: 10px 16px; border-radius: 4px 4px 0 0; background: #f4f4f4; color: #666; border: 1px solid #ddd; border-bottom: none; }
    .stTabs [aria-selected="true"] { background: #fff; color: #CC0000; border-top: 3px solid #CC0000; border-left: 1px solid #ddd; border-right: 1px solid #ddd; border-bottom: 1px solid #fff; margin-bottom: -1px; }
    .stTabs [data-baseweb="tab-border"] { background-color: #ddd !important; height: 1px; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) > div > div > button[kind="secondary"],
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) > div > div > button {
      background: #fff !important; border: 1px solid #ccc !important; color: #000 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) > div > div > button:hover {
      background: #f4f4f4 !important; border-color: #999 !important; color: #000 !important;
    }
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
    html += "<table class='custom-table'><thead><tr><th>Batters</th><th class='num'>R</th><th class='num'>B</th><th class='num'>4s</th><th class='num'>6s</th><th class='num'>SR</th></tr></thead><tbody>"
    for b in batters:
      name = b.get("playerName", "—")
      status = b.get('dismissedBy')
      html += f"<tr><td><div style='font-weight:700;color:#000;'>{name}</div><div style='font-size:0.7rem;color:#666;text-transform:uppercase;'>{status}</div></td><td class='num bold'>{b.get('runs',0)}</td><td class='num'>{b.get('balls',0)}</td><td class='num'>{b.get('fours',0)}</td><td class='num'>{b.get('sixes',0)}</td><td class='num'>{b.get('strikeRate',0.0):.1f}</td></tr>"
    html += "</tbody></table>"
  if bowlers:
    html += "<table class='custom-table' style='margin-top:1.5rem;'><thead><tr><th>Bowlers</th><th class='num'>O</th><th class='num'>R</th><th class='num'>W</th><th class='num'>ECON</th></tr></thead><tbody>"
    for b in bowlers:
      html += f"<tr><td><div style='font-weight:700;color:#000;'>{b.get('playerName','—')}</div></td><td class='num'>{b.get('overs','0.0')}</td><td class='num'>{b.get('runs',0)}</td><td class='num bold'>{b.get('wickets',0)}</td><td class='num'>{b.get('economy',0.0):.2f}</td></tr>"
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
    <div style="margin: 1.5rem 0; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 1.5rem;">
      <div style="font-size:0.75rem;font-weight:700;color:#666;text-transform:uppercase;margin-bottom:1rem;">{guild} | {channel}</div>
      <div style="display:flex;justify-content:center;align-items:center;gap:2rem;flex-wrap:wrap;">
        <div style="text-align:right;flex:1;min-width:200px;">
          <div style="font-size:2.4rem;font-weight:900;color:#000;text-transform:uppercase;line-height:1;">{team_a}</div>
          <div style="font-size:1.6rem;font-weight:900;color:#CC0000;margin-top:0.3rem;">{ta_str}</div>
        </div>
        <div style="font-size:1.8rem;font-weight:900;color:#ccc;">VS</div>
        <div style="text-align:left;flex:1;min-width:200px;">
          <div style="font-size:2.4rem;font-weight:900;color:#000;text-transform:uppercase;line-height:1;">{team_b}</div>
          <div style="font-size:1.6rem;font-weight:900;color:#CC0000;margin-top:0.3rem;">{tb_str}</div>
        </div>
      </div>
    </div>
  """, unsafe_allow_html=True)
  mc1, mc2, mc3 = st.columns([2, 2, 4])
  with mc1:
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap" rel="stylesheet">
      <div style="background:#fff;border:1px solid #ddd;border-top:3px solid #CC0000;padding:1rem;">
        <div style="font-size:0.65rem;font-weight:700;color:#666;text-transform:uppercase;margin-bottom:0.4rem;font-family:'Roboto',sans-serif;">Result</div>
        <div style="font-family:'Roboto',sans-serif;font-size:0.95rem;font-weight:900;color:#000;text-transform:uppercase;">🏆 {res_text}</div>
      </div>
    """, height=85)
  with mc2:
    avatar = mvp.get("avatar", "") if mvp else ""
    name = mvp.get("name", "—") if mvp else "—"
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap" rel="stylesheet">
      <div style="background:#fff;border:1px solid #ddd;border-top:3px solid #000;padding:1rem;">
        <div style="font-size:0.65rem;font-weight:700;color:#666;text-transform:uppercase;margin-bottom:0.4rem;font-family:'Roboto',sans-serif;">Player of the Match</div>
        <div style="display:flex;align-items:center;gap:0.5rem;">
          <img src="{avatar}" style="width:24px;height:24px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
          <span style="font-family:'Roboto',sans-serif;font-size:1.1rem;font-weight:900;color:#000;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</span>
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
          '<div style="flex:0 0 auto;min-width:90px;text-align:center;border-right:1px solid #eee;padding:0 0.8rem;">'
          f'<div style="font-size:0.6rem;font-weight:700;color:#666;text-transform:uppercase;margin-bottom:0.2rem;font-family:\'Roboto\',sans-serif;">{bt} {ord_str}</div>'
          f'<div style="font-family:\'Roboto\',sans-serif;font-size:1.2rem;font-weight:900;color:#000;">{score}</div>'
          f'<div style="font-size:0.7rem;color:#666;font-weight:700;">{inn.get("overs", "0.0")} OV</div>'
          '</div>'
        )
      components.html(f"""
        <style>::-webkit-scrollbar{{display:none;}}</style>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap" rel="stylesheet">
        <div style="background:#fff;border:1px solid #ddd;padding:0.7rem;display:flex;align-items:center;overflow-x:auto;height:100%;box-sizing:border-box;-ms-overflow-style:none;scrollbar-width:none;">
          {pills}
        </div>
      """, height=85)
  innings_data = scorecard.get("innings", [])
  if not innings_data:
    st.markdown("<p style='color:#666;margin-top:2rem;font-size:1rem;text-align:center;font-weight:700;text-transform:uppercase;'>Scorecard data pending.</p>", unsafe_allow_html=True)
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
  st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
  s1, s2 = st.columns([10, 2])
  with s1:
    query = st.text_input("Query", placeholder="Search matches...", label_visibility="collapsed")
  with s2:
    if st.button("⚙ Filters", use_container_width=True):
      st.session_state["show_filters"] = not st.session_state.get("show_filters", False)
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
    st.markdown("<p style='color:#000;font-size:1.2rem;font-weight:900;text-align:center;margin-top:4rem;text-transform:uppercase;'>No Results Found</p>", unsafe_allow_html=True)
    return
  st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
  for match in matches:
    mid = match["id"]
    team_a = match.get("teamAName", "Team A")
    team_b = match.get("teamBName", "Team B")
    ts = match.get("timestamp", 0)
    tid = f"ts_{mid}"
    time_html = f"""<span id="{tid}" style="color:#CC0000;font-weight:900;margin-right:8px;"></span><script>document.getElementById("{tid}").textContent=new Date({ts}*1000).toLocaleString([],{{dateStyle:"medium",timeStyle:"short"}});</script>""" if ts else ""
    ta_scores = []
    tb_scores = []
    for inn in match.get("innings", []):
      w = inn.get("wickets", 0)
      score = f"{inn.get('runs', 0)}" if w == 10 else f"{inn.get('runs', 0)}/{w}"
      if inn.get("isDeclared"): score += "d"
      if inn.get("battingTeam") == team_a: ta_scores.append(score)
      elif inn.get("battingTeam") == team_b: tb_scores.append(score)
    ta_str = f" <span style='color:#CC0000;font-size:1.1rem;margin-left:0.4rem;'>{' & '.join(ta_scores)}</span>" if ta_scores else ""
    tb_str = f" <span style='color:#CC0000;font-size:1.1rem;margin-left:0.4rem;'>{' & '.join(tb_scores)}</span>" if tb_scores else ""
    res_text = get_result_text(match)
    c1, c2 = st.columns([10, 2])
    with c1:
      st.markdown(f"""
        <div style="background:#fff;border:1px solid #e0e0e0;border-left:4px solid #CC0000;padding:1.2rem;margin-bottom:0.3rem;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
            <div>
              <div style="font-size:0.7rem;font-weight:700;color:#666;text-transform:uppercase;margin-bottom:0.3rem;">{time_html}{match.get('guildName', '')} | {match.get('channelName', '')}</div>
              <div style="font-family:'Roboto',sans-serif;font-size:1.2rem;font-weight:900;color:#000;text-transform:uppercase;">
                {team_a}{ta_str} <span style="color:#ccc;font-weight:900;font-size:1rem;margin:0 0.4rem;">VS</span> {team_b}{tb_str}
              </div>
            </div>
            <div style="display:inline-flex;align-items:center;background:#f4f4f4;border:1px solid #ddd;color:#000;font-size:0.75rem;font-family:'Roboto',sans-serif;font-weight:700;padding:0.3rem 0.8rem;border-radius:2px;text-transform:uppercase;">
              <span style="color:#CC0000;margin-right:6px;font-weight:900;">RESULT:</span> {res_text}
            </div>
          </div>
        </div>
      """, unsafe_allow_html=True)
    with c2:
      st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
      if st.button("Scorecard", key=mid, use_container_width=True):
        st.query_params["id"] = mid
        st.rerun()
params = st.query_params
match_id = params.get("id", None)
if match_id:
  page_scorecard(match_id)
else:
  page_list()
