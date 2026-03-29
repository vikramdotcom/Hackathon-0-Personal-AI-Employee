# Silver Tier Quick Reference

Quick command reference for all Silver Tier skills.

## 📧 Gmail Monitoring

### Check for New Emails
```bash
claude /gmail-monitor check
```
- Scans Gmail inbox for unread emails
- Creates tasks in Needs_Action/ for important emails
- Assesses priority based on keywords
- Generates draft replies when appropriate

### View Status
```bash
claude /gmail-monitor status
```
- Shows recent email activity
- Lists pending email tasks
- Displays monitoring configuration

### Configure Rules
```bash
claude /gmail-monitor configure
```
- Set up priority keywords
- Configure skip senders
- Adjust check frequency

**Config File**: `AI_Employee_Vault/Config/gmail_rules.json`

---

## 📤 Email Sending

### Send Approved Emails
```bash
claude /send-email send
```
- Sends all emails in Approved/ folder
- Validates recipients and content
- Logs all sent emails
- Moves to Done/ after sending

### Create Email Draft
```bash
claude /send-email draft
```
- Interactive draft creation
- Creates approval request in Pending_Approval/
- Requires human approval before sending

### Check Status
```bash
claude /send-email status
```
- Shows pending drafts
- Lists approved emails ready to send
- Displays recently sent emails

**Config File**: `AI_Employee_Vault/Config/email_settings.json`

---

## 📅 Calendar & Scheduling

### Create Event
```bash
claude /schedule-task create
```
- Interactive event creation
- Parses natural language dates/times
- Creates approval request
- Adds to Google Calendar after approval

### List Upcoming Events
```bash
claude /schedule-task list
```
- Shows next 7 days of events
- Displays pending approvals
- Identifies scheduling conflicts

### Parse Scheduling Request
```bash
claude /schedule-task parse
```
- Extracts scheduling info from text
- Parses natural language
- Creates event draft for approval

**Config File**: `AI_Employee_Vault/Config/calendar_settings.json`

**Natural Language Examples**:
- "Meeting with John tomorrow at 2pm"
- "Call client next Monday morning"
- "Deadline for report is March 15"
- "Weekly standup every Monday at 9am"

---

## 💬 WhatsApp Monitoring

### Check Messages
```bash
claude /whatsapp-monitor check
```
- Scans WhatsApp for new messages
- Creates tasks for important messages
- Downloads media attachments
- Generates draft replies

### View Status
```bash
claude /whatsapp-monitor status
```
- Shows recent message activity
- Lists pending responses
- Displays monitoring configuration

### Configure Rules
```bash
claude /whatsapp-monitor configure
```
- Set up priority keywords
- Configure important contacts
- Adjust media download settings

**Config File**: `AI_Employee_Vault/Config/whatsapp_rules.json`

---

## 💼 LinkedIn Automation

### Check Messages
```bash
claude /linkedin-automation check-messages
```
- Scans LinkedIn inbox
- Creates tasks for messages
- Generates professional replies

### Schedule Post
```bash
claude /linkedin-automation schedule-post
```
- Create post for approval
- Schedule publication time
- Track engagement after posting

### Send Connection Request
```bash
claude /linkedin-automation send-connection
```
- Create personalized connection request
- Requires approval before sending
- Tracks acceptance rate

### Monitor Engagement
```bash
claude /linkedin-automation monitor-engagement
```
- Track post performance
- Identify comments needing responses
- Generate engagement report

### View Status
```bash
claude /linkedin-automation status
```
- Shows pending messages
- Lists scheduled posts
- Displays recent activity

**Config File**: `AI_Employee_Vault/Config/linkedin_settings.json`

---

## 🔄 Integrated Workflows

### Email-to-Calendar Workflow
```bash
# 1. Check emails
claude /gmail-monitor check

# 2. Process tasks (AI Employee finds meeting request)
claude /ai-employee process

# 3. Review scheduling approval in Pending_Approval/
# 4. Move to Approved/

# 5. Create calendar event
claude /schedule-task create
```

### Email Response Workflow
```bash
# 1. Check emails
claude /gmail-monitor check

# 2. Process tasks (AI Employee drafts reply)
claude /ai-employee process

# 3. Review draft in Pending_Approval/
# 4. Move to Approved/

# 5. Send approved emails
claude /send-email send
```

### LinkedIn Engagement Workflow
```bash
# 1. Check messages
claude /linkedin-automation check-messages

# 2. Process tasks
claude /ai-employee process

# 3. Review responses in Pending_Approval/
# 4. Move to Approved/

# 5. Send responses (via browser automation)
```

---

## 📁 Folder Workflow

