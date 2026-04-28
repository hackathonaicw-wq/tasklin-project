import streamlit as st
import requests

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