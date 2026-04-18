from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # This is crucial so your frontend can talk to this backend

# Helper function to connect to the database you seeded
def get_db_connection():
    conn = sqlite3.connect('hackathons.db')
    # This row_factory line is a lifesaver—it lets you access data by column name 
    # like row['title'] instead of row[0]
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "The Hackathon Aggregator API is live!"

# 1. ROUTE TO GET ALL HACKATHONS
@app.route('/api/hackathons', methods=['GET'])
def get_hackathons():
    try:
        conn = get_db_connection()
        query = 'SELECT * FROM hackathons'
        
        # Optional: Add a search filter if you want to be fancy
        search = request.args.get('q')
        if search:
            query += f" WHERE title LIKE '%{search}%' OR category LIKE '%{search}%'"
            
        hackathons = conn.execute(query).fetchall()
        conn.close()

        # Convert the SQLite rows into a list of dictionaries for JSON
        result = [dict(row) for row in hackathons]
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. ROUTE TO GET A SINGLE HACKATHON BY ID
@app.route('/api/hackathons/<int:id>', methods=['GET'])
def get_hackathon_detail(id):
    conn = get_db_connection()
    hackathon = conn.execute('SELECT * FROM hackathons WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if hackathon is None:
        return jsonify({"message": "Hackathon not found"}), 404
        
    return jsonify(dict(hackathon))

if __name__ == '__main__':
    # During the hackathon, keep debug=True so it restarts when you save
    app.run(debug=True, port=5000)