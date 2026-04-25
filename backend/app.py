from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
# CORS is essential for Streamlit to communicate with this Flask API
CORS(app)

# Use absolute path to ensure we use the same DB file as fetch.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hackathons.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Initializes the required tables if they don't exist."""
    conn = get_db_connection()
    # Create users table for TASKLIN login/signup
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     username TEXT UNIQUE, 
                     password TEXT)''')
    # Create hackathons table to store scraped data
    conn.execute('''CREATE TABLE IF NOT EXISTS hackathons 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title TEXT, link TEXT, location TEXT, date TEXT)''')
    conn.commit()
    conn.close()

# Initialize the database on script startup
setup_database()

@app.route('/api/signup', methods=['POST'])
def register_user():
    """Handles new user registration."""
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                     (data['username'], data['password']))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"result": "error", "message": "Username already exists"}), 400
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def authenticate_user():
    """Handles user authentication."""
    data = request.json
    try:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                            (data['username'], data['password'])).fetchone()
        conn.close()
        if user:
            return jsonify({"result": "success", "user": user['username']}), 200
        return jsonify({"result": "failed", "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

@app.route('/api/hackathons', methods=['GET'])
def fetch_stored_hackathons():
    """Retrieves all hackathons stored in the database."""
    try:
        conn = get_db_connection()
        data = conn.execute('SELECT * FROM hackathons').fetchall()
        conn.close()
        return jsonify([dict(row) for row in data])
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Running on port 8000 to match the UI's API_URL
    print("🚀 TASKLIN BACKEND STARTING ON PORT 8000...")
    app.run(debug=True, port=8000)