import requests
import sqlite3
import json

# --- CONFIGURATION ---
API_KEY = "46ec4458de0c4628f7d4a21a6cdda9bd241753c2" 
# Removed internal quotes to prevent Serper 400 Bad Request
SEARCH_QUERY = "hackathon 2026 India register now -inurl:list -inurl:best"
DB_NAME = "hackathons.db"

BLACKLIST = [
    "devpost.com", "unstop.com", "hackerearth.com", "medium.com", 
    "geeksforgeeks.org", "linkedin.com", "eventbrite.com", "topcoder.com"
]

def fetch_and_save_hackathons():
    print(f"Connecting to Serper.dev for: {SEARCH_QUERY}")
    
    url = "https://google.serper.dev/search"
    # Using a slightly lower 'num' (20) to ensure compatibility with all Serper tiers
    payload = json.dumps({
        "q": SEARCH_QUERY,
        "gl": "in",
        "hl": "en",
        "num": 20
    })
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        
        # If it fails, print the actual error message from Serper to debug
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return

        results = response.json().get('organic', [])

        if not results:
            print("No results found.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hackathons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                location TEXT,
                date TEXT
            )
        ''')

        cursor.execute('DELETE FROM hackathons')

        added_count = 0
        for item in results:
            link = item.get('link', '#')
            title = item.get('title', 'No Title')
            snippet = item.get('snippet', 'No details available')

            # Skip aggregator domains
            if any(domain in link.lower() for domain in BLACKLIST):
                continue
            
            # Skip listicle titles
            list_keywords = ['top', 'best', 'list', 'upcoming', 'series', 'roundup']
            if any(word in title.lower() for word in list_keywords):
                continue

            cursor.execute('''
                INSERT INTO hackathons (title, link, location, date)
                VALUES (?, ?, ?, ?)
            ''', (title, link, "India/Online", snippet[:150]))
            added_count += 1

        conn.commit()
        conn.close()
        print(f"✅ Successfully updated database with {added_count} specific hackathons!")

    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    fetch_and_save_hackathons()