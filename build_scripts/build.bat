@echo off
REM Activate virtual environment and build EXE with PyInstaller

cd ..
call venv\Scripts\activate
pyinstaller --onefile --windowed --icon=assets\app_icon.ico --add-data "creds.json;." main.py
pause
