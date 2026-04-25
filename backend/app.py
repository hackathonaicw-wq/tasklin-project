from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hackathons.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

setup_database()

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

@app.route('/api/hackathons', methods=['GET'])
def fetch_stored_hackathons():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM hackathons').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    print("🚀 TASKLIN BACKEND STARTING ON PORT 8000...")
    app.run(debug=True, port=8000)
