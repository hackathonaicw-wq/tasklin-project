import streamlit as st
import requests

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