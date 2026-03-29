# Silver Tier Quick Start Guide

Get your Gmail and LinkedIn watchers running in 5 minutes!

## Prerequisites Check

✅ Bronze Tier working
✅ credentials.json in project root
✅ Python 3.12+ installed
✅ UV package manager installed

## Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to watchers directory
cd AI_Employee_Vault/watchers

# Install all Silver Tier dependencies
uv sync

# Install Playwright browsers
playwright install chromium
```

**Windows:**
```bash
cd AI_Employee_Vault\watchers
uv sync
playwright install chromium
```

## Step 2: Run Setup Script (1 minute)

```bash
# Linux/Mac
bash setup_silver_tier.sh

# Windows
setup_silver_tier.bat
```

This creates all configuration files automatically.

## Step 3: Test Gmail Watcher (2 minutes)

```bash
cd AI_Employee_Vault/watchers
uv run python gmail_watcher.py
```

**What happens:**
1. Browser opens for Google OAuth2 login
2. Sign in with your Google account
3. Grant Gmail permissions
4. Watcher checks for unread emails
5. Creates tasks in Needs_Action/

**First run only:** You'll need to authenticate. After that, it's automatic.

## Step 4: Test LinkedIn Watcher (Optional)

```bash
cd AI_Employee_Vault/watchers
uv run python linkedin_watcher.py
```

**What happens:**
1. Browser opens (visible, not headless)
2. Navigate to LinkedIn and login manually
3. Session is saved for future automated checks
4. Watcher checks for new messages
5. Creates tasks in Needs_Action/

## Step 5: Process Tasks

```bash
# Go back to project root
cd ../..

# Process all tasks with AI Employee
claude /ai-employee process
```

The AI Employee will:
- Read email tasks
- Assess priority
- Generate draft replies
- Create approval requests

## Step 6: Review and Approve

```bash
# Check what needs approval
ls AI_Employee_Vault/Pending_Approval/

# Review files, then move to Approved/
mv AI_Employee_Vault/Pending_Approval/DRAFT_* AI_Employee_Vault/Approved/

# Send approved emails (when email sending is configured)
claude /send-email send
```

## Daily Workflow

### Morning Routine (5 minutes)
```bash
# 1. Check Gmail
cd AI_Employee_Vault/watchers
uv run python gmail_watcher.py

# 2. Process tasks
cd ../..
claude /ai-employee process

# 3. Review approvals
ls AI_Employee_Vault/Pending_Approval/

# 4. Approve and execute
# (move files to Approved/ folder)
```

### Automated Checking (Optional)

Run watchers on a schedule:

**Linux/Mac (cron):**
```bash
# Edit crontab
crontab -e

# Add these lines (check every 5 minutes)
*/5 * * * * cd /path/to/project/AI_Employee_Vault/watchers && uv run python gmail_watcher.py
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Every 5 minutes
4. Action: Start a program
5. Program: `uv`
6. Arguments: `run python gmail_watcher.py`
7. Start in: `C:\path\to\project\AI_Employee_Vault\watchers`

## Troubleshooting

### Gmail Watcher Issues

**"Credentials file not found"**
- Ensure credentials.json is in project root
- Check file name is exactly `credentials.json`

**"Authentication failed"**
- Delete `AI_Employee_Vault/watchers/token.pickle`
- Run watcher again to re-authenticate

**"Gmail API not enabled"**
- Go to Google Cloud Console
- Enable Gmail API for your project
- Wait a few minutes, try again

### LinkedIn Watcher Issues

**"Playwright not installed"**
```bash
pip install playwright
playwright install chromium
```

**"Login timeout"**
- Increase timeout in linkedin_watcher.py
- Login manually when browser opens
- Session will be saved for next time

**"Browser crashes"**
- Try non-headless mode: Set `"headless": false` in linkedin_settings.json
- Update Playwright: `pip install --upgrade playwright`

## Configuration

Edit these files to customize behavior:

- `AI_Employee_Vault/Config/gmail_rules.json` - Email priority keywords
- `AI_Employee_Vault/Config/linkedin_settings.json` - LinkedIn settings

## Next Steps

1. ✅ Gmail watcher working
2. ✅ LinkedIn watcher working (optional)
3. ⏭️ Set up MCP servers for Claude Code skills
4. ⏭️ Configure email sending
5. ⏭️ Set up calendar integration

See [SILVER_TIER_README.md](../SILVER_TIER_README.md) for complete documentation.

## Quick Commands Reference

```bash
# Test Gmail watcher
cd AI_Employee_Vault/watchers && uv run python gmail_watcher.py

# Test LinkedIn watcher
cd AI_Employee_Vault/watchers && uv run python linkedin_watcher.py

# Run comprehensive tests
cd AI_Employee_Vault/watchers && uv run python test_silver_tier.py

# Process tasks
claude /ai-employee process

# Check system status
claude /ai-employee status
```

## Success Indicators

✅ Gmail watcher runs without errors
✅ Email tasks appear in Needs_Action/
✅ LinkedIn watcher can login and check messages
✅ AI Employee processes tasks successfully
✅ Draft replies generated in Pending_Approval/

---

**You're ready!** Your AI Employee can now monitor Gmail and LinkedIn automatically.
