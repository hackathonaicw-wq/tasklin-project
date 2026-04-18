import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="HackTracker 2026",
    page_icon="📅",
    layout="wide"
)

# 2. Styling (Hiding the default Streamlit footer)
hide_style = """
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 3. Header Section
st.title("📅 Upcoming Hackathons 2026")
st.markdown("Fetching the best engineering challenges live from Google.")
st.divider()

# 4. Connection to Flask Backend
# Make sure your app.py is running on port 5000!
BACKEND_URL = "http://127.0.0.1:5000/api/hackathons"

def fetch_data():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return None

# 5. Main UI Logic
hackathons = fetch_data()

if hackathons is None:
    st.error("❌ Cannot connect to the Backend. Please run 'python app.py' in your terminal.")
elif len(hackathons) == 0:
    st.warning("⚠️ No hackathons found. Make sure you've run 'python fetch.py' to populate the database.")
else:
    # Sidebar Search
    st.sidebar.header("Filter Results")
    search = st.sidebar.text_input("Search by Keyword (e.g. AI, India)")

    # Display Hackathons
    for h in hackathons:
        # Filter logic
        if search.lower() in h['title'].lower() or search.lower() in h['date'].lower():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.subheader(h['title'])
                    st.write(f"📍 **Location:** {h['location']}")
                    st.write(f"🕒 **Details:** {h['date']}")
                
                with col2:
                    st.write("##") # Spacing
                    st.link_button("View Original Search", h['link'], use_container_width=True)
                
                st.divider()

# 6. Sidebar Refresh Button
if st.sidebar.button("🔄 Refresh Page"):
    st.rerun()