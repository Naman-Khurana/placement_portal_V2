# Placement Portal Application

## Prerequisites

- Python 3.x
- Node.js & npm
- Redis / Memurai (running)

---

## Backend

From the project root directory:

```bash
pip install -r requirements.txt
python app.py
```

Backend runs on:

```
http://localhost:5000
```

---

## Frontend

Navigate to:

```bash
cd placement_portal_frontend/placement_portal_frontend
```

Install dependencies (first time only):

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## Celery Worker

From the project root directory, run:

```bash
python -m celery -A celery_worker:celery worker --pool=solo --loglevel=info
```

---

## Celery Beat

From the project root directory, run:

```bash
python -m celery -A celery_worker:celery beat --loglevel=info
```

---

## Startup Order

1. Start Redis / Memurai.
2. Start the Flask backend.
3. Start the Celery Worker.
4. Start the Celery Beat Scheduler.
5. Start the Vue frontend.
