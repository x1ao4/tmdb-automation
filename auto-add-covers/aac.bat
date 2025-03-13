@echo off

set DIR=%~dp0

cd /d %DIR%

python3 auto-add-covers.py

pause
