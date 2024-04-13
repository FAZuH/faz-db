@echo off

call .venv/Scripts/activate
python -m wynndb
call .venv/Scripts/deactivate

pause
