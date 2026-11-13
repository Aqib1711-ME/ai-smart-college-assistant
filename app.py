import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-before-deployment")
DATABASE = os.getenv("DATABASE_PATH", "chat_history.db")

FAQS = [
    (["hello", "hi", "hey"], "Hello! I'm your Smart College Assistant. How can I help you today?"),
    (["admission", "apply", "application"], "For admission guidance, check your college's official admission notice or contact the admissions office. I don't have access to your college's live admission records."),
    (["library", "book"], "For library services, please check your college library's official timings, catalogue, and borrowing rules."),
    (["fee", "fees", "tuition"], "Fee amounts and deadlines vary by institution and semester. Please confirm the latest details with your college accounts office."),
    (["exam", "examination", "date sheet", "schedule"], "Please refer to the official examination notice or student portal for confirmed exam dates and schedules."),
    (["attendance", "absent"], "Attendance requirements are institution-specific. Please consult your department or the official student handbook."),
    (["contact", "office", "department"], "Please use the contact information published on your college's official website or notice board."),
    (["help", "what can you do"], "I can answer general student questions about admissions, fees, exams, attendance, library services, and college life. For official decisions, always verify with your college.")
]

def db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def faq_answer(message):
    msg = message.lower()
    for keywords, answer in FAQS:
        if any(word in msg for word in keywords):
            return answer
    return ("I don't have a verified answer for that yet. Please check your college's official "
            "website, student portal, or relevant office. You can also configure an AI API key "
            "to enable broader AI-generated answers.")

def ai_answer(message):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": (
                    "You are a helpful, respectful assistant for college students. "
                    "Give clear, concise general guidance. Never invent institution-specific "
                    "policies, dates, fees, contacts, or official decisions. If details depend "
                    "on a particular college, tell the student to verify with official sources."
                )},
                {"role": "user", "content": message}
            ],
            temperature=0.4,
            max_tokens=350
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        app.logger.exception("AI response failed; using FAQ fallback.")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please enter a message."}), 400
    if len(message) > 1500:
        return jsonify({"error": "Message is too long. Please keep it under 1500 characters."}), 400

    answer = ai_answer(message) or faq_answer(message)
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        with db() as conn:
            conn.execute(
                "INSERT INTO chat_logs (user_message, bot_response, created_at) VALUES (?, ?, ?)",
                (message, answer, timestamp)
            )
    except sqlite3.Error:
        app.logger.exception("Could not save chat log.")
    return jsonify({"reply": answer, "mode": "AI" if os.getenv("OPENAI_API_KEY") else "FAQ"})

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Page not found."}), 404

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
