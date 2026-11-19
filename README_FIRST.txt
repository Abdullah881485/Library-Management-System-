LIBRA - LIBRARY MANAGEMENT SYSTEM (BEGINNER EDITION)

WHAT YOU NEED
1. Install Python 3.11, 3.12, or 3.13 from https://www.python.org/downloads/
   IMPORTANT: during installation, tick "Add Python to PATH".
2. Install Visual Studio Code from https://code.visualstudio.com/
3. Internet connection (for Google Fonts and Tailwind browser CDN used in the demo).

HOW TO OPEN
1. Extract this ZIP file.
2. Open the extracted "library_management_system" folder in VS Code.
3. In VS Code, choose Terminal > New Terminal.
4. Run these commands one by one:

   python -m venv venv

   Windows PowerShell:
   .\venv\Scripts\Activate.ps1

   If PowerShell blocks activation, use Command Prompt terminal instead:
   venv\Scripts\activate.bat

   python -m pip install -r requirements.txt

5. Create database tables:

   python manage.py makemigrations core
   python manage.py migrate

6. Create your administrator account:

   python manage.py createsuperuser

   Enter a username, email and password. Password characters do not appear while typing; this is normal.
   A superuser automatically has administrator access.

7. Start the website:

   python manage.py runserver

8. Open this address in Chrome or Edge:
   http://127.0.0.1:8000/

HOW TO USE
- Sign in with the administrator account you created.
- Add Categories first.
- Add Authors second.
- Add Books third.
- Register a normal member using the Register link (or sign out and register).
- Copy the member's Library ID from their dashboard.
- Sign back in as administrator and open Issue & return.
- Enter the member's Library ID, select a book and issue it.
- Sign in as the member to see their borrowed book and due date.
- Admin can mark a loan as returned from Issue & return.

PASSWORD RESET NOTE
This local project uses Django's console email backend. When a user requests a password reset,
the reset link is printed in the VS Code terminal running "python manage.py runserver".
This is for local demonstration only. A real deployed website needs an email provider.

IMPORTANT NOTES
- The project uses SQLite. The database file db.sqlite3 is created automatically after migrations.
- Tailwind's browser CDN is included to make the beginner setup easier. It needs internet and is
  suitable for a classroom/demo project, not an optimized production deployment.
- Uploaded book cover URLs are optional.
- Never share your administrator password.
- Do not delete db.sqlite3 if you want to keep your project data.
- This is a learning/demo project. Before public deployment, set DEBUG=False, use a strong
  SECRET_KEY, configure ALLOWED_HOSTS, HTTPS, email delivery and production static files.
