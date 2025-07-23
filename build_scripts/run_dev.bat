@echo off
REM Navigate to project folder, activate venv, and run main.py

cd /d "%~dp0\.."
call venv\Scripts\activate
python main.py
pause
