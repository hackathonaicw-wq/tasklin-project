import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="HackTracker 2026", page_icon="🚀", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Typography & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 960px; }

/* ── Header bar ── */
.ht-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.25rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.ht-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 600;
    color: #1a1a2e;
}
.ht-logo-icon {
    width: 32px; height: 32px;
    background: #534AB7;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 16px;
}

/* ── Hero section ── */
.ht-hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.ht-hero h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.5rem;
}
.ht-hero p {
    font-size: 15px;
    color: #6b7280;
    max-width: 460px;
    margin: 0 auto 1.5rem;
    line-height: 1.7;
}

/* ── Stats row ── */
.ht-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
}
.ht-stat { text-align: center; }
.ht-stat-num { font-size: 22px; font-weight: 700; color: #534AB7; }
.ht-stat-lbl { font-size: 12px; color: #9ca3af; margin-top: 2px; }

/* ── Hackathon card ── */
.ht-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
}
.ht-card:hover { box-shadow: 0 4px 16px rgba(83,74,183,0.10); border-color: #c4bfee; }
.ht-card-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.ht-card-title { font-size: 17px; font-weight: 600; color: #1a1a2e; margin-bottom: 6px; }
.ht-card-meta { font-size: 13px; color: #6b7280; display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 10px; }
.ht-card-meta span { display: flex; align-items: center; gap: 5px; }
.ht-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
}
.ht-tag-online  { background:#E6F1FB; color:#0C447C; }
.ht-tag-offline { background:#E1F5EE; color:#085041; }
.ht-tag-hybrid  { background:#FAEEDA; color:#633806; }
.ht-tag-default { background:#EEEDFE; color:#3C3489; }

/* ── Auth forms ── */
.ht-form-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 2rem 2.25rem;
    max-width: 440px;
    margin: 2rem auto;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.ht-form-title { font-size: 22px; font-weight: 700; color: #1a1a2e; margin-bottom: 0.25rem; }
.ht-form-sub   { font-size: 14px; color: #6b7280; margin-bottom: 1.5rem; }

/* ── Section label ── */
.ht-section-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.75rem;
}

/* ── Empty state ── */
.ht-empty {
    text-align: center;
    padding: 3rem 1rem;
    color: #9ca3af;
}
.ht-empty-icon { font-size: 40px; margin-bottom: 1rem; }
.ht-empty p { font-size: 15px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [('logged_in', False), ('page', 'home'), ('username', '')]:
    if key not in st.session_state:
        st.session_state[key] = default

API_URL = "http://127.0.0.1:8000/api"


# ── Helpers ───────────────────────────────────────────────────────────────────
def go(page):
    st.session_state['page'] = page
    st.rerun()


def tag_class(location: str) -> str:
    loc = (location or '').lower()
    if 'online' in loc or 'remote' in loc or 'virtual' in loc:
        return 'ht-tag-online', 'Online'
    if 'hybrid' in loc:
        return 'ht-tag-hybrid', 'Hybrid'
    return 'ht-tag-offline', 'In person'


# ── Header ────────────────────────────────────────────────────────────────────
def render_header():
    col_l, col_r = st.columns([6, 2])

    with col_l:
        st.markdown("""
        <div class="ht-logo">
            <div class="ht-logo-icon">🚀</div>
            HackTracker 2026
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        if not st.session_state['logged_in']:
            if st.button("🔑  Login / Signup", use_container_width=True, type="primary"):
                go('login')
        else:
            ua, ub = st.columns([2, 1])
            ua.markdown(f"<div style='padding-top:6px;font-size:14px;'>👤 <b>{st.session_state['username']}</b></div>",
                        unsafe_allow_html=True)
            if ub.button("Logout", use_container_width=True):
                st.session_state['logged_in'] = False
                go('home')


# ── Login ─────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""
    <div class="ht-form-card">
        <div class="ht-form-title">Welcome back</div>
        <div class="ht-form-sub">Sign in to track your hackathons</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if st.button("Sign in", use_container_width=True, type="primary"):
            with st.spinner("Signing in…"):
                try:
                    res = requests.post(f"{API_URL}/login",
                                        json={"username": username, "password": password})
                    if res.status_code == 200:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.success("Logged in!")
                        go('home')
                    else:
                        st.error("Invalid username or password.")
                except Exception:
                    st.error("Could not reach the server. Is the backend running?")

        st.markdown("<div style='text-align:center; margin-top:1rem; font-size:14px; color:#6b7280;'>Don't have an account?</div>",
                    unsafe_allow_html=True)
        if st.button("Create account →", use_container_width=True):
            go('signup')


# ── Signup ────────────────────────────────────────────────────────────────────
def show_signup():
    st.markdown("""
    <div class="ht-form-card">
        <div class="ht-form-title">Create account</div>
        <div class="ht-form-sub">Join HackTracker to save and follow hackathons</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        new_user = st.text_input("Choose a username", placeholder="hackerman42")
        new_pwd  = st.text_input("Choose a password", type="password", placeholder="••••••••")

        if st.button("Register", use_container_width=True, type="primary"):
            with st.spinner("Creating account…"):
                try:
                    res = requests.post(f"{API_URL}/signup",
                                        json={"username": new_user, "password": new_pwd})
                    if res.status_code == 201:
                        st.success("Account created! You can now sign in.")
                    else:
                        st.error("That username is already taken.")
                except Exception:
                    st.error("Could not reach the server.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to login", use_container_width=True):
            go('login')


# ── Home / hackathon list ─────────────────────────────────────────────────────
def show_home():
    # Hero
    greeting = f"Welcome back, {st.session_state['username']}!" \
               if st.session_state['logged_in'] else "Discover hackathons near you"
    st.markdown(f"""
    <div class="ht-hero">
        <h1>🚀 Upcoming hackathons 2026</h1>
        <p>{greeting}<br>Find, track, and register for the best hackathons in India and globally.</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch data
    try:
        hackathons = requests.get(f"{API_URL}/hackathons").json()
    except Exception:
        st.error("⚠️  Could not connect to the backend. Make sure your server is running.")
        return

    if not hackathons:
        st.markdown("""
        <div class="ht-empty">
            <div class="ht-empty-icon">📭</div>
            <p>No hackathons found. Run <code>fetch.py</code> to populate the database.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Stats row
    st.markdown(f"""
    <div class="ht-stats">
        <div class="ht-stat"><div class="ht-stat-num">{len(hackathons)}</div><div class="ht-stat-lbl">Events listed</div></div>
        <div class="ht-stat"><div class="ht-stat-num">2026</div><div class="ht-stat-lbl">Season</div></div>
        <div class="ht-stat"><div class="ht-stat-num">Free</div><div class="ht-stat-lbl">Always</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Search
    search = st.text_input("", placeholder="🔍  Search hackathons by name, location…", label_visibility="collapsed")

    filtered = [h for h in hackathons
                if search.lower() in (h.get('title', '') + h.get('location', '')).lower()] \
               if search else hackathons

    if not filtered:
        st.info("No results match your search.")
        return

    st.markdown(f"<div class='ht-section-label'>{len(filtered)} events found</div>", unsafe_allow_html=True)

    # Cards
    for h in filtered:
        tc, label = tag_class(h.get('location', ''))
        with st.container():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class="ht-card">
                    <span class="ht-tag {tc}">{label}</span>
                    <div class="ht-card-title">{h.get('title', 'Untitled')}</div>
                    <div class="ht-card-meta">
                        <span>📅 {h.get('date', 'TBA')}</span>
                        <span>📍 {h.get('location', 'India')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.link_button("View →", h['link'], use_container_width=True)


# ── Router ────────────────────────────────────────────────────────────────────
render_header()
st.markdown("<hr style='border:none; border-top: 1px solid #e5e7eb; margin: 0 0 1rem;'>", unsafe_allow_html=True)

page = st.session_state['page']
if page == 'login':
    show_login()
elif page == 'signup':
    show_signup()
else:
    show_home()