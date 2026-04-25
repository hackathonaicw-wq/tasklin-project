from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import json

app = Flask(__name__)
CORS(app)

# ── Database setup ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hackathons.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     username TEXT UNIQUE, 
                     password TEXT)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS hackathons 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title TEXT, link TEXT, location TEXT, date TEXT)''')

    conn.commit()
    conn.close()

setup_database()

# ── Auth APIs ─────────────────────────────────────────────
@app.route('/api/signup', methods=['POST'])
def register_user():
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                     (data['username'], data['password']))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"}), 201
    except:
        return jsonify({"result": "error", "message": "User exists"}), 400


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
@app.route('/api/hackathons', methods=['GET'])
def fetch_stored_hackathons():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM hackathons').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


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