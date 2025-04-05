@echo off

set DIR=%~dp0

cd /d %DIR%

python3 auto-add-backdrops.py

pause
