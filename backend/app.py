from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "tasklin.db"

# ---------------- DB ----------------
def get_db():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # CERTIFICATES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        link TEXT
    )
    """)

    # PROFILE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        username TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        college TEXT,
        skills TEXT,
        bio TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- WAITING ROOM ----------------
waiting_rooms = {}

# ---------------- AUTH ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data["username"], data["password"])
        )
        conn.commit()
        return jsonify({"msg": "signup success"})
    except:
        return jsonify({"msg": "user exists"}), 400


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    ).fetchone()

    if user:
        return jsonify({"msg": "success"})
    return jsonify({"msg": "invalid"}), 401


# ---------------- PROFILE ----------------
@app.route("/api/update_profile", methods=["POST"])
def update_profile():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO profiles (username, name, email, college, skills, bio)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(username) DO UPDATE SET
        name=excluded.name,
        email=excluded.email,
        college=excluded.college,
        skills=excluded.skills,
        bio=excluded.bio
    """, (
        data["username"],
        data["name"],
        data["email"],
        data["college"],
        data["skills"],
        data["bio"]
    ))

    conn.commit()
    return jsonify({"msg": "saved"})


@app.route("/api/get_profile/<username>")
def get_profile(username):
    conn = get_db()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT name, email, college, skills, bio FROM profiles WHERE username=?",
        (username,)
    ).fetchone()

    if row:
        return jsonify({
            "name": row[0],
            "email": row[1],
            "college": row[2],
            "skills": row[3],
            "bio": row[4]
        })

    return jsonify({})


# ---------------- CERTIFICATES ----------------
@app.route("/api/add_certificate", methods=["POST"])
def add_cert():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO certificates VALUES (NULL, ?, ?, ?)",
        (data["username"], data["name"], data["link"])
    )
    conn.commit()

    return jsonify({"msg": "added"})


@app.route("/api/get_certificates/<username>")
def get_certificates(username):
    conn = get_db()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT name, link FROM certificates WHERE username=?",
        (username,)
    ).fetchall()

    return jsonify([{"name": r[0], "link": r[1]} for r in rows])


# ---------------- HACKATHONS ----------------
@app.route("/api/hackathons")
def get_hackathons():
    conn = sqlite3.connect("hackathons.db")
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT title, link, location, date FROM hackathons"
    ).fetchall()

    return jsonify([
        {
            "title": r[0],
            "link": r[1],
            "location": r[2],
            "date": r[3]
        } for r in rows
    ])


# ---------------- WAITING ROOM ----------------
@app.route("/api/join_waiting", methods=["POST"])
def join_waiting():
    data = request.json
    h = data["hackathon"]

    waiting_rooms.setdefault(h, [])

    if not any(u["username"] == data["username"] for u in waiting_rooms[h]):
        waiting_rooms[h].append(data)

    return jsonify({"msg": "joined"})


@app.route("/api/leave_waiting", methods=["POST"])
def leave_waiting():
    data = request.json
    h = data["hackathon"]

    if h in waiting_rooms:
        waiting_rooms[h] = [
            u for u in waiting_rooms[h]
            if u["username"] != data["username"]
        ]

    return jsonify({"msg": "left"})


@app.route("/api/get_waiting/<hackathon>")
def get_waiting(hackathon):
    users = waiting_rooms.get(hackathon, [])
    return jsonify({
        "count": len(users),
        "users": users
    })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=8000)