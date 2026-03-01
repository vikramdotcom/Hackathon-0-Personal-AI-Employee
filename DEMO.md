# Bronze Tier Demo - AI Employee System

This demo walks through the complete Bronze tier functionality.

## Prerequisites Check

Before starting, ensure:
- [ ] Python 3.13+ installed
- [ ] UV package manager installed
- [ ] Claude Code CLI installed
- [ ] All dependencies installed in watchers/ folder

## Demo Steps

### Step 1: Verify Vault Structure

Check that all folders exist:

```bash
ls -la AI_Employee_Vault/
```

Expected folders:
- Inbox/
- Needs_Action/
- Done/
- Plans/
- Logs/
- Pending_Approval/
- Approved/
- Rejected/
- Accounting/
- watchers/

### Step 2: Review Core Files

1. **Dashboard.md** - System status overview
   ```bash
   cat AI_Employee_Vault/Dashboard.md
   ```

2. **Company_Handbook.md** - Rules and guidelines
   ```bash
   cat AI_Employee_Vault/Company_Handbook.md
   ```

### Step 3: Start the File System Watcher

Open Terminal 1:

```bash
# Windows
start_watcher.bat

# Linux/Mac
bash start_watcher.sh
```

You should see:
```
Starting FileSystemWatcher
Monitoring drop folder: C:\...\AI_Employee_Vault\Inbox
File system watcher is now active
Drop files into the Inbox folder to trigger processing
```

### Step 4: Test File Drop Detection

Open Terminal 2 and create a test file:

```bash
# Create a test document
echo "This is a test invoice for Client A - Amount: $500" > AI_Employee_Vault/Inbox/invoice_client_a.txt
```

Watch Terminal 1 - you should see:
```
INFO - Found 1 new items to process
INFO - Processed new file: invoice_client_a.txt
INFO - Created action file: FILE_invoice_client_a.txt.md
```

### Step 5: Verify File Processing

Check that metadata was created:

```bash
ls -la AI_Employee_Vault/Needs_Action/
```

You should see:
- FILE_invoice_client_a.txt (the copied file)
- FILE_invoice_client_a.txt.md (the metadata)

View the metadata:

```bash
cat AI_Employee_Vault/Needs_Action/FILE_invoice_client_a.txt.md
```

Expected content:
```markdown
---
type: file_drop
original_name: invoice_client_a.txt
size: X.XX KB
created: 2026-03-01T...
status: pending
priority: medium
---

## New File Dropped for Processing
...
```

### Step 6: Use AI Employee Skill

Check system status:

```bash
claude /ai-employee status
```

Process pending tasks:

```bash
claude /ai-employee process
```

The AI Employee will:
1. Read Company_Handbook.md
2. Scan Needs_Action/ folder
3. Process each task according to rules
4. Update Dashboard.md
5. Move completed tasks to Done/
6. Log all actions

### Step 7: Verify Task Completion

Check Dashboard:

```bash
cat AI_Employee_Vault/Dashboard.md
```

Should show updated:
- Recent Activity
- Tasks Completed Today
- Current status

Check Done folder:

```bash
ls -la AI_Employee_Vault/Done/
```

Should contain processed task files.

Check Logs:

```bash
ls -la AI_Employee_Vault/Logs/
```

Should contain log files with timestamps.

### Step 8: Test Approval Workflow

Create a sensitive task that requires approval:

```bash
echo "URGENT: Please send payment of $5000 to Vendor XYZ" > AI_Employee_Vault/Inbox/payment_request.txt
```

Run AI Employee:

```bash
claude /ai-employee process
```

The AI should:
1. Detect this is a financial action
2. Create approval request in Pending_Approval/
3. NOT execute the payment
4. Update Dashboard with "Awaiting Approval"

Verify:

```bash
ls -la AI_Employee_Vault/Pending_Approval/
```

Should contain an approval request file.

### Step 9: Test Multiple File Types

Drop various file types:

```bash
echo "name,email,phone" > AI_Employee_Vault/Inbox/contacts.csv
echo '{"config": "value"}' > AI_Employee_Vault/Inbox/settings.json
echo "# Meeting Notes" > AI_Employee_Vault/Inbox/notes.md
```

Watch the watcher process all files automatically.

### Step 10: Update Dashboard

Manually update dashboard:

```bash
claude /ai-employee update-dashboard
```

Verify Dashboard.md reflects current system state.

## Success Criteria

Bronze tier is complete if:

✅ Vault structure exists with all required folders
✅ Dashboard.md and Company_Handbook.md are present and properly formatted
✅ File System Watcher detects new files in Inbox/
✅ Watcher creates metadata files in Needs_Action/
✅ Watcher logs activity to Logs/ folder
✅ AI Employee skill is accessible via `/ai-employee` command
✅ AI Employee can read from vault (Dashboard, Handbook, tasks)
✅ AI Employee can write to vault (logs, updates)
✅ AI Employee processes tasks according to handbook rules
✅ AI Employee requests approval for sensitive actions
✅ All functionality implemented as Agent Skills

## Troubleshooting

### Watcher not starting
- Check Python installation: `python --version`
- Check UV installation: `uv --version`
- Install dependencies: `cd AI_Employee_Vault/watchers && uv sync`

### Files not being detected
- Ensure watcher is running
- Check Inbox folder path is correct
- Try creating file manually in Inbox/

### AI Employee skill not found
- Verify `.claude/skills/ai-employee/` exists
- Check SKILL.md and prompt.md are present
- Restart Claude Code session

### Claude Code can't access vault
- Run Claude from project root directory
- Use absolute paths if needed
- Check file permissions

## Next Steps

After completing Bronze tier:

1. **Silver Tier**: Add Gmail watcher, WhatsApp watcher, MCP servers
2. **Gold Tier**: Add Odoo integration, social media automation, CEO briefings
3. **Platinum Tier**: Deploy to cloud, multi-agent coordination

## Demo Complete!

You now have a working Bronze tier AI Employee system that:
- Monitors file drops automatically
- Processes tasks autonomously
- Follows defined rules and guidelines
- Maintains human oversight for sensitive actions
- Logs all activities for audit

Congratulations on completing Bronze tier! 🎉
