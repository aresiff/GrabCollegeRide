# GrabCollegeRide

GrabCollegeRide is a Django web application for students and drivers to sign up,
find and manage college rides, and handle ride bookings.

## Run locally on Windows

### Requirements

- Python 3.10–3.12
- PowerShell

### Setup

1. Clone the repository and open its folder:

   ```powershell
   git clone https://github.com/aresiff/GrabCollegeRide.git
   cd GrabCollegeRide
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, allow scripts for the current terminal
   session and activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Set a secret key for this PowerShell session:

   ```powershell
   $env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

   The key is only needed locally and should not be committed to GitHub. Set it
   again in a new terminal session before running the project.

5. Create the local SQLite database and apply migrations:

   ```powershell
   python manage.py migrate
   ```

6. Start the development server:

   ```powershell
   python manage.py runserver
   ```

7. Open <http://127.0.0.1:8000/ticket/> in your browser. The Django admin is at
   <http://127.0.0.1:8000/admin/>.

To create an admin account for the admin site, run this in another activated
terminal with `DJANGO_SECRET_KEY` set:

```powershell
python manage.py createsuperuser
```

## Notes

- The project uses SQLite. The database file is created locally by migrations
  and is intentionally excluded from Git.
- Django's built-in development server is for local development, not production
  deployment.
