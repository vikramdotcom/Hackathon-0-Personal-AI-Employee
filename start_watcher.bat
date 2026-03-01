@echo off
REM Start the File System Watcher (Windows)

echo Starting AI Employee File System Watcher...
echo Monitoring: AI_Employee_Vault\Inbox\
echo Press Ctrl+C to stop
echo.

cd AI_Employee_Vault\watchers
uv run python filesystem_watcher.py
