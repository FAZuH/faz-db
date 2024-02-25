@echo off

call .venv/Scripts/activate
python -m kans
call .venv/Scripts/deactivate

pause
