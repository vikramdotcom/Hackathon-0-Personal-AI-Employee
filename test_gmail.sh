#!/bin/bash
# Quick test script for Gmail watcher

echo "=========================================="
echo "Testing Gmail Watcher"
echo "=========================================="
echo ""

cd AI_Employee_Vault/watchers

echo "Running Gmail watcher..."
echo "This will:"
echo "1. Open browser for Google OAuth2 (first time only)"
echo "2. Check your Gmail inbox for unread emails"
echo "3. Create task files in Needs_Action/"
echo "4. Save token for future automatic runs"
echo ""
echo "Press Ctrl+C to stop after first check"
echo ""

uv run python gmail_watcher.py
