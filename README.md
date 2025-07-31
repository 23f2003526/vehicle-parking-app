# 🚗 vehicle-parking-app

**MAD II Project**
Platform: **Linux-based systems**

---

## 🔧 Backend Setup

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip3 install -r requirements.txt

# Run the backend server
python3 main.py
```

---

## 🌐 Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start the frontend development server
npm run dev
```

---

## ⚙️ Background Task Workers (Celery)

In separate terminals, run the following:

```bash
# Start Celery worker
celery -A main:celery_app worker -l INFO

# Start Celery beat scheduler
celery -A main:celery_app beat -l INFO
```

---

## 📬 Email Testing (MailHog)

Make sure MailHog is installed and accessible at `~/go/bin/MailHog`:

```bash
~/go/bin/MailHog
```

MailHog UI will be available at: [http://localhost:8025](http://localhost:8025)

---
