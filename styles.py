"""
styles.py — Global CSS injected into Streamlit.
Centralising styles here avoids scattered st.markdown() calls in UI code.
"""

BMS_CSS = """
<style>
/* ── Google Fonts ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── CSS Variables ─────────────────────────────────────────────── */
:root {
    --bms-red:        #dc2441;
    --bms-red-dark:   #a81830;
    --bms-red-glow:   rgba(220, 36, 65, 0.25);
    --bg-primary:     #0d0d0d;
    --bg-card:        #161616;
    --bg-card-hover:  #1f1f1f;
    --bg-elevated:    #1a1a1a;
    --text-primary:   #f5f5f5;
    --text-secondary: #9a9a9a;
    --text-muted:     #555;
    --border:         #2a2a2a;
    --border-hover:   #3d3d3d;
    --success:        #22c55e;
    --warning:        #f59e0b;
    --gold:           #fbbf24;
    --radius-sm:      8px;
    --radius-md:      12px;
    --radius-lg:      20px;
}

/* ── Global Reset ──────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid var(--border) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Scrollbar ─────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* ── Typography ────────────────────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 1px;
}

/* ── Navbar ────────────────────────────────────────────────────── */
.bms-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 28px;
    background: rgba(13,13,13,0.96);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
    margin: -1rem -1rem 2rem -1rem;
}
.bms-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    color: var(--bms-red);
    letter-spacing: 3px;
    text-shadow: 0 0 20px var(--bms-red-glow);
}
.bms-logo span { color: var(--text-primary); }
.bms-nav-pills { display: flex; gap: 8px; }
.bms-pill {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    background: var(--bg-card);
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.2s;
}
.bms-pill:hover, .bms-pill.active {
    color: var(--bms-red);
    border-color: var(--bms-red);
    background: var(--bms-red-glow);
}

/* ── Hero Banner ───────────────────────────────────────────────── */
.bms-hero {
    background: linear-gradient(
        135deg,
        rgba(220,36,65,0.12) 0%,
        rgba(13,13,13,0) 60%
    ),
    repeating-linear-gradient(
        0deg,
        transparent,
        transparent 40px,
        rgba(255,255,255,0.015) 40px,
        rgba(255,255,255,0.015) 41px
    );
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 40px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.bms-hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(220,36,65,0.15), transparent 70%);
    pointer-events: none;
}
.bms-hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px;
    color: var(--text-primary);
    line-height: 1;
    margin: 0 0 8px;
}
.bms-hero-title em {
    color: var(--bms-red);
    font-style: normal;
}
.bms-hero-sub {
    color: var(--text-secondary);
    font-size: 15px;
    margin: 0;
}

/* ── Section Headers ───────────────────────────────────────────── */
.bms-section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 20px;
}
.bms-section-header h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 26px;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: 2px;
}
.bms-section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border), transparent);
}
.bms-badge {
    padding: 3px 10px;
    background: var(--bms-red);
    color: white;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ── Movie Cards ───────────────────────────────────────────────── */
.movie-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    height: 100%;
}
.movie-card:hover {
    border-color: var(--bms-red);
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 0 1px var(--bms-red-glow);
}
.movie-poster {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    background: var(--bg-elevated);
}
.movie-poster-placeholder {
    width: 100%;
    aspect-ratio: 2/3;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #1a1a2e, #16213e, #0f3460);
    font-size: 52px;
}
.movie-info {
    padding: 14px;
}
.movie-title {
    font-weight: 700;
    font-size: 14px;
    color: var(--text-primary);
    margin: 0 0 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.movie-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 10px;
}
.tag {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    background: var(--bg-elevated);
    color: var(--text-secondary);
    border: 1px solid var(--border);
}
.tag-genre  { color: #60a5fa; border-color: rgba(96,165,250,0.3); background: rgba(96,165,250,0.08); }
.tag-lang   { color: #a78bfa; border-color: rgba(167,139,250,0.3); background: rgba(167,139,250,0.08); }
.tag-rating { color: var(--gold); border-color: rgba(251,191,36,0.3); background: rgba(251,191,36,0.08); }
.movie-seats {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 12px;
}
.movie-seats.low { color: var(--warning); }
.movie-seats.sold { color: var(--bms-red); }
.movie-price {
    font-weight: 700;
    font-size: 16px;
    color: var(--text-primary);
}
.movie-price span {
    font-size: 11px;
    font-weight: 400;
    color: var(--text-muted);
}

/* ── Booking Panel ─────────────────────────────────────────────── */
.booking-panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px;
    position: sticky;
    top: 80px;
}
.booking-panel-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 20px;
    color: var(--text-primary);
    letter-spacing: 2px;
    margin: 0 0 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
}
.booking-summary {
    background: var(--bg-elevated);
    border-radius: var(--radius-sm);
    padding: 16px;
    margin: 16px 0;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 8px;
}
.summary-row:last-child { margin: 0; }
.summary-row .val {
    color: var(--text-primary);
    font-weight: 600;
}
.summary-total {
    display: flex;
    justify-content: space-between;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    padding-top: 12px;
    margin-top: 12px;
    border-top: 1px solid var(--border);
}
.summary-total .amount { color: var(--bms-red); }

/* ── Seat Picker ───────────────────────────────────────────────── */
.seat-grid {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 20px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    margin: 16px 0;
}
.seat-screen {
    width: 80%;
    height: 4px;
    background: linear-gradient(to right, transparent, var(--bms-red), transparent);
    border-radius: 2px;
    margin-bottom: 20px;
    position: relative;
}
.seat-screen::after {
    content: 'SCREEN';
    position: absolute;
    top: 10px; left: 50%;
    transform: translateX(-50%);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 2px;
}
.seat-row { display: flex; gap: 5px; }
.seat {
    width: 26px; height: 26px;
    border-radius: 5px 5px 3px 3px;
    border: 1px solid var(--border);
    background: var(--bg-elevated);
    cursor: pointer;
    transition: all 0.15s;
    font-size: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
}
.seat:hover  { background: rgba(220,36,65,0.2); border-color: var(--bms-red); }
.seat.taken  { background: #2a2a2a; border-color: #333; cursor: not-allowed; opacity: 0.4; }
.seat.picked { background: var(--bms-red); border-color: var(--bms-red-dark); color: white; }
.seat-legend {
    display: flex; gap: 20px;
    font-size: 11px; color: var(--text-secondary);
    margin-top: 10px;
}
.legend-dot {
    width: 12px; height: 12px;
    border-radius: 3px;
    display: inline-block;
    margin-right: 5px;
    vertical-align: middle;
}

/* ── Buttons ───────────────────────────────────────────────────── */
.stButton > button {
    background: var(--bms-red) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: var(--bms-red-dark) !important;
    box-shadow: 0 4px 20px var(--bms-red-glow) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Form Inputs ───────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > textarea {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: var(--bms-red) !important;
    box-shadow: 0 0 0 2px var(--bms-red-glow) !important;
}

/* ── Selectbox ─────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: var(--bg-elevated) !important;
    border-color: var(--border) !important;
}

/* ── Slider ────────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] > div > div > div {
    background: var(--bms-red) !important;
}

/* ── Tabs ──────────────────────────────────────────────────────── */
[data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--bms-red) !important;
    color: white !important;
    border-radius: 6px !important;
}

/* ── Sidebar Refinements ───────────────────────────────────────── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-secondary) !important;
}
[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px;
    font-size: 18px !important;
}

/* ── Booking History Card ──────────────────────────────────────── */
.history-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: border-color 0.2s;
}
.history-card:hover { border-color: var(--border-hover); }
.history-movie-name {
    font-weight: 700;
    font-size: 15px;
    color: var(--text-primary);
    margin: 0 0 4px;
}
.history-meta {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    gap: 14px;
}
.history-amount {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 24px;
    color: var(--bms-red);
    letter-spacing: 1px;
}
.history-seats {
    font-size: 12px;
    color: var(--text-secondary);
    text-align: right;
}

/* ── Status Banners ────────────────────────────────────────────── */
.banner {
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    font-size: 14px;
    font-weight: 500;
    margin: 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.banner-success {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80;
}
.banner-error {
    background: rgba(220,36,65,0.1);
    border: 1px solid rgba(220,36,65,0.3);
    color: #f87171;
}
.banner-info {
    background: rgba(96,165,250,0.08);
    border: 1px solid rgba(96,165,250,0.25);
    color: #93c5fd;
}

/* ── Divider ───────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Metric widgets ────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    color: var(--bms-red) !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 36px !important;
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
[data-testid="stMetricDelta"] svg { display: none; }

/* ── Spinner ───────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--bms-red) !important; }

/* ── Expander ──────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Notification toast ────────────────────────────────────────── */
.stAlert { border-radius: var(--radius-sm) !important; }

/* ── Mobile responsiveness ─────────────────────────────────────── */
@media (max-width: 768px) {
    .bms-hero-title { font-size: 36px; }
    .bms-navbar { padding: 12px 16px; }
}
</style>
"""


def inject_css() -> None:
    """Call once in main.py to apply the global theme."""
    import streamlit as st
    st.markdown(BMS_CSS, unsafe_allow_html=True)
