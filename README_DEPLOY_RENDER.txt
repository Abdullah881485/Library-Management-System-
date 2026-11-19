DEPLOY TO RENDER (Django + PostgreSQL)

1. Push this project folder to a GitHub repository.
2. In Render, create a PostgreSQL database. Copy its Internal Database URL.
3. Create a new Render Web Service and connect the GitHub repository.
4. Runtime: Python 3.12 (or a supported current Python version).
5. Build Command: bash build.sh
6. Start Command: gunicorn config.wsgi:application
7. Add environment variables to the Web Service:
   SECRET_KEY = a long random secret value
   DEBUG = False
   DATABASE_URL = the PostgreSQL Internal Database URL from Render
   ALLOWED_HOSTS = your-service-name.onrender.com
   CSRF_TRUSTED_ORIGINS = https://your-service-name.onrender.com
8. Deploy. After deployment, open the service Shell and run:
   python manage.py createsuperuser
9. Use that account to sign in as the admin.

IMPORTANT:
- Do not use SQLite for a public Render deployment; use PostgreSQL so data persists.
- Replace the example host above with your actual Render hostname.
- The password-reset email backend is still console-only; real email delivery needs SMTP configuration.
- Tailwind CDN needs internet access in the visitor's browser.
