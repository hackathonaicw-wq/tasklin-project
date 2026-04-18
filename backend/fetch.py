import requests
import sqlite3
import json

# --- CONFIGURATION ---
# 1. Get your free API key from https://serper.dev
API_KEY = "46ec4458de0c4628f7d4a21a6cdda9bd241753c2" 
SEARCH_QUERY = "upcoming engineering hackathons India 2026"
DB_NAME = "hackathons.db"

def fetch_and_save_hackathons():
    print("Connecting to Google via Serper.dev...")
    
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": SEARCH_QUERY,
        "gl": "in",      # Geographic location: India
        "hl": "en",      # Host language: English
        "num": 20        # Number of results to fetch
    })
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        # 1. FETCH DATA FROM GOOGLE
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status() # Check for HTTP errors
        results = response.json().get('organic', [])

        if not results:
            print("No results found. Check your API key or query.")
            return

        # 2. CONNECT TO DATABASE
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 3. INITIALIZE TABLE (The "Self-Healing" part)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hackathons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                location TEXT,
                date TEXT
            )
        ''')

        # 4. CLEAR OLD DATA (So your website only shows current events)
        cursor.execute('DELETE FROM hackathons')

        # 5. INSERT NEW DATA
        for item in results:
            title = item.get('title', 'No Title')
            link = item.get('link', '#')
            # Google snippets often contain date/location info
            snippet = item.get('snippet', 'Check link for details')
            
            cursor.execute('''
                INSERT INTO hackathons (title, link, location, date)
                VALUES (?, ?, ?, ?)
            ''', (title, link, "India/Online", snippet[:100]))

        conn.commit()
        conn.close()
        print(f"Successfully updated database with {len(results)} live hackathons!")

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    fetch_and_save_hackathons()