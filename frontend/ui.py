import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="TASKLIN", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if not st.session_state.user:

    st.title("🚀 TASKLIN")

    mode = st.radio("Select", ["Login", "Signup"])

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button(mode):
        url = "/api/login" if mode == "Login" else "/api/signup"

        r = requests.post(API + url, json={
            "username": user,
            "password": pwd
        })

        if r.status_code == 200:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Error")

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
    st.title("Profile")

    res = requests.get(f"{API}/api/get_profile/{st.session_state.user}")
    p = res.json()

    name = st.text_input("Name", p.get("name", st.session_state.user))
    email = st.text_input("Email", p.get("email", ""))
    college = st.text_input("College", p.get("college", ""))
    skills = st.text_input("Skills", p.get("skills", ""))
    bio = st.text_area("Bio", p.get("bio", ""))

    if st.button("Save"):
        requests.post(f"{API}/api/update_profile", json={
            "username": st.session_state.user,
            "name": name,
            "email": email,
            "college": college,
            "skills": skills,
            "bio": bio
        })
        st.success("Saved ✅")


# ---------------- CERTIFICATES ----------------
elif menu == "Certificates":
    st.title("Certificates")

    name = st.text_input("Certificate")
    link = st.text_input("Link")

    if st.button("Add"):
        requests.post(f"{API}/api/add_certificate", json={
            "username": st.session_state.user,
            "name": name,
            "link": link
        })

    data = requests.get(
        f"{API}/api/get_certificates/{st.session_state.user}"
    ).json()

    for c in data:
        st.write(f"📜 {c['name']} - {c['link']}")


# ---------------- HACKATHONS ----------------
elif menu == "Hackathons":

    st.title("🌐 TASKLIN Hackathons")

    filt = st.radio("Filter", ["All", "Online", "Offline"])

    hacks = requests.get(f"{API}/api/hackathons").json()

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
            if st.button("🚀 Join", key=h["title"]):
                requests.post(f"{API}/api/join_waiting", json={
                    "username": st.session_state.user,
                    "hackathon": h["title"],
                    "skills": "Python"
                })
                st.rerun()

        with col2:
            if st.button("❌ Leave", key=h["title"]+"leave"):
                requests.post(f"{API}/api/leave_waiting", json={
                    "username": st.session_state.user,
                    "hackathon": h["title"]
                })
                st.rerun()


        w = requests.get(
            f"{API}/api/get_waiting/{h['title']}"
        ).json()

        st.info(f"👥 {w['count']} people waiting")

        for u in w["users"]:
            st.write(f"• {u['username']} ({u['skills']})")

        st.divider()