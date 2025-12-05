# AI Resume Match Platform

An end-to-end mini-project that scores job seeker resumes against curated job postings using TF-IDF similarity. The stack includes a FastAPI backend with SQLite + SQLAlchemy, a lightweight ML layer, and a static frontend.

## Features
- CRUD-ready job catalog with seed data.
- Resume submission endpoint that produces top AI matches.
- Persistent logging of scores for analytics.
- Frontend to view jobs and submit resumes.

## Project Structure
```
backend/
  app/
    main.py
    models.py
    routers/
    services/
    seed.py
  requirements.txt
frontend/
  index.html
  app.js
  styles.css
```

## Setup

1. **Backend environment**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Seed database**
   ```bash
   python -m app.seed
   ```

3. **Run API**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Frontend**
   Open `frontend/index.html` in a browser (or use a static server) and set `API_BASE` in `app.js` if the host differs.

## Extending
- Replace TF-IDF with fine-tuned transformer embeddings.
- Add authentication for recruiters/candidates.
- Deploy using Docker + managed Postgres for production readiness.




