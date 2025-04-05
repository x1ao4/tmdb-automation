@echo off

set DIR=%~dp0

cd /d %DIR%

python3 auto-update-episodes.py

pause
