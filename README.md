# tasklin-project

# 🚀 Tasklin – Smart Hackathon Finder & Collaboration Platform

Tasklin is a modern web application that helps students discover hackathons and find compatible teammates efficiently using smart search, filtering, and skill-based matching.

---

## 🌟 Features

### 🔍 Hackathon Finder
- Search hackathons using keywords
- Smart filtering across title, location, and date
- Modern responsive UI with interactive hackathon cards
- Direct links to official hackathon pages
- Dynamic frontend updates using API data

### 🤝 Teammate Finder
- Create and manage user profiles
- Add skills, interests, and contact details
- Skill-based teammate matching system
- Highlighted “Good Match” suggestions
- Clean and interactive collaboration interface

---

## 🧠 How It Works

- Backend (Flask) provides APIs for hackathon and teammate data
- Frontend (Streamlit) dynamically fetches and displays data
- Interactive UI improves navigation and user experience
- Smart keyword search helps users quickly find hackathons
- Skill-based matching suggests compatible teammates
- Real-time frontend updates ensure smooth interaction between frontend and backend

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Modern Interactive UI)
- **Backend:** Flask REST API
- **API Communication:** Requests
- **Data Storage:** JSON
- **UI Design:** Custom CSS Styling & Responsive Layouts

---

## 📂 Project Structure

```bash
tasklin-project/
│
├── backend/
│   ├── app.py
│   └── fetch.py
│
├── frontend/
│   └── ui.py
│
├── data/
│   ├── hackathons.json
│   └── users.json
│
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Start Backend

```bash
cd backend
python fetch.py
python app.py
```

### 2️⃣ Start Frontend

```bash
cd frontend
streamlit run ui.py
```

---

## 🎯 Project Goal

The goal of Tasklin is to simplify hackathon discovery and help students build strong teams by connecting people with similar skills and interests through an easy-to-use platform.

---

## 🚀 Future Enhancements

- Authentication System
- Real Database Integration
- AI-based Team Recommendations
- Live Chat System
- Hackathon Bookmarking
- Cloud Deployment
