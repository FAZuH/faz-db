@echo off

call .venv/Scripts/activate
python -m vindicator
call .venv/Scripts/deactivate

pause
