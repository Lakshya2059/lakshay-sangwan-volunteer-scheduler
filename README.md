# Lakshay Sangwan — Community Event Volunteer Scheduler

Full-stack educational project.

- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- Database: SQLite
- Production web server for hosting: Gunicorn

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `python -m pip install -r requirements.txt` (on some Macs use `python3 -m pip install -r requirements.txt`).
4. Run `python app.py` (or `python3 app.py`).
5. Open http://127.0.0.1:5000.

## Publish on Render
1. Create a GitHub account at https://github.com/ and sign in.
2. Create a new repository, for example `lakshay-sangwan-volunteer-scheduler`.
3. Upload these project files (`app.py`, `requirements.txt`, `render.yaml`, `README.md`) to the repository root.
4. Go to https://render.com/ and sign in. Connect GitHub if asked.
5. Choose **New + → Web Service** and select your repository.
6. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Instance plan: Free (for a demo)
7. Click **Deploy Web Service** and wait until the status is Live. Render will show the public `onrender.com` URL. The name may need adjusting if already taken.
8. Open that URL and test event creation, registration, attendance, and conflict checks.

## Important hosting / data note
Render's free web service filesystem is ephemeral. The SQLite database can be reset when the service restarts or is redeployed, so this setup is suitable for a class demo, not important real-world records. For durable public use, switch the database to PostgreSQL or use a host/storage plan with a persistent disk. Free Render services may sleep after inactivity, so the first visit can take a little while.

## Demo checklist
- Create an event.
- Register a volunteer.
- Try the same email and same shift again to see validation.
- Mark a registration Present and confirm completed hours update.

This prototype does not include secure accounts, passwords, actual email reminders, or production-grade access control. Do not collect sensitive personal data.
