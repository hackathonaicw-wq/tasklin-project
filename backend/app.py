from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import uuid

app = Flask(__name__)
CORS(app)


# ───────────── DATABASE ─────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasklin.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



# ───────────── SETUP ─────────────
def setup():
    conn = get_db()

    # USERS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        email TEXT,
        college TEXT,
        skills TEXT,
        bio TEXT,
        resume TEXT,
        share_id TEXT
    )
    """)

    # CERTIFICATES
    conn.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        link TEXT
    )
    """)

    # HACKATHONS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS hackathons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        location TEXT,
        date TEXT,
        link TEXT
    )
    """)

    # WAITING ROOM
    conn.execute("""
    CREATE TABLE IF NOT EXISTS waiting_room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hackathon_id INTEGER,
        username TEXT,
        skills TEXT,
        team_size INTEGER
    )
    """)

    # INSERT SAMPLE DATA (ONLY ONCE)
    count = conn.execute("SELECT COUNT(*) FROM hackathons").fetchone()[0]

    if count == 0:
        conn.execute("""
        INSERT INTO hackathons (title, location, date, link)
        VALUES 
        ('Goldman Sachs India Hackathon 2026', 'India/Online',
         'Registrations Open: April 22 - May 10',
         'https://www.goldmansachs.com'),

        ('Energize India Hackathon 2026', 'India/Online',
         'March - April 2026',
         'https://myevents.3ds.com')
        """)


def setup_database():
    """Initializes tables for TASKLIN."""
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     username TEXT UNIQUE, 
                     password TEXT,
                     full_name TEXT,
                     dob TEXT,
                     email TEXT,
                     gender TEXT,
                     college TEXT,
                     skills TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS hackathons 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title TEXT, link TEXT, location TEXT, date TEXT)''')

    conn.commit()
    conn.close()

setup()

# ───────────── AUTH ─────────────
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db()

    try:
        conn.execute("""
        INSERT INTO users (username, password, share_id)
        VALUES (?, ?, ?)
        """, (data["username"], data["password"], str(uuid.uuid4())))

        conn.commit()
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error", "msg": "User exists"})



@app.route("/api/login", methods=["POST"])
def login():

@app.route('/api/login', methods=['POST'])
def authenticate_user():
    """Checks credentials and returns full user data."""

    data = request.json
    conn = get_db()

    user = conn.execute("""
    SELECT * FROM users WHERE username=? AND password=?
    """, (data["username"], data["password"])).fetchone()

    if user:

        return jsonify(dict(user))
    return jsonify({"status": "fail"})


# ───────────── PROFILE ─────────────
@app.route("/api/profile/<username>")
def get_profile(username):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    return jsonify(dict(user))


@app.route("/api/profile/update", methods=["POST"])
def update_profile():
    data = request.json
    conn = get_db()

    conn.execute("""
    UPDATE users SET full_name=?, email=?, college=?, skills=?, bio=?, resume=?
    WHERE username=?
    """, (
        data["full_name"],
        data["email"],
        data["college"],
        data["skills"],
        data["bio"],
        data["resume"],
        data["username"]
    ))

    conn.commit()
    return jsonify({"status": "updated"})


# ───────────── SHARE PROFILE ─────────────
@app.route("/api/share/<share_id>")
def share_profile(share_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE share_id=?", (share_id,)).fetchone()
    return jsonify(dict(user))


# ───────────── CERTIFICATES ─────────────
@app.route("/api/add_certificate", methods=["POST"])
def add_cert():
    data = request.json
    conn = get_db()

    conn.execute("""
    INSERT INTO certificates (username, name, link)
    VALUES (?, ?, ?)
    """, (data["username"], data["name"], data["link"]))

    conn.commit()
    return jsonify({"status": "added"})


@app.route("/api/get_certificates/<username>")
def get_certs(username):
    conn = get_db()
    rows = conn.execute("""
    SELECT * FROM certificates WHERE username=?
    """, (username,)).fetchall()

    return jsonify([dict(r) for r in rows])


# ───────────── HACKATHONS ─────────────
@app.route("/api/hackathons")
def hackathons():
    conn = get_db()
    rows = conn.execute("SELECT * FROM hackathons").fetchall()
    return jsonify([dict(r) for r in rows])


# ───────────── WAITING ROOM ─────────────
@app.route("/api/join_waiting", methods=["POST"])
def join_waiting():
    data = request.json
    conn = get_db()

    conn.execute("""
    INSERT INTO waiting_room (hackathon_id, username, skills, team_size)
    VALUES (?, ?, ?, ?)
    """, (
        data["hackathon_id"],
        data["username"],
        data["skills"],
        data["team_size"]
    ))

    conn.commit()
    return jsonify({"status": "joined"})


@app.route("/api/waiting/<hackathon_id>")
def get_waiting(hackathon_id):
    conn = get_db()
    rows = conn.execute("""
    SELECT * FROM waiting_room WHERE hackathon_id=?
    """, (hackathon_id,)).fetchall()

    return jsonify([dict(r) for r in rows])


@app.route("/api/form_team/<hackathon_id>")
def form_team(hackathon_id):
    conn = get_db()

    users = conn.execute("""
    SELECT * FROM waiting_room WHERE hackathon_id=?
    """, (hackathon_id,)).fetchall()

    if not users:
        return jsonify({"status": "no users"})

    team_size = users[0]["team_size"]

    if len(users) >= team_size:
        selected = users[:team_size]

        for u in selected:
            conn.execute("DELETE FROM waiting_room WHERE id=?", (u["id"],))

        conn.commit()

        return jsonify({
            "status": "team formed",
            "team": [dict(u) for u in selected]
        })

    return jsonify({"status": "not enough users"})


# ───────────── RUN ─────────────
if __name__ == "__main__":
    print("🚀 Backend running on http://127.0.0.1:8000")
    app.run(debug=True, port=8000)

        return jsonify({"result": "success", "user": dict(user)}), 200
    return jsonify({"result": "failed"}), 401

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    """Updates profile details in the database."""
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('''UPDATE users 
                        SET full_name=?, dob=?, email=?, gender=?, college=?, skills=? 
                        WHERE username=?''', 
                     (data['full_name'], data['dob'], data['email'], 
                      data['gender'], data['college'], data['skills'], data['username']))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"}), 200
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

@app.route('/api/hackathons', methods=['GET'])
def fetch_stored_hackathons():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM hackathons').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    print("🚀 TASKLIN BACKEND STARTING ON PORT 8000...")
    app.run(debug=True, port=8000)
