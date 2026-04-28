import streamlit as st
import requests
import datetime


API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Tasklin", layout="wide")

# ───────────── SAFE REQUEST ─────────────
def safe_get(url):
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.text.strip():
            return res.json()
        return []
    except:
        return []

def safe_post(url, data):
    try:
        return requests.post(url, json=data)
    except:
        return None

# ───────────── SESSION ─────────────
if "user" not in st.session_state:
    st.session_state.user = None

# ───────────── LOGIN / SIGNUP ─────────────
if not st.session_state.user:
    st.title("🔐 Tasklin Login")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = safe_post(f"{API}/api/login", {
                "username": username,
                "password": password
            })

            if res and res.status_code == 200:
                data = res.json()
                if "username" in data:
                    st.session_state.user = data["username"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    # SIGNUP
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Signup"):
            res = safe_post(f"{API}/api/signup", {
                "username": new_user,
                "password": new_pass
            })

            if res and res.status_code == 200:
                st.success("Account created! Login now.")
            else:
                st.error("Signup failed")

    st.stop()

# ───────────── SIDEBAR ─────────────
st.sidebar.title("Menu")

page = st.sidebar.radio("Go to", [
    "Profile",
    "Certificates",
    "Hackathons"
])

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

user = st.session_state.user

# ───────────── PROFILE ─────────────
if page == "Profile":
    st.title("👤 Profile")

    data = safe_get(f"{API}/api/profile/{user}")

    full_name = st.text_input("Full Name", data.get("full_name", ""))
    email = st.text_input("Email", data.get("email", ""))
    college = st.text_input("College", data.get("college", ""))
    skills = st.text_input("Skills", data.get("skills", ""))
    bio = st.text_area("Bio", data.get("bio", ""))
    resume = st.text_input("Resume Link", data.get("resume", ""))

    if st.button("Save Profile"):
        safe_post(f"{API}/api/profile/update", {
            "username": user,
            "full_name": full_name,
            "email": email,
            "college": college,
            "skills": skills,
            "bio": bio,
            "resume": resume
        })
        st.success("Saved!")

    # Share link
    if data.get("share_id"):
        st.info(f"🔗 Share Profile: http://127.0.0.1:8000/api/share/{data['share_id']}")

# ───────────── CERTIFICATES ─────────────
elif page == "Certificates":
    st.title("🏆 Certificates")

    name = st.text_input("Hackathon Name")
    link = st.text_input("Certificate Link")

    if st.button("Add Certificate"):
        safe_post(f"{API}/api/add_certificate", {
            "username": user,
            "name": name,
            "link": link
        })
        st.success("Added!")

    certs = safe_get(f"{API}/api/get_certificates/{user}")

    st.subheader("Your Certificates")

    if not certs:
        st.warning("No certificates yet")
    else:
        for c in certs:
            st.markdown(f"### {c['name']}")
            st.link_button("View Certificate", c["link"])
            st.divider()

# ───────────── HACKATHONS ─────────────
elif page == "Hackathons":
    st.title("🚀 Hackathons")

    hacks = safe_get(f"{API}/api/hackathons")

    if not hacks:
        st.warning("No hackathons available")
    else:
        for h in hacks:
            with st.container():
                st.subheader(h["title"])
                st.write("📍", h["location"])
                st.write("📅", h["date"])

                if h.get("link"):
                    st.link_button("View", h["link"])

                # WAITING ROOM INSIDE EACH HACKATHON
                st.markdown("### 🤝 Join Waiting Room")

                skills = st.text_input(f"Skills_{h['id']}")
                team_size = st.number_input(f"Team Size_{h['id']}", min_value=2, max_value=10, value=3)

                if st.button(f"Join_{h['id']}"):
                    safe_post(f"{API}/api/join_waiting", {
                        "hackathon_id": h["id"],
                        "username": user,
                        "skills": skills,
                        "team_size": team_size
                    })
                    st.success("Joined waiting room")

                # SHOW WAITING USERS
                waiting = safe_get(f"{API}/api/waiting/{h['id']}")

                if waiting:
                    st.write("👥 Waiting:")
                    for w in waiting:
                        st.write(f"- {w['username']} ({w['skills']})")

                    if st.button(f"Form Team_{h['id']}"):
                        res = safe_get(f"{API}/api/form_team/{h['id']}")
                        st.success(res)

                st.divider()
=======
# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="TASKLIN 2026", page_icon="🚀", layout="wide")

# ── Global CSS: Deep Black Theme ──────────────────────────────────────────────
st.markdown("""
<style>
/* Typography & Base Font */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Full Black Theme */
.stApp { 
    background-color: #000000 !important; 
    color: #ffffff !important; 
}

/* Hide standard Streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 900px; }

/* Header bar Styling (TASKLIN Logo) */
.ht-logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;
}
.ht-logo-icon {
    width: 32px; height: 32px; background: #ffffff;
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    color: #000000; font-size: 16px;
}

/* Hackathon List (Transparent Backgrounds) */
.ht-card {
    background-color: transparent !important; 
    color: #ffffff !important;                
    border: none !important;                  
    border-bottom: 1px solid #333333 !important; 
    padding: 1.5rem 0; 
    margin-bottom: 0.5rem;
}
.ht-card-title { 
    font-size: 18px; 
    font-weight: 700; 
    color: #ffffff !important; 
    margin-bottom: 8px; 
}
.ht-card-meta { 
    font-size: 14px; 
    color: #9ca3af !important; 
    display: flex; 
    gap: 15px; 
}

/* Auth forms and Profile Containers */
.ht-form-card {
    background-color: #111111 !important; 
    color: #ffffff !important;
    border: 1px solid #333333; border-radius: 16px;
    padding: 2rem 2.25rem; max-width: 440px; margin: 3rem auto;
    text-align: center;
}

.ht-hero { text-align: center; padding: 2.5rem 0; color: #ffffff; }
.ht-hero h1 { font-size: 2.2rem; font-weight: 800; color: #ffffff; }

/* Form Inputs Visibility Correction */
label { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Session State Management ──────────────────────────────────────────────────
# Force immediate redirect to login page
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login' 
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

# Ensure this URL has NO trailing spaces or slashes
API_URL = "http://127.0.0.1:8000/api"

def go(page):
    """Refreshes Streamlit to show a new page state."""
    st.session_state['page'] = page
    st.rerun()

# ── Header with Profile Dropdown ─────────────────────────────────────────────
def render_header():
    """Renders the top navigation bar with the popover dropdown."""
    col_l, col_r = st.columns([6, 2])
    with col_l:
        st.markdown('<div class="ht-logo"><div class="ht-logo-icon">🚀</div>TASKLIN 2026</div>', unsafe_allow_html=True)
    with col_r:
        if st.session_state['logged_in']:
            user_display = st.session_state['user_data'].get('username', 'User')
            with st.popover(f"👤 {user_display}"):
                if st.button("👤 My Profile", use_container_width=True):
                    go('profile')
                if st.button("🚀 Logout", use_container_width=True):
                    st.session_state['logged_in'] = False
                    st.session_state['user_data'] = {}
                    go('login')

# ── Authentication View (Login/Signup) ────────────────────────────────────────
def show_auth(mode):
    """Renders the login or signup forms."""
    title = "Login" if mode == 'login' else "Create Account"
    st.markdown(f'<div class="ht-form-card"><h2>{title}</h2></div>', unsafe_allow_html=True)
    
    u = st.text_input("Username", key=f"{mode}_u", placeholder="Enter username")
    p = st.text_input("Password", type="password", key=f"{mode}_p", placeholder="••••••••")
    
    if mode == 'login':
        if st.button("Sign In", type="primary", use_container_width=True):
            try:
                # Use a timeout to prevent the app from hanging
                res = requests.post(f"{API_URL}/login", json={"username": u, "password": p}, timeout=5)
                if res.status_code == 200:
                    st.session_state['logged_in'] = True
                    st.session_state['user_data'] = res.json()['user']
                    go('home')
                else:
                    st.error("Invalid credentials.")
            except Exception as e:
                # Provides actual error details instead of just "Offline"
                st.error(f"Backend Connection Error: {e}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("New here? Create Tasklin Account"): 
            go('signup')
            
    else:
        if st.button("Register Now", type="primary", use_container_width=True):
            try:
                res = requests.post(f"{API_URL}/signup", json={"username": u, "password": p}, timeout=5)
                if res.status_code == 201:
                    st.success("Account created! Please login.")
                    go('login')
                else:
                    st.error("Username already exists.")
            except Exception as e:
                st.error(f"Backend Connection Error: {e}")
        
        if st.button("Back to Login"): 
            go('login')

# ── Profile View ──────────────────────────────────────────────────────────────
def show_profile():
    """Renders the editable user details form."""
    st.markdown("<div class='ht-hero'><h1>👤 My Profile</h1></div>", unsafe_allow_html=True)
    user = st.session_state['user_data']
    
    with st.form("profile_edit"):
        c1, c2 = st.columns(2)
        with c1:
            fn = st.text_input("Full Name", value=user.get('full_name') or "")
            em = st.text_input("Email", value=user.get('email') or "")
            
            # Date conversion for st.date_input
            curr_dob = None
            if user.get('dob'):
                try: curr_dob = datetime.datetime.strptime(user['dob'], '%Y-%m-%d').date()
                except: pass
            dob = st.date_input("Date of Birth", value=curr_dob)
            
        with c2:
            gender = st.selectbox("Gender", ["Female", "Male", "Other"], index=0)
            cl = st.text_input("College", value=user.get('college') or "")
            sk = st.text_area("Skills", value=user.get('skills') or "")
            
        if st.form_submit_button("Save Changes"):
            payload = {
                "username": user['username'], "full_name": fn, "email": em, 
                "college": cl, "skills": sk, "dob": dob.strftime('%Y-%m-%d') if dob else "", 
                "gender": gender
            }
            try:
                res = requests.post(f"{API_URL}/update_profile", json=payload, timeout=5)
                if res.status_code == 200:
                    st.session_state['user_data'].update(payload)
                    st.success("Profile Saved!")
            except Exception as e:
                st.error(f"Update failed: {e}")
            
    if st.button("← Back to Dashboard"): 
        go('home')

# ── Home Dashboard ────────────────────────────────────────────────────────────
def show_home():
    """Displays the hackathon list on the black background."""
    st.markdown("<div class='ht-hero'><h1>🚀 TASKLIN Dashboard</h1></div>", unsafe_allow_html=True)
    try:
        # Fetching hackathons from your working backend
        data = requests.get(f"{API_URL}/hackathons", timeout=5).json()
        
        search = st.text_input("", placeholder="🔍 Search hackathons...", label_visibility="collapsed")
        filtered = [h for h in data if search.lower() in (h['title'] + h['location']).lower()] if search else data
        
        if not filtered:
            st.info("No hackathons found matching your search.")
        
        for h in filtered:
            st.markdown(f"""
            <div class="ht-card">
                <div class="ht-card-title">{h['title']}</div>
                <div class="ht-card-meta">📅 {h.get('date', 'TBA')} | 📍 {h.get('location', 'India')}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("View Details", h.get('link', '#'), use_container_width=True)
            
    except Exception as e:
        st.error(f"Could not load hackathons: {e}")

# ── Main Routing Logic ────────────────────────────────────────────────────────
# This gating structure ensures the login page is shown first
if not st.session_state['logged_in']:
    if st.session_state['page'] == 'signup':
        show_auth('signup')
    else:
        show_auth('login') # Forced entry page
else:
    render_header()
    st.markdown("<hr style='border:none; border-top: 1px solid #333333; margin: 0 0 1.5rem;'>", unsafe_allow_html=True)
    if st.session_state['page'] == 'profile':
        show_profile()
    else:
        show_home()

