# vehicle-parking-app

MAD II Project
for linux based systems:

python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
python3 main.py

cd frontend
npm install
npm run dev

celery -A main:celery_app worker -l INFO
celery -A main:celery_app beat -l INFO
~/go/bin/MailHog
