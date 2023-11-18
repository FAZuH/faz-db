@echo off

call .venv/Scripts/activate
python src/main.py
call .venv/Scripts/deactivate

pause