### Approval Process

1. **Pending_Approval/** - Items awaiting your decision
   - Review the file
   - Edit if needed
   - Move to Approved/ or Rejected/

2. **Approved/** - Ready to execute
   - Run appropriate skill to execute
   - Items automatically move to Done/

3. **Rejected/** - Declined items
   - Archived for reference
   - Logged for audit trail

### Task Processing

```bash
# Standard workflow
claude /ai-employee process
```

This processes all tasks in Needs_Action/:
- Reads Company_Handbook.md for rules
- Assesses priority
- Creates plans for complex tasks
- Generates drafts for responses
- Requests approval for sensitive actions
- Executes safe actions
- Logs everything
- Updates Dashboard

---

## 🔧 Configuration Files

All config files are in `AI_Employee_Vault/Config/`:

- **gmail_rules.json** - Email monitoring rules
- **email_settings.json** - Email sending preferences
- **calendar_settings.json** - Calendar and scheduling
- **whatsapp_rules.json** - WhatsApp monitoring
- **linkedin_settings.json** - LinkedIn automation

Edit these files to customize behavior.

---

## 📊 Monitoring & Logs

### Dashboard
```bash
# View current status
cat AI_Employee_Vault/Dashboard.md

# Update dashboard
claude /ai-employee update-dashboard
```

### Logs
All activity logged in `AI_Employee_Vault/Logs/`:
- `YYYY-MM-DD_task_log.json` - Task processing
- `YYYY-MM-DD_email_log.json` - Email activity
- `YYYY-MM-DD_whatsapp_log.json` - WhatsApp activity
- `YYYY-MM-DD_linkedin_log.json` - LinkedIn activity
- `YYYY-MM-DD_schedule_log.json` - Calendar events

### Reports
Weekly reports in `AI_Employee_Vault/Reports/`:
- LinkedIn engagement reports
- Email response metrics
- Calendar utilization

---

## 🚨 Troubleshooting

### Skill Not Found
```bash
# Verify skills are installed
ls .claude/skills/

# Restart Claude Code session
```

### MCP Server Not Working
```bash
# Check MCP server configuration
cat .claude/settings.local.json

# Test MCP server
npx @modelcontextprotocol/server-gmail --version
```

### Authentication Issues
```bash
# Delete tokens and re-authenticate
rm -rf ~/.claude/mcp-tokens/
claude /gmail-monitor check
```

### Permission Denied
- Check OAuth scopes in Google Cloud Console
- Ensure APIs are enabled
- Verify test users are added

---

## 💡 Tips & Best Practices

### Email Management
- Check emails 2-3 times per day
- Process high-priority emails immediately
- Review drafts before approving
- Keep signature updated in config

### Calendar
- Set working hours in config
- Enable conflict detection
- Use natural language for quick scheduling
- Review recurring events monthly

### WhatsApp
- Configure important contacts
- Enable media download for receipts/documents
- Set up auto-responses for common queries
- Review group message settings

### LinkedIn
- Personalize all connection requests
- Schedule posts during optimal times (9am, 12pm, 5pm)
- Respond to comments within 24 hours
- Track engagement metrics weekly

### Security
- Review approval requests carefully
- Never approve suspicious emails
- Check recipient addresses before sending
- Monitor logs regularly for unusual activity

---

## 🎯 Daily Routine

### Morning (9:00 AM)
```bash
# 1. Check overnight activity
claude /ai-employee status

# 2. Check emails
claude /gmail-monitor check

# 3. Check messages
claude /whatsapp-monitor check
claude /linkedin-automation check-messages

# 4. Process all tasks
claude /ai-employee process

# 5. Review approvals in Pending_Approval/
# 6. Move approved items to Approved/

# 7. Execute approved actions
claude /send-email send
```

### Midday (12:00 PM)
```bash
# Quick check
claude /ai-employee status
claude /gmail-monitor check
```

### Evening (5:00 PM)
```bash
# Final check
claude /ai-employee status
claude /gmail-monitor check

# Update dashboard
claude /ai-employee update-dashboard

# Review logs
cat AI_Employee_Vault/Logs/$(date +%Y-%m-%d)_task_log.json
```

---

## 📚 Additional Resources

- [SILVER_TIER_README.md](./SILVER_TIER_README.md) - Complete guide
- [MCP_SETUP_GUIDE.md](./MCP_SETUP_GUIDE.md) - Setup instructions
- [Company_Handbook.md](./AI_Employee_Vault/Company_Handbook.md) - Rules
- Individual skill documentation in `.claude/skills/*/SKILL.md`

---

**Quick Reference Complete!** Keep this handy for daily operations.
