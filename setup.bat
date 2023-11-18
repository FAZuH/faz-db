@echo off
color 5

python --version 2>&1 | findstr /C:"3.11." >nul
if %errorlevel%==0 (
    echo Python 3.11.0 or higher is already installed
) else (
    echo Python 3.11.0 or higher is not installed
    echo Please install Python 3.11.0 or higher and add it to your PATH
)

cd /d "%~dp0"

python -m venv .venv
call .venv\Scripts\activate
echo Installing Requirements...
python -m pip install -r requirements.txt
call .venv\Scripts\deactivate
