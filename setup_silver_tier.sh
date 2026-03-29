#!/bin/bash
# Silver Tier Setup Script
# Sets up Gmail and LinkedIn watchers with all dependencies

echo "=========================================="
echo "Silver Tier Setup - AI Employee"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "AI_Employee_Vault" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

echo "Step 1: Installing Python dependencies..."
echo "------------------------------------------"
cd AI_Employee_Vault/watchers

# Install dependencies using UV
if command -v uv &> /dev/null; then
    echo "Using UV package manager..."
    uv sync
else
    echo "UV not found. Installing with pip..."
    pip install -r requirements.txt
fi

echo ""
echo "Step 2: Installing Playwright browsers..."
echo "------------------------------------------"
if command -v playwright &> /dev/null; then
    playwright install chromium
    echo "Playwright browsers installed!"
else
    echo "Warning: Playwright not found. Run: pip install playwright && playwright install"
fi

cd ../..

echo ""
echo "Step 3: Checking credentials.json..."
echo "------------------------------------------"
if [ -f "credentials.json" ]; then
    echo "✓ credentials.json found"
else
    echo "✗ credentials.json not found"
    echo ""
    echo "Please add your Google OAuth2 credentials:"
    echo "1. Go to Google Cloud Console"
    echo "2. Create OAuth2 credentials"
    echo "3. Download as credentials.json"
    echo "4. Place in project root"
    echo ""
    echo "See MCP_SETUP_GUIDE.md for detailed instructions"
fi

echo ""
echo "Step 4: Creating configuration files..."
echo "------------------------------------------"

# Create Config directory if it doesn't exist
mkdir -p AI_Employee_Vault/Config

# Create gmail_rules.json if it doesn't exist
if [ ! -f "AI_Employee_Vault/Config/gmail_rules.json" ]; then
    cat > AI_Employee_Vault/Config/gmail_rules.json << 'EOF'
{
  "check_interval": 300,
  "priority_keywords": {
    "high": ["urgent", "asap", "invoice", "payment", "client", "deadline"],
    "medium": ["inquiry", "question", "request", "meeting", "schedule"],
    "low": ["newsletter", "notification", "update", "unsubscribe"]
  },
  "skip_senders": ["noreply@", "no-reply@", "notifications@", "donotreply@"],
  "max_emails_per_check": 20,
  "auto_label": "AI_Employee_Processed",
  "create_drafts": true
}
EOF
    echo "✓ Created gmail_rules.json"
else
    echo "✓ gmail_rules.json already exists"
fi

# Create email_settings.json if it doesn't exist
if [ ! -f "AI_Employee_Vault/Config/email_settings.json" ]; then
    cat > AI_Employee_Vault/Config/email_settings.json << 'EOF'
{
  "default_signature": "Best regards,\nYour Name",
  "reply_prefix": "Re: ",
  "max_recipients": 10,
  "require_approval": true,
  "log_all_emails": true,
  "blocked_domains": []
}
EOF
    echo "✓ Created email_settings.json"
else
    echo "✓ email_settings.json already exists"
fi

# Create calendar_settings.json if it doesn't exist
if [ ! -f "AI_Employee_Vault/Config/calendar_settings.json" ]; then
    cat > AI_Employee_Vault/Config/calendar_settings.json << 'EOF'
{
  "default_duration": 60,
  "default_reminder": 15,
  "timezone": "America/New_York",
  "working_hours": {
    "start": "09:00",
    "end": "17:00"
  },
  "auto_decline_conflicts": false,
  "require_approval": true,
  "max_event_duration": 480
}
EOF
    echo "✓ Created calendar_settings.json"
else
    echo "✓ calendar_settings.json already exists"
fi

# Create whatsapp_rules.json if it doesn't exist
if [ ! -f "AI_Employee_Vault/Config/whatsapp_rules.json" ]; then
    cat > AI_Employee_Vault/Config/whatsapp_rules.json << 'EOF'
{
  "check_interval": 300,
  "priority_keywords": {
    "high": ["urgent", "asap", "help", "emergency", "problem"],
    "medium": ["question", "inquiry", "request", "when", "how"],
    "low": ["thanks", "ok", "received", "noted"]
  },
  "auto_mark_read": false,
  "skip_groups": false,
  "important_contacts": [],
  "max_messages_per_check": 50,
  "download_media": true,
  "create_task_for_groups": false
}
EOF
    echo "✓ Created whatsapp_rules.json"
else
    echo "✓ whatsapp_rules.json already exists"
fi

# Create linkedin_settings.json if it doesn't exist
if [ ! -f "AI_Employee_Vault/Config/linkedin_settings.json" ]; then
    cat > AI_Employee_Vault/Config/linkedin_settings.json << 'EOF'
{
  "check_messages_interval": 3600,
  "auto_accept_connections": false,
  "post_approval_required": true,
  "max_connections_per_day": 10,
  "max_messages_per_day": 20,
  "max_posts_per_day": 5,
  "engagement_tracking": true,
  "personalize_connection_requests": true,
  "default_post_time": "09:00",
  "default_visibility": "public",
  "optimal_posting_days": ["Tuesday", "Wednesday", "Thursday"],
  "optimal_posting_times": ["09:00", "12:00", "17:00"],
  "hashtag_limit": 5,
  "connection_message_max_length": 300,
  "require_approval": true,
  "track_analytics": true,
  "respond_to_comments": true,
  "auto_like": false,
  "rate_limit_delay": 30,
  "headless": true,
  "session_file": "linkedin_session.json"
}
EOF
    echo "✓ Created linkedin_settings.json"
else
    echo "✓ linkedin_settings.json already exists"
fi

echo ""
echo "Step 5: Creating necessary directories..."
echo "------------------------------------------"
mkdir -p AI_Employee_Vault/Reports
mkdir -p AI_Employee_Vault/Logs
echo "✓ Directories created"

echo ""
echo "=========================================="
echo "Silver Tier Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Ensure credentials.json is in project root"
echo "2. Test Gmail watcher: cd AI_Employee_Vault/watchers && uv run python gmail_watcher.py"
echo "3. Test LinkedIn watcher: cd AI_Employee_Vault/watchers && uv run python linkedin_watcher.py"
echo "4. Read MCP_SETUP_GUIDE.md for MCP server configuration"
echo "5. Run verification: bash verify_silver_tier.sh"
echo ""
echo "For detailed instructions, see:"
echo "- SILVER_TIER_README.md"
echo "- MCP_SETUP_GUIDE.md"
echo "- SILVER_TIER_QUICK_REFERENCE.md"
echo ""
