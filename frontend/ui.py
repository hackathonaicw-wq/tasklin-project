import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="TASKLIN 2026", page_icon="🚀", layout="wide")

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
    font-size: 18px;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.5px;
}
.ht-logo-icon {
    width: 32px; height: 32px;
    background: #1a1a2e;
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
    font-size: 2.2rem;
    font-weight: 800;
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
.ht-card-title { font-size: 17px; font-weight: 600; color: #1a1a2e; margin-bottom: 6px; }
.ht-card-meta { font-size: 13px; color: #6b7280; display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 10px; }
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

/* ── Auth forms ── */
.ht-form-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 2rem 2.25rem;
    max-width: 440px;
    margin: 2rem auto 0;
    text-align: center;
}
.ht-form-title { font-size: 24px; font-weight: 800; color: #1a1a2e; margin-bottom: 0.25rem; }
.ht-form-sub   { font-size: 14px; color: #6b7280; margin-bottom: 1.5rem; }

.ht-section-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
# Set default page to 'login' for the initial popup
for key, default in [('logged_in', False), ('page', 'login'), ('username', '')]:
    if key not in st.session_state:
        st.session_state[key] = default

API_URL = "http://127.0.0.1:8000/api"

# ── Helpers ───────────────────────────────────────────────────────────────────
def go(page):
    st.session_state['page'] = page
    st.rerun()

def tag_class(location: str) -> str:
    loc = (location or '').lower()
    if any(word in loc for word in ['online', 'remote', 'virtual']):
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
            <div class="ht-logo-icon">T</div>
            TASKLIN 2026
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        if st.session_state['logged_in']:
            ua, ub = st.columns([2, 1])
            ua.markdown(f"<div style='padding-top:6px;font-size:14px;text-align:right;'>👤 <b>{st.session_state['username']}</b></div>",
                        unsafe_allow_html=True)
            if ub.button("Logout", use_container_width=True):
                st.session_state['logged_in'] = False
                st.session_state['username'] = ''
                go('login')

# ── Login Page ────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""
    <div class="ht-form-card">
        <div class="ht-form-title">Welcome to TASKLIN</div>
        <div class="ht-form-sub">Please sign in to continue</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        user = st.text_input("Username", placeholder="e.g. nish_01")
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Sign In", use_container_width=True, type="primary"):
            try:
                res = requests.post(f"{API_URL}/login", json={"username": user, "password": pwd})
                if res.status_code == 200:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user
                    go('home')
                else:
                    st.error("Invalid username or password.")
            except:
                st.error("Backend server is not responding (Port 8000).")

        st.markdown("<div style='text-align:center; margin:1rem 0; color:#9ca3af;'>OR</div>", unsafe_allow_html=True)
        if st.button("Create new account", use_container_width=True):
            go('signup')

# ── Signup Page ───────────────────────────────────────────────────────────────
def show_signup():
    st.markdown("""
    <div class="ht-form-card">
        <div class="ht-form-title">Join TASKLIN</div>
        <div class="ht-form-sub">Create your account to start tracking events</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        new_user = st.text_input("Choose Username")
        new_pwd = st.text_input("Choose Password", type="password")
        
        if st.button("Register Now", use_container_width=True, type="primary"):
            try:
                res = requests.post(f"{API_URL}/signup", json={"username": new_user, "password": new_pwd})
                if res.status_code == 201:
                    st.success("Account created successfully!")
                    st.info("You can now login with your credentials.")
                else:
                    st.error("Username already exists.")
            except:
                st.error("Could not reach backend server.")
        
        if st.button("← Back to Login", use_container_width=True):
            go('login')

# ── Home Page (Dashboard) ─────────────────────────────────────────────────────
def show_home():
    st.markdown(f"""
    <div class="ht-hero">
        <h1>🚀 TASKLIN Dashboard</h1>
        <p>Discover and track the best hackathons in 2026.<br>Handpicked events for developers.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        hackathons = requests.get(f"{API_URL}/hackathons").json()
    except:
        st.error("⚠️ Backend Connection Failed. Is app.py running?")
        return

    if not hackathons:
        st.warning("No hackathons found in database. Run fetch.py first!")
        return

    # Stats
    st.markdown(f"""
    <div class="ht-stats">
        <div class="ht-stat"><div class="ht-stat-num">{len(hackathons)}</div><div class="ht-stat-lbl">Active Events</div></div>
        <div class="ht-stat"><div class="ht-stat-num">2026</div><div class="ht-stat-lbl">Current Season</div></div>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("", placeholder="🔍 Search by name or location...", label_visibility="collapsed")
    
    filtered = [h for h in hackathons if search.lower() in (h['title'] + h['location']).lower()] if search else hackathons

    st.markdown(f"<div class='ht-section-label'>{len(filtered)} results</div>", unsafe_allow_html=True)

    for h in filtered:
        tc, label = tag_class(h.get('location', ''))
        with st.container():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class="ht-card">
                    <span class="ht-tag {tc}">{label}</span>
                    <div class="ht-card-title">{h['title']}</div>
                    <div class="ht-card-meta">
                        <span>📅 {h['date']}</span>
                        <span>📍 {h['location']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.link_button("View Details", h['link'], use_container_width=True)

# ── Main Routing Logic ────────────────────────────────────────────────────────
render_header()
st.markdown("<hr style='border:none; border-top: 1px solid #e5e7eb; margin: 0 0 1.5rem;'>", unsafe_allow_html=True)

# Force Auth check: Users cannot see 'home' unless logged_in is True
if not st.session_state['logged_in']:
    if st.session_state['page'] == 'signup':
        show_signup()
    else:
        show_login()
else:
    show_home()