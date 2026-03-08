@echo off
REM Production start script for Windows

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Install dependencies if needed
if "%1"=="--install" (
    pip install -r requirements.txt
)

REM Create necessary directories
if not exist documents mkdir documents
if not exist static\extracted_images mkdir static\extracted_images
if not exist content mkdir content

REM Run with gunicorn for production
where gunicorn >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PORT=%PORT%
    if "%PORT%"=="" set PORT=5000
    gunicorn --bind 0.0.0.0:%PORT% --workers 4 --timeout 120 app:app
) else (
    REM Fallback to Flask development server
    python app.py
)
