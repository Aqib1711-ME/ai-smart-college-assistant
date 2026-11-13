# AI Smart College Assistant – Student Chatbot

A small college mini-project built with Flask, HTML, CSS, JavaScript and SQLite. It includes a built-in FAQ fallback and optional OpenAI-powered answers.

## Features
- Responsive student chat interface
- Flask JSON chat endpoint
- Built-in FAQ answers for common student topics
- Optional OpenAI API integration (API key stays on the server)
- SQLite storage for user messages and bot replies
- Health-check endpoint at `/health`

## Requirements
- Python 3.10 or newer
- pip
- Optional: an OpenAI API key for AI-generated responses

## Run locally (Windows)
1. Extract the ZIP and open the project folder in VS Code or a terminal.
2. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`.
5. (Optional) Add your API key to `.env` as `OPENAI_API_KEY=your_key_here`. Never paste the key into frontend JavaScript or commit `.env` to GitHub.
6. Start the server:
   ```powershell
   python app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.

Without an API key, the app still works using the built-in FAQ fallback.

## Publish online using Render + GitHub
1. Create a GitHub account (if you do not have one) and create a **private** repository for the project.
2. Upload the project files, excluding `.env`, `.venv`, and `chat_history.db`.
3. Sign in to Render and choose **New → Web Service**, then connect your GitHub repository.
4. Render can read `render.yaml`; otherwise set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. In Render environment variables, set `FLASK_SECRET_KEY` to a long random value. Optionally set `OPENAI_API_KEY` and `OPENAI_MODEL`.
6. Deploy and open the Render URL. Test `/health` and send a chat message.

### Important deployment notes
- A free hosting instance may sleep when idle and may have usage limits.
- The SQLite database is local to the running instance. On hosting platforms with ephemeral filesystems, chat history may be lost after redeploy/restart. For persistent production storage, use a managed PostgreSQL database or a persistent disk and update the database layer.
- Do not use this demo as an official source of college policy. Replace the sample FAQ answers with verified, institution-approved information before real student use.
- Add authentication, rate limiting, abuse monitoring, privacy notice/consent and retention controls before collecting real student data.
- Never publish API keys or student chat logs in a public repository.

## Project structure
```text
ai-smart-college-assistant/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## API
`POST /api/chat`
```json
{"message": "How can I get exam information?"}
```
Returns:
```json
{"reply": "Please refer to ...", "mode": "FAQ"}
```

`GET /health` returns `{"status":"ok"}`.

## Database
SQLite table `chat_logs`:
- `id`: primary key
- `user_message`: student's message
- `bot_response`: assistant response
- `created_at`: UTC timestamp

## Testing checklist
- [ ] Home page loads at `/`
- [ ] FAQ prompt returns an appropriate fallback answer
- [ ] Empty message is rejected
- [ ] Message over 1500 characters is rejected
- [ ] Chat messages are stored in SQLite
- [ ] Optional AI response works with a valid API key
- [ ] App falls back to FAQ if AI is unavailable
- [ ] `/health` returns status `ok`

## Academic integrity / feature status
Implemented in this starter: Flask app, web chat UI, FAQ fallback, optional OpenAI integration, SQLite chat logging and health endpoint.
Not implemented: student login, admin dashboard, live college database integration, official notices feed, timetable integration, file uploads, analytics, or institution-specific policy engine. These are possible future enhancements.
