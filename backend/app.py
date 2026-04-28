from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
<<<<<<< HEAD
import json
=======
>>>>>>> origin/nish

app = Flask(__name__)
CORS(app)

<<<<<<< HEAD
# ── Database setup ─────────────────────────────────────────────
=======
>>>>>>> origin/nish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hackathons.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
<<<<<<< HEAD
=======
    """Initializes tables for TASKLIN."""
>>>>>>> origin/nish
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     username TEXT UNIQUE, 
<<<<<<< HEAD
                     password TEXT)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS hackathons 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title TEXT, link TEXT, location TEXT, date TEXT)''')

=======
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
>>>>>>> origin/nish
    conn.commit()
    conn.close()

setup_database()

<<<<<<< HEAD
# ── Auth APIs ─────────────────────────────────────────────
=======
>>>>>>> origin/nish
@app.route('/api/signup', methods=['POST'])
def register_user():
    data = request.json
    try:
        conn = get_db_connection()
<<<<<<< HEAD
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
=======
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
>>>>>>> origin/nish
                     (data['username'], data['password']))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"}), 201
    except:
        return jsonify({"result": "error", "message": "User exists"}), 400

<<<<<<< HEAD

@app.route('/api/login', methods=['POST'])
def authenticate_user():
    data = request.json
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (data['username'], data['password'])
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"result": "success", "user": user['username']}), 200
    return jsonify({"result": "failed"}), 401


# ── Hackathon API ─────────────────────────────────────────────
=======
@app.route('/api/login', methods=['POST'])
def authenticate_user():
    """Checks credentials and returns full user data."""
    data = request.json
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                        (data['username'], data['password'])).fetchone()
    conn.close()
    if user:
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

>>>>>>> origin/nish
@app.route('/api/hackathons', methods=['GET'])
def fetch_stored_hackathons():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM hackathons').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

<<<<<<< HEAD

# ── Teammate System (Day 4) ───────────────────────────────────
USERS_FILE = os.path.join(BASE_DIR, "../data/users.json")

@app.route("/api/users", methods=["GET"])
def get_users():
    if not os.path.exists(USERS_FILE):
        return jsonify([])

    with open(USERS_FILE) as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/add_user", methods=["POST"])
def add_user():
    new_user = request.json

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            data = json.load(f)
    else:
        data = []

    data.append(new_user)

    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

    return jsonify({"message": "User added"})


# ── Run server ─────────────────────────────────────────────
if __name__ == '__main__':
    print("🚀 BACKEND STARTING ON PORT 8000...")
    app.run(debug=True, port=8000)
=======
if __name__ == '__main__':
    print("🚀 TASKLIN BACKEND STARTING ON PORT 8000...")
    app.run(debug=True, port=8000)
>>>>>>> origin/nish
