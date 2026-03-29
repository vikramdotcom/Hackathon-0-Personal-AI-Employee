# MCP Server Setup Guide - Silver Tier

This guide walks you through setting up the MCP (Model Context Protocol) servers required for Silver Tier functionality.

## Overview

Silver Tier requires these MCP servers:
1. **Gmail MCP Server** - Email monitoring and sending
2. **Google Calendar MCP Server** - Calendar and scheduling
3. **Playwright MCP Server** - Browser automation (already available)

## Prerequisites

- Node.js 18+ installed
- Google Cloud Project with APIs enabled
- OAuth2 credentials from Google Cloud Console
- Claude Code CLI installed

## Step 1: Create Google Cloud Project

### 1.1 Go to Google Cloud Console

Visit: https://console.cloud.google.com/

### 1.2 Create New Project

1. Click "Select a project" → "New Project"
2. Name: "AI Employee Silver Tier"
3. Click "Create"

### 1.3 Enable Required APIs

Navigate to "APIs & Services" → "Library" and enable:

- **Gmail API**
- **Google Calendar API**
- **Google People API** (for contacts)

## Step 2: Create OAuth2 Credentials

### 2.1 Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (unless you have Google Workspace)
3. Fill in:
   - App name: "AI Employee"
   - User support email: [your email]
   - Developer contact: [your email]
4. Click "Save and Continue"
5. Add scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/calendar.events`
6. Add test users (your email address)
7. Click "Save and Continue"

### 2.2 Create OAuth2 Client ID

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "AI Employee Desktop"
5. Click "Create"
6. **Download JSON** - Save as `credentials.json`

## Step 3: Install MCP Servers

### 3.1 Install Gmail MCP Server

```bash
# Install globally
npm install -g @modelcontextprotocol/server-gmail

# Or use npx (no installation needed)
npx @modelcontextprotocol/server-gmail
```

### 3.2 Install Google Calendar MCP Server

```bash
# Install globally
npm install -g @modelcontextprotocol/server-google-calendar

# Or use npx
npx @modelcontextprotocol/server-google-calendar
```

### 3.3 Verify Playwright MCP

Playwright MCP is already available as a Claude Code skill:

```bash
# Check if available
claude --help | grep playwright
```

## Step 4: Configure Claude Code

### 4.1 Locate Settings File

**Windows**: `C:\Users\[username]\.claude\settings.json`
**Mac/Linux**: `~/.claude/settings.json`

Or use local settings in your project:
`.claude/settings.local.json`

### 4.2 Add MCP Server Configuration

Edit the settings file and add:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GOOGLE_CLIENT_ID": "YOUR_CLIENT_ID_HERE",
        "GOOGLE_CLIENT_SECRET": "YOUR_CLIENT_SECRET_HERE",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth2callback"
      }
    },
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": {
        "GOOGLE_CLIENT_ID": "YOUR_CLIENT_ID_HERE",
        "GOOGLE_CLIENT_SECRET": "YOUR_CLIENT_SECRET_HERE",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth2callback"
      }
    }
  }
}
```

### 4.3 Extract Credentials

From your downloaded `credentials.json`:

```json
{
  "installed": {
    "client_id": "123456789-abcdefg.apps.googleusercontent.com",
    "client_secret": "GOCSPX-abc123def456",
    ...
  }
}
```

Copy:
- `client_id` → `GOOGLE_CLIENT_ID`
- `client_secret` → `GOOGLE_CLIENT_SECRET`

## Step 5: Authenticate MCP Servers

### 5.1 First-Time Authentication

When you first use a skill that requires Gmail or Calendar:

```bash
claude /gmail-monitor check
```

You'll see:
1. A browser window opens
2. Google OAuth consent screen appears
3. Sign in with your Google account
4. Grant permissions
5. Browser shows "Authentication successful"
6. Return to Claude Code

### 5.2 Token Storage

After authentication, tokens are stored securely:
- **Windows**: `C:\Users\[username]\.claude\mcp-tokens\`
- **Mac/Linux**: `~/.claude/mcp-tokens/`

These tokens are refreshed automatically.

## Step 6: Test MCP Servers

### 6.1 Test Gmail Access

```bash
# Check for new emails
claude /gmail-monitor check
```

Expected output:
- Connection to Gmail successful
- List of unread emails (if any)
- Tasks created in Needs_Action/

### 6.2 Test Calendar Access

```bash
# List upcoming events
claude /schedule-task list
```

Expected output:
- Connection to Google Calendar successful
- List of upcoming events
- No errors

### 6.3 Test Email Sending

```bash
# Create a draft email
claude /send-email draft
```

Follow prompts to create a test email draft.

## Step 7: Configure Skill Settings

### 7.1 Gmail Monitoring Rules

Edit `AI_Employee_Vault/Config/gmail_rules.json`:

```json
{
  "check_interval": 300,
  "priority_keywords": {
    "high": ["urgent", "asap", "invoice", "payment"],
    "medium": ["inquiry", "question", "request"],
    "low": ["newsletter", "notification"]
  },
  "max_emails_per_check": 20
}
```

### 7.2 Calendar Settings

Edit `AI_Employee_Vault/Config/calendar_settings.json`:

```json
{
  "default_duration": 60,
  "timezone": "America/New_York",
  "working_hours": {
    "start": "09:00",
    "end": "17:00"
  }
}
```

### 7.3 Email Settings

Edit `AI_Employee_Vault/Config/email_settings.json`:

```json
{
  "default_signature": "Best regards,\nYour Name",
  "require_approval": true
}
```

## Troubleshooting

### Issue: "MCP server not found"

**Solution**:
```bash
# Install MCP server globally
npm install -g @modelcontextprotocol/server-gmail
npm install -g @modelcontextprotocol/server-google-calendar

# Or verify npx can access them
npx @modelcontextprotocol/server-gmail --version
```

### Issue: "Authentication failed"

**Solution**:
1. Check credentials in settings.json
2. Verify OAuth consent screen is configured
3. Ensure your email is added as test user
4. Delete old tokens: `rm -rf ~/.claude/mcp-tokens/`
5. Re-authenticate

### Issue: "Permission denied" errors

**Solution**:
1. Go to Google Cloud Console
2. Check OAuth consent screen scopes
3. Ensure all required scopes are added:
   - `gmail.readonly`
   - `gmail.send`
   - `gmail.modify`
   - `calendar`
   - `calendar.events`

### Issue: "Rate limit exceeded"

**Solution**:
1. Reduce check frequency in config files
2. Wait 24 hours for quota reset
3. Request quota increase in Google Cloud Console

### Issue: "Token expired"

**Solution**:
Tokens auto-refresh. If issues persist:
```bash
# Delete tokens and re-authenticate
rm -rf ~/.claude/mcp-tokens/
claude /gmail-monitor check
```

## Security Best Practices

### 1. Protect Credentials

Never commit credentials to git:

```bash
# Add to .gitignore
echo "credentials.json" >> .gitignore
echo ".claude/mcp-tokens/" >> .gitignore
```

### 2. Use Environment Variables

Instead of hardcoding in settings.json:

```json
{
  "mcpServers": {
    "gmail": {
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

Set in your shell:
```bash
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
```

### 3. Limit Scopes

Only request necessary permissions:
- Use `gmail.readonly` if only reading
- Use `calendar.readonly` if only viewing

### 4. Regular Token Rotation

Revoke and regenerate tokens periodically:
1. Go to Google Account → Security → Third-party apps
2. Revoke "AI Employee" access
3. Re-authenticate

## Alternative: Using Service Accounts

For production/business use, consider service accounts:

### 1. Create Service Account

1. Google Cloud Console → "IAM & Admin" → "Service Accounts"
2. Create service account
3. Download JSON key
4. Enable domain-wide delegation (if using Google Workspace)

### 2. Configure MCP Server

```json
{
  "mcpServers": {
    "gmail": {
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_KEY": "/path/to/service-account-key.json",
        "GOOGLE_IMPERSONATE_USER": "your-email@domain.com"
      }
    }
  }
}
```

## Next Steps

After MCP servers are configured:

1. ✅ Test each skill individually
2. ✅ Configure monitoring rules
3. ✅ Run integration tests
4. ✅ Set up automated checking (cron/scheduled tasks)
5. ✅ Monitor logs for issues

## Support Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **Google API Docs**: https://developers.google.com/gmail/api
- **Claude Code Docs**: https://claude.com/claude-code
- **Project Issues**: Check logs in `AI_Employee_Vault/Logs/`

---

**Setup Complete!** 🎉 Your MCP servers are ready for Silver Tier functionality.
