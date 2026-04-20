import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="HackTracker 2026", page_icon="🚀", layout="wide")

# 2. Session State Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# API URL
API_URL = "http://127.0.0.1:8000/api"

# --- NAVIGATION HEADER ---
def render_header():
    col_l, col_m, col_r = st.columns([1, 4, 1.5])
    
    with col_l:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state['page'] = 'home'
            st.rerun()

    with col_r:
        if not st.session_state['logged_in']:
            # The single Login/Signup button you requested
            if st.button("🔑 Login / Signup", use_container_width=True):
                st.session_state['page'] = 'login'
                st.rerun()
        else:
            u_col, out_col = st.columns([2, 1])
            u_col.write(f"👤 **{st.session_state['username']}**")
            if out_col.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['page'] = 'home'
                st.rerun()
    st.divider()

# --- LOGIN PAGE ---
def show_login():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login Now", use_container_width=True):
        try:
            res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['page'] = 'home'
                st.rerun()
            else:
                st.error("Invalid credentials.")
        except:
            st.error("Backend offline.")

    st.write("---")
    st.write("Don't have an account?")
    if st.button("Create a New Account (Sign Up)"):
        st.session_state['page'] = 'signup'
        st.rerun()

# --- SIGNUP PAGE ---
def show_signup():
    st.header("📝 Sign Up")
    new_user = st.text_input("Choose Username")
    new_pwd = st.text_input("Choose Password", type="password")
    
    if st.button("Register Account", use_container_width=True):
        try:
            res = requests.post(f"{API_URL}/signup", json={"username": new_user, "password": new_pwd})
            if res.status_code == 201:
                st.success("Account created successfully!")
                st.info("Now go to the Login page to enter your dashboard.")
            else:
                st.error("Username already taken.")
        except:
            st.error("Backend offline.")
            
    if st.button("← Back to Login"):
        st.session_state['page'] = 'login'
        st.rerun()

# --- DASHBOARD / HOME ---
def show_home():
    st.title("🚀 Upcoming Hackathons 2026")
    try:
        res = requests.get(f"{API_URL}/hackathons").json()
        if not res:
            st.info("No hackathons found. Make sure to run fetch.py!")
        for h in res:
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.subheader(h['title'])
                    st.write(f"📅 {h.get('date', 'TBA')} | 📍 {h.get('location', 'India')}")
                with c2:
                    st.write("##")
                    st.link_button("View Details", h['link'])
                st.divider()
    except:
        st.error("Could not connect to Backend.")

# --- ROUTING LOGIC ---
render_header()

if st.session_state['page'] == 'login':
    show_login()
elif st.session_state['page'] == 'signup':
    show_signup()
else:
    show_home()