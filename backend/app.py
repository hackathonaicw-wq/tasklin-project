from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
CORS(app)

DB = "tasklin.db"


# ---------------- DB ----------------
def get_db():
    return sqlite3.connect(DB)


# ---------------- AUTH ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users VALUES (?, ?)",
                   (data["username"], data["password"]))
    conn.commit()
    conn.close()

    return jsonify({"msg": "ok"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    ).fetchone()

    conn.close()

    if user:
        return jsonify({"msg": "ok"})
    return jsonify({"msg": "fail"}), 401


# ---------------- PROFILE ----------------
@app.route("/api/update_profile", methods=["POST"])
def update_profile():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO profiles
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["username"],
        data["name"],
        data["email"],
        data["college"],
        data["skills"],
        data["bio"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"msg": "saved"})


@app.route("/api/get_profile/<username>")
def get_profile(username):
    conn = get_db()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM profiles WHERE username=?",
        (username,)
    ).fetchone()

    conn.close()

    if not row:
        return jsonify({})

    return jsonify({
        "username": row[0],
        "name": row[1],
        "email": row[2],
        "college": row[3],
        "skills": row[4],
        "bio": row[5]
    })


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
    conn.close()

    return jsonify({"msg": "added"})


@app.route("/api/get_certificates/<username>")
def get_certificates(username):
    conn = get_db()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT name, link FROM certificates WHERE username=?",
        (username,)
    ).fetchall()

    conn.close()

    return jsonify([{"name": r[0], "link": r[1]} for r in rows])


# ---------------- HACKATHONS ----------------
@app.route("/api/hackathons")
def get_hackathons():
    conn = get_db()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT title, link, location, date FROM hackathons"
    ).fetchall()

    conn.close()

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
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO waiting VALUES (?, ?, ?)",
        (data["username"], data["hackathon"], data["skills"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "joined"})


@app.route("/api/leave_waiting", methods=["POST"])
def leave_waiting():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM waiting WHERE username=? AND hackathon=?",
        (data["username"], data["hackathon"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "left"})


@app.route("/api/get_waiting/<hackathon>")
def get_waiting(hackathon):
    conn = get_db()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT username, skills FROM waiting WHERE hackathon=?",
        (hackathon,)
    ).fetchall()

    conn.close()

    return jsonify({
        "count": len(rows),
        "users": [{"username": r[0], "skills": r[1]} for r in rows]
    })


# ---------------- RESUME (HTML) ----------------
@app.route("/api/resume/<username>")
def resume(username):
    conn = get_db()
    cursor = conn.cursor()

    p = cursor.execute(
        "SELECT * FROM profiles WHERE username=?",
        (username,)
    ).fetchone()

    certs = cursor.execute(
        "SELECT name, link FROM certificates WHERE username=?",
        (username,)
    ).fetchall()

    hacks = cursor.execute(
        "SELECT hackathon FROM waiting WHERE username=?",
        (username,)
    ).fetchall()

    conn.close()

    if not p:
        return "No profile found"

    # ✅ FIX 1: filter empty certificates
    cert_html = ""
    for c in certs:
        if not c[0].strip():
            continue
        cert_html += f"<li><a href='{c[1]}'>{c[0]}</a></li>"

    hack_html = "".join([f"<li>{h[0]}</li>" for h in hacks])

    html = f"""
    <html>
    <head>
        <title>{p[1]}</title>
        <style>
            body {{
                font-family: Arial;
                margin: 40px;
                color: #333;
            }}
            h1 {{ color: #2c3e50; }}
            h2 {{
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }}
        </style>
    </head>

    <body>

    <h1>{p[1]}</h1>

    <p><b>Email:</b> {p[2]}</p>
    <p><b>College:</b> {p[3]}</p>
    <p><b>Skills:</b> {p[4]}</p>

    <h2>Bio</h2>
    <p>{p[5]}</p>

    <h2>Certificates</h2>
    <ul>{cert_html}</ul>

    <h2>Hackathons Participated</h2>
    <ul>{hack_html}</ul>

    </body>
    </html>
    """

    return html


# ---------------- RESUME PDF ----------------
@app.route("/api/resume_pdf/<username>")
def resume_pdf(username):
    conn = get_db()
    cursor = conn.cursor()

    p = cursor.execute(
        "SELECT * FROM profiles WHERE username=?",
        (username,)
    ).fetchone()

    certs = cursor.execute(
        "SELECT name FROM certificates WHERE username=?",
        (username,)
    ).fetchall()

    conn.close()

    doc = SimpleDocTemplate(f"{username}_resume.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(p[1], styles["Title"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Email: {p[2]}", styles["Normal"]))
    content.append(Paragraph(f"College: {p[3]}", styles["Normal"]))
    content.append(Paragraph(f"Skills: {p[4]}", styles["Normal"]))

    content.append(Spacer(1, 10))
    content.append(Paragraph("Certificates", styles["Heading2"]))

    for c in certs:
        if not c[0].strip():  # ✅ FIX 2
            continue
        content.append(Paragraph(f"- {c[0]}", styles["Normal"]))

    doc.build(content)

    return send_file(f"{username}_resume.pdf", as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=8000)