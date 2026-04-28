import streamlit as st
import requests
<<<<<<< HEAD

st.set_page_config(page_title="Tasklin", layout="wide")

API_URL = "http://127.0.0.1:8000"

st.title("🚀 Tasklin - Hackathon Finder")

# --- Hackathons Section ---
st.header("📢 Hackathons")

# Fetch hackathons with loading spinner
try:
    with st.spinner("Loading hackathons..."):
        hackathons = requests.get(f"{API_URL}/api/hackathons").json()
except:
    st.error("Backend not running")
    hackathons = []

# Search input
search = st.text_input("Search Hackathons").lower()

# Highlight search
if search:
    st.markdown(f"### 🔍 Results for: `{search}`")

found = False

# Display hackathons
if not hackathons:
    st.warning("⚠️ No hackathons available right now.")
else:
    for h in hackathons:
        title = h.get("title", "").lower()
        location = h.get("location", "").lower()
        date = h.get("date", "").lower()

        keywords = title + " " + location + " " + date
        search_words = search.split()

        if search == "" or any(word in keywords for word in search_words):
            found = True

            with st.container():
                st.subheader(h.get("title", "No Title"))

                st.markdown(f"📍 **Location:** {h.get('location', 'N/A')}")
                st.markdown(f"📅 **Date:** {h.get('date', 'N/A')}")

                # Smart tags
                if "ai" in keywords:
                    st.caption("🤖 AI")
                if "web" in keywords:
                    st.caption("🌐 Web")
                if "data" in keywords:
                    st.caption("📊 Data")

                if h.get("link"):
                    st.link_button("🔗 View Hackathon", h["link"])

                st.divider()

# No match case
if hackathons and not found:
    st.warning("No matching hackathons found")

# Divider before next section
st.divider()

# ── Teammate Finder ────────────────────────────────
st.header("🤝 Teammate Finder")

name = st.text_input("Name")
skills = st.text_input("Skills (comma separated)")
looking_for = st.text_input("Looking For")
contact = st.text_input("Contact")

# Input validation
if st.button("Add Profile"):
    if not name or not skills or not contact:
        st.error("Please fill all required fields")
    else:
        requests.post(f"{API_URL}/add_user", json={
            "name": name,
            "skills": skills.split(","),
            "looking_for": looking_for.split(","),
            "contact": contact
        })
        st.success("Profile Added!")

st.subheader("Available Teammates")

try:
    users = requests.get(f"{API_URL}/users").json()
except:
    users = []

your_skills = st.text_input("Enter your skills (comma separated)")

if your_skills:
    your_skills_list = [s.strip().lower() for s in your_skills.split(",")]
else:
    your_skills_list = []

for u in users:
    user_skills = [s.lower() for s in u["skills"]]

    match = any(skill in user_skills for skill in your_skills_list)

    if your_skills_list == [] or match:
        st.markdown(f"### 👤 {u['name']}")
        st.markdown(f"🧠 **Skills:** {', '.join(u['skills'])}")
        st.markdown(f"🎯 **Looking For:** {', '.join(u['looking_for'])}")
        st.markdown(f"📞 **Contact:** {u['contact']}")

        if match:
            st.success("✅ Good Match")

        st.divider()

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Flask")
=======
import datetime

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
>>>>>>> origin/nish
