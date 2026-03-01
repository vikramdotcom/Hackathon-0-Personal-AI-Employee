# AI Employee - Bronze Tier Implementation

A local-first autonomous AI Employee built with Claude Code and Obsidian for personal and business automation.

## 🎯 Bronze Tier Features

✅ Obsidian vault with Dashboard.md and Company_Handbook.md
✅ Working File System Watcher for monitoring Inbox folder
✅ Claude Code reading from and writing to the vault
✅ Basic folder structure: /Inbox, /Needs_Action, /Done, /Plans, /Logs, /Pending_Approval
✅ AI functionality implemented as Agent Skill

## 📁 Project Structure

```
Hackathon-0-Personal-AI-Employee/
├── AI_Employee_Vault/           # Obsidian vault
│   ├── Dashboard.md             # System status overview
│   ├── Company_Handbook.md      # Rules and guidelines
│   ├── Inbox/                   # Drop folder (monitored)
│   ├── Needs_Action/           # Tasks to process
│   ├── Done/                   # Completed tasks
│   ├── Plans/                  # Task plans
│   ├── Logs/                   # Activity logs
│   ├── Pending_Approval/       # Awaiting approval
│   ├── Approved/               # Approved actions
│   ├── Rejected/               # Rejected actions
│   └── watchers/               # Python watcher scripts
│       ├── base_watcher.py
│       ├── filesystem_watcher.py
│       └── pyproject.toml
└── .claude/
    └── skills/
        └── ai-employee/        # Claude Code skill
            ├── SKILL.md
            └── prompt.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Claude Code CLI installed
- Obsidian (optional, for GUI viewing)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd Hackathon-0-Personal-AI-Employee
   ```

2. **Install Python dependencies**
   ```bash
   cd AI_Employee_Vault/watchers
   uv sync
   ```

3. **Verify Claude Code installation**
   ```bash
   claude --version
   ```

### Running the System

#### Step 1: Start the File System Watcher

Open a terminal and run:

```bash
cd AI_Employee_Vault/watchers
uv run python filesystem_watcher.py
```

The watcher will monitor the `Inbox/` folder for new files.

#### Step 2: Use the AI Employee Skill

Open another terminal and navigate to the project root:

```bash
cd Hackathon-0-Personal-AI-Employee
```

Process tasks using the AI Employee skill:

```bash
# Check system status
claude /ai-employee status

# Process all pending tasks
claude /ai-employee process

# Update dashboard
claude /ai-employee update-dashboard
```

## 📝 How It Works

### 1. File Drop Workflow

1. Drop a file into `AI_Employee_Vault/Inbox/`
2. File System Watcher detects the new file
3. Watcher copies file to `Needs_Action/` and creates metadata file
4. Watcher logs the action

### 2. Task Processing Workflow

1. Run `/ai-employee process` command
2. Claude Code reads `Company_Handbook.md` for rules
3. Scans `Needs_Action/` folder for pending tasks
4. For each task:
   - Assesses priority (high/medium/low)
   - Checks if approval is needed
   - Creates plan if complex
   - Executes safe actions or requests approval
   - Logs all actions
   - Updates Dashboard
   - Moves to Done when complete

### 3. Human-in-the-Loop

For sensitive actions:
- AI creates approval request in `Pending_Approval/`
- Human reviews and moves to `Approved/` or `Rejected/`
- AI executes only after approval

## 🧪 Testing the System

### Test 1: File Drop Detection

1. Start the watcher
2. Create a test file:
   ```bash
   echo "Test document" > AI_Employee_Vault/Inbox/test.txt
   ```
3. Check that a metadata file appears in `Needs_Action/`
4. Verify the watcher logs the action

### Test 2: Task Processing

1. Run the AI Employee:
   ```bash
   claude /ai-employee process
   ```
2. Verify that:
   - Task is processed
   - Dashboard is updated
   - Task moves to Done/
   - Action is logged in Logs/

### Test 3: Dashboard Update

1. Run:
   ```bash
   claude /ai-employee status
   ```
2. Verify current system status is displayed

## 📊 Monitoring

### View Dashboard
Open `AI_Employee_Vault/Dashboard.md` in Obsidian or any text editor to see:
- System status
- Pending tasks
- Recent activity
- Alerts

### View Logs
Check `AI_Employee_Vault/Logs/` for:
- Watcher activity logs
- AI Employee action logs
- Error logs

## 🔒 Security

- All operations are local-first
- No external API calls (except Claude Code)
- Sensitive actions require human approval
- All actions are logged for audit
- Credentials never stored in vault

## 📚 Configuration

### Customizing Rules

Edit `AI_Employee_Vault/Company_Handbook.md` to:
- Adjust priority levels
- Modify approval thresholds
- Add custom workflows
- Define communication guidelines

### Watcher Settings

Edit `filesystem_watcher.py` to:
- Change check interval
- Modify monitored folder
- Adjust file filters

## 🎓 Bronze Tier Completion Checklist

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (File System monitoring)
- [x] Claude Code successfully reading from and writing to vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] All AI functionality implemented as Agent Skills

## 🚧 Next Steps (Silver Tier)

To upgrade to Silver tier, add:
- Gmail watcher for email monitoring
- WhatsApp watcher for message monitoring
- MCP server for sending emails
- Automated scheduling via cron/Task Scheduler
- Enhanced approval workflows

## 📖 Resources

- [Hackathon Documentation](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026-%20MARKDOWN.md)
- [Claude Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Agent Skills Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## 🐛 Troubleshooting

### Watcher not detecting files
- Ensure watcher is running
- Check file permissions
- Verify Inbox folder path

### Claude Code can't find vault
- Run Claude from project root directory
- Verify vault path in commands

### Skill not found
- Ensure `.claude/skills/ai-employee/` exists
- Check SKILL.md and prompt.md are present
- Restart Claude Code session

## 📄 License

This is a hackathon project for educational purposes.

## 👥 Contributing

This is part of the GIAIC Q4 Hackathon 0. Join the Wednesday research meetings to collaborate!

---

**Built with**: Claude Code, Python, Obsidian, UV
**Tier**: Bronze ✅
**Status**: Complete and functional
