import streamlit as st
import requests
import base64
import os

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="TASKLIN", layout="wide")

# ---------------- IMAGE BACKGROUND ----------------
def set_image_bg(image_file):
    image_path = os.path.join(os.path.dirname(__file__), image_file)

    if not os.path.exists(image_path):
        st.warning(f"{image_file} not found")
        return

    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .stTextInput>div>div>input {{
        background-color: rgba(255,255,255,0.05);
        color: white;
    }}

    .stTextArea textarea {{
        background-color: rgba(255,255,255,0.05);
        color: white;
    }}

    .stButton button {{
        border-radius: 10px;
        height: 45px;
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        color: white;
        border: none;
    }}

    h1, h2, h3, h4, h5, h6, p, label, span {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if not st.session_state.user:

    set_image_bg("login.jpg")

    st.markdown("## 🚀 TASKLIN")
    st.caption("Build teams • Discover hackathons • Showcase yourself")

    mode = st.radio("", ["Login", "Signup"], horizontal=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Continue"):
        url = "/api/login" if mode == "Login" else "/api/signup"

        try:
            r = requests.post(API + url, json={
                "username": user,
                "password": pwd
            })

            if r.status_code == 200:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")

        except Exception as e:
            st.error(f"Error: {e}")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 TASKLIN")
st.sidebar.write(f"👤 {st.session_state.user}")

menu = st.sidebar.radio("Menu", ["Profile", "Certificates", "Hackathons"])

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ---------------- PROFILE ----------------
if menu == "Profile":

    set_image_bg("profile.jpg")

    st.title("Profile")

    try:
        res = requests.get(f"{API}/api/get_profile/{st.session_state.user}")
        p = res.json()
    except Exception as e:
        st.error(f"Error: {e}")
        p = {}

    name = st.text_input("Name", p.get("name", ""))
    email = st.text_input("Email", p.get("email", ""))
    college = st.text_input("College", p.get("college", ""))
    skills = st.text_input("Skills", p.get("skills", ""))
    bio = st.text_area("Bio", p.get("bio", ""))

    if st.button("Save"):

        try:
            requests.post(f"{API}/api/update_profile", json={
                "username": st.session_state.user,
                "name": name,
                "email": email,
                "college": college,
                "skills": skills,
                "bio": bio
            })

            st.success("Saved ✅")

        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()

    resume_link = f"{API}/api/resume/{st.session_state.user}"
    pdf_link = f"{API}/api/resume_pdf/{st.session_state.user}"

    st.markdown(f"[🔗 View Resume]({resume_link})")

    if st.button("⬇ Download Resume"):
        st.markdown(f"[Click here]({pdf_link})")

# ---------------- CERTIFICATES ----------------
elif menu == "Certificates":

    set_image_bg("profile.jpg")

    st.title("Certificates")

    name = st.text_input("Certificate")
    link = st.text_input("Link")

    if st.button("Add"):

        try:
            requests.post(f"{API}/api/add_certificate", json={
                "username": st.session_state.user,
                "name": name,
                "link": link
            })

            st.success("Added ✅")
            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

    try:
        data = requests.get(
            f"{API}/api/get_certificates/{st.session_state.user}"
        ).json()

    except Exception as e:
        st.error(f"Error: {e}")
        data = []

    for c in data:
        col1, col2 = st.columns([4,1])

        with col1:
            st.write(f"📜 {c['name']} - {c['link']}")

        with col2:
            if st.button("❌", key=f"delete_{c['name']}_{c['link']}"):

                try:
                    requests.post(f"{API}/api/delete_certificate", json={
                        "username": st.session_state.user,
                        "name": c["name"]
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

# ---------------- HACKATHONS ----------------
elif menu == "Hackathons":

    set_image_bg("profile.jpg")

    st.title("🌐 Hackathons")

    filt = st.radio("Filter", ["All", "Online", "Offline"])

    try:
        hacks = requests.get(f"{API}/api/hackathons").json()

    except Exception as e:
        st.error(f"Error: {e}")
        hacks = []

    for h in hacks:

        if filt == "Online" and "online" not in h["location"].lower():
            continue

        if filt == "Offline" and "offline" not in h["location"].lower():
            continue

        st.subheader(h["title"])
        st.write(f"📍 {h['location']}")
        st.write(f"📅 {h['date']}")
        st.markdown(f"[🔗 View]({h['link']})")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🚀 Join",
                key=f"join_{h['title']}_{h['date']}"
            ):

                try:
                    requests.post(f"{API}/api/join_waiting", json={
                        "username": st.session_state.user,
                        "hackathon": h["title"],
                        "skills": "Python"
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

        with col2:
            if st.button(
                "❌ Leave",
                key=f"leave_{h['title']}_{h['date']}"
            ):

                try:
                    requests.post(f"{API}/api/leave_waiting", json={
                        "username": st.session_state.user,
                        "hackathon": h["title"]
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

        try:
            w = requests.get(
                f"{API}/api/get_waiting/{h['title']}"
            ).json()

            st.info(f"👥 {w['count']} people waiting")

            for u in w["users"]:
                st.write(f"• {u['username']} ({u['skills']})")

        except Exception as e:
            st.error(f"Error: {e}")

        st.divider()