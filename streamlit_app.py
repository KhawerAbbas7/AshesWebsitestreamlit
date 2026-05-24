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

    /* Scorecard button: flush against card, no gap */
    .sc-btn-wrap { margin-top: 0 !important; }
    .sc-btn-wrap > div > button {
      border-radius: 0 0 2px 2px !important;
      width: 100% !important;
      margin-top: 0 !important;
      border-top: 1px solid #1e1e1e !important;
    }

    /* Collapse spacing around the button element */
    .sc-btn-wrap [data-testid="stButton"] { margin: 0 !important; padding: 0 !important; }

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

def page_list():
  render_header()
  st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
  query = st.text_input("Query", placeholder="Search matches...", label_visibility="collapsed", key="query_input")

  # Animated filter panel — entirely inside components.html so CSS transition works
  # We post a message to Streamlit to toggle session state when the button inside is clicked
  show_filters = st.session_state.get("show_filters", False)

  # Render the animated filter panel + toggle button as one HTML block
  filter_html_open = "open" if show_filters else ""
  components.html(f"""
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; }}
      #filter-toggle {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #aaa;
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.45rem 1rem;
        border-radius: 2px;
        cursor: pointer;
        transition: background 0.15s, border-color 0.15s, color 0.15s;
        margin-bottom: 0;
      }}
      #filter-toggle:hover {{ background: #222; border-color: #444; color: #e8e8e8; }}
      #filter-toggle.active {{ border-color: #CC0000; color: #CC0000; }}
      .chevron {{
        display: inline-block;
        transition: transform 0.3s ease;
        font-style: normal;
      }}
      #filter-toggle.active .chevron {{ transform: rotate(180deg); }}

      #filter-panel {{
        overflow: hidden;
        max-height: 0;
        opacity: 0;
        transition: max-height 0.35s cubic-bezier(0.4,0,0.2,1), opacity 0.25s ease;
        margin-top: 0;
      }}
      #filter-panel.open {{
        max-height: 120px;
        opacity: 1;
        margin-top: 10px;
      }}
      .filter-row {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        padding-top: 2px;
      }}
      .filter-row input {{
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #e8e8e8;
        font-family: 'DM Mono', monospace;
        font-size: 0.8rem;
        border-radius: 2px;
        padding: 0.45rem 0.7rem;
        width: 100%;
        outline: none;
        transition: border-color 0.15s;
      }}
      .filter-row input::placeholder {{ color: #444; }}
      .filter-row input:focus {{ border-color: #CC0000; }}
    </style>

    <button id="filter-toggle" class="{'active' if show_filters else ''}" onclick="toggleFilters()">
      <span>⚙</span>
      <span id="btn-label">{'Hide Filters' if show_filters else 'Filters'}</span>
      <i class="chevron">▾</i>
    </button>

    <div id="filter-panel" class="{filter_html_open}">
      <div class="filter-row">
        <input id="f-guild" type="text" placeholder="Server ID" value="">
        <input id="f-channel" type="text" placeholder="Channel ID" value="">
        <input id="f-player" type="text" placeholder="Player ID" value="">
      </div>
    </div>

    <script>
      var isOpen = {'true' if show_filters else 'false'};

      function toggleFilters() {{
        isOpen = !isOpen;
        var panel = document.getElementById('filter-panel');
        var btn = document.getElementById('filter-toggle');
        var label = document.getElementById('btn-label');
        if (isOpen) {{
          panel.classList.add('open');
          btn.classList.add('active');
          label.textContent = 'Hide Filters';
        }} else {{
          panel.classList.remove('open');
          btn.classList.remove('active');
          label.textContent = 'Filters';
        }}
        // Notify Streamlit after transition settles
        setTimeout(function() {{
          window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{
              action: 'toggle_filters',
              open: isOpen,
              guild: document.getElementById('f-guild').value,
              channel: document.getElementById('f-channel').value,
              player: document.getElementById('f-player').value
            }}
          }}, '*');
        }}, 360);
      }}
    </script>
  """, height=120 if show_filters else 55, key="filter_component")

  # Read filter values from session state (set by the component above on toggle)
  guild_id = st.session_state.get("filter_guild", "")
  channel_id = st.session_state.get("filter_channel", "")
  player_id = st.session_state.get("filter_player", "")

  # Handle component return value
  component_val = st.session_state.get("filter_component")
  if isinstance(component_val, dict) and component_val.get("action") == "toggle_filters":
    new_open = component_val.get("open", show_filters)
    if new_open != show_filters:
      st.session_state["show_filters"] = new_open
      st.session_state["filter_guild"] = component_val.get("guild", "")
      st.session_state["filter_channel"] = component_val.get("channel", "")
      st.session_state["filter_player"] = component_val.get("player", "")
      st.rerun()

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
    ta_str = f"<span style='font-family:DM Mono,monospace;color:#CC0000;font-size:0.95rem;margin-left:0.4rem;font-weight:500;'>{' & '.join(ta_scores)}</span>" if ta_scores else ""
    tb_str = f"<span style='font-family:DM Mono,monospace;color:#CC0000;font-size:0.95rem;margin-left:0.4rem;font-weight:500;'>{' & '.join(tb_scores)}</span>" if tb_scores else ""
    res_text = get_result_text(match)
    guild = match.get("guildName", "")
    channel = match.get("channelName", "")
    time_span = f'<span class="ts" data-ts="{ts}"></span>' if ts else ""

    # Card + button rendered as a single HTML block to eliminate the gap
    components.html(f"""
      <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        .card {{
          background: #161616;
          border: 1px solid #1e1e1e;
          border-left: 3px solid #CC0000;
          border-bottom: none;
          padding: 0.85rem 1.1rem 0.75rem;
          font-family: 'DM Sans', sans-serif;
        }}
        .sc-btn {{
          display: block;
          width: 100%;
          background: #1a1a1a;
          border: 1px solid #1e1e1e;
          border-top: none;
          color: #666;
          font-family: 'DM Mono', monospace;
          font-size: 0.72rem;
          letter-spacing: 1.5px;
          text-transform: uppercase;
          padding: 0.5rem;
          text-align: center;
          cursor: pointer;
          transition: background 0.15s, color 0.15s;
          border-radius: 0 0 2px 2px;
        }}
        .sc-btn:hover {{ background: #CC0000; color: #fff; border-color: #CC0000; }}
        .meta {{ font-family: 'DM Mono', monospace; font-size: 0.58rem; font-weight: 500; color: #3a3a3a; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.35rem; }}
        .teams {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.35rem; letter-spacing: 1.5px; color: #e8e8e8; margin-bottom: 0.45rem; }}
        .score {{ font-family: 'DM Mono', monospace; color: #CC0000; font-size: 0.9rem; margin-left: 0.35rem; }}
        .vs {{ color: #252525; font-size: 0.85rem; margin: 0 0.35rem; }}
        .result-pill {{
          display: inline-flex; align-items: center;
          background: #111; border: 1px solid #1e1e1e;
          color: #888; font-family: 'DM Mono', monospace;
          font-size: 0.65rem; font-weight: 500;
          padding: 0.2rem 0.65rem; border-radius: 2px;
          text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .res-label {{ color: #CC0000; margin-right: 5px; }}
      </style>

      <div class="card">
        <div class="meta">{time_span} {guild} · {channel}</div>
        <div class="teams">
          {team_a}<span class="score">{' & '.join(ta_scores) if ta_scores else ''}</span>
          <span class="vs">VS</span>
          {team_b}<span class="score">{' & '.join(tb_scores) if tb_scores else ''}</span>
        </div>
        <div class="result-pill"><span class="res-label">RES</span>{res_text}</div>
      </div>
      <button class="sc-btn" onclick="
        window.parent.postMessage({{type:'streamlit:setComponentValue', value:{{action:'go_scorecard', id:'{mid}'}}}}, '*');
      ">Scorecard →</button>

      <script>
        document.querySelectorAll('.ts').forEach(function(el) {{
          var d = new Date(parseInt(el.getAttribute('data-ts')) * 1000);
          el.textContent = d.toLocaleString([], {{dateStyle:'medium', timeStyle:'short'}}) + ' ·';
        }});
      </script>
    """, height=130, key=f"card_{mid}")

    # Handle scorecard navigation from card button
    card_val = st.session_state.get(f"card_{mid}")
    if isinstance(card_val, dict) and card_val.get("action") == "go_scorecard":
      st.query_params["id"] = card_val["id"]
      st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

params = st.query_params
match_id = params.get("id", None)
if match_id:
  page_scorecard(match_id)
else:
  page_list()
