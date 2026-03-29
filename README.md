# Personal AI Employee - Bronze & Silver Tier ✅

**GIAIC Q4 Hackathon 0** - Building Autonomous FTEs in 2026

A local-first autonomous AI Employee built with Claude Code and Obsidian that manages personal and business tasks while maintaining human oversight.

## 🎯 Project Status

**Current Tier**: Silver (Ready) 🚀
**Bronze Tier**: Complete ✅
**Silver Tier**: Skills Created ✅ (MCP Setup Remaining)
**Architecture**: Local-first, Human-in-the-loop, Agent-driven

## ✨ Bronze Tier Features (Complete)

✅ Obsidian vault with Dashboard.md and Company_Handbook.md
✅ File System Watcher monitoring Inbox folder
✅ Claude Code integration reading/writing to vault
✅ Folder structure: /Inbox, /Needs_Action, /Done, /Plans, /Logs
✅ All AI functionality implemented as Agent Skills
✅ Human-in-the-loop approval workflow
✅ Comprehensive logging and audit trail

## 🌟 Silver Tier Features (Ready)

✅ Gmail monitoring and email management
✅ Email sending with approval workflow
✅ Calendar integration and scheduling
✅ WhatsApp message monitoring
✅ LinkedIn automation and networking
✅ Natural language date/time parsing
✅ Draft response generation
✅ Engagement tracking and analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ ([Download](https://www.python.org/downloads/))
- UV Package Manager: `pip install uv`
- Claude Code CLI ([Installation](https://claude.com/product/claude-code))

### Installation
```bash
# 1. Navigate to project
cd Hackathon-0-Personal-AI-Employee

# 2. Install dependencies
cd AI_Employee_Vault/watchers
uv sync
cd ../..

# 3. Verify Claude Code
claude --version
```

### Running the System

**Windows:**
```bash
# Terminal 1: Start watcher
start_watcher.bat

# Terminal 2: Process tasks
claude /ai-employee process
```

**Linux/Mac:**
```bash
# Terminal 1: Start watcher
bash start_watcher.sh

# Terminal 2: Process tasks
claude /ai-employee process
```

## 📁 Project Structure

```
Hackathon-0-Personal-AI-Employee/
├── AI_Employee_Vault/              # Obsidian vault
│   ├── Dashboard.md                # System status
│   ├── Company_Handbook.md         # Rules & guidelines
│   ├── Config/                     # NEW: Configuration files
│   │   ├── gmail_rules.json
│   │   ├── email_settings.json
│   │   ├── calendar_settings.json
│   │   ├── whatsapp_rules.json
│   │   └── linkedin_settings.json
│   ├── Reports/                    # NEW: Analytics reports
│   ├── Inbox/                      # Drop folder (monitored)
│   ├── Needs_Action/              # Tasks to process
│   ├── Done/                      # Completed tasks
│   ├── Plans/                     # Task plans
│   ├── Logs/                      # Activity logs
│   ├── Pending_Approval/          # Awaiting approval
│   ├── Approved/                  # Approved actions
│   ├── Rejected/                  # Rejected actions
│   └── watchers/                  # Python scripts
│       ├── filesystem_watcher.py
│       ├── gmail_watcher.py       # NEW
│       ├── whatsapp_watcher.py    # NEW
│       └── base_watcher.py
├── .claude/skills/                # Claude Code skills
│   ├── ai-employee/               # Bronze Tier
│   ├── gmail-monitor/             # NEW: Silver Tier
│   ├── send-email/                # NEW: Silver Tier
│   ├── schedule-task/             # NEW: Silver Tier
│   ├── whatsapp-monitor/          # NEW: Silver Tier
│   └── linkedin-automation/       # NEW: Silver Tier
├── start_watcher.sh/bat           # Start scripts
├── test_system.sh/bat             # Test scripts
├── verify_silver_tier.sh/bat      # NEW: Verification scripts
├── DEMO.md                        # Bronze Tier demo
├── SILVER_TIER_README.md          # NEW: Silver Tier guide
├── MCP_SETUP_GUIDE.md             # NEW: MCP setup guide
└── README.md                      # This file
```

## 🎮 Usage

### AI Employee Commands
```bash
# Check system status
claude /ai-employee status

# Process all pending tasks
claude /ai-employee process

# Update dashboard
claude /ai-employee update-dashboard
```

### Testing
```bash
# Windows
test_system.bat

# Linux/Mac
bash test_system.sh
```

## 📖 How It Works

1. **File Drop**: Drop files into `AI_Employee_Vault/Inbox/`
2. **Detection**: Watcher detects and creates metadata in `Needs_Action/`
3. **Processing**: Run `/ai-employee process` to handle tasks
4. **Reasoning**: Claude reads handbook, assesses priority, determines actions
5. **Approval**: Sensitive actions require human approval
6. **Execution**: Safe actions executed, everything logged
7. **Completion**: Dashboard updated, tasks moved to `Done/`

## 🔒 Security

- **Local-First**: All data stays on your machine
- **Human-in-the-Loop**: Sensitive actions require approval
- **Audit Trail**: All actions logged with timestamps
- **Sandboxed**: Operations limited to vault directory

## 📚 Documentation

### Bronze Tier
- [DEMO.md](./DEMO.md) - Complete step-by-step demo
- [AI_Employee_Vault/README.md](./AI_Employee_Vault/README.md) - Vault docs

### Silver Tier
- [SILVER_TIER_README.md](./SILVER_TIER_README.md) - Complete Silver Tier guide
- [MCP_SETUP_GUIDE.md](./MCP_SETUP_GUIDE.md) - MCP server setup
- [.claude/skills/gmail-monitor/SKILL.md](./.claude/skills/gmail-monitor/SKILL.md) - Gmail skill
- [.claude/skills/send-email/SKILL.md](./.claude/skills/send-email/SKILL.md) - Email skill
- [.claude/skills/schedule-task/SKILL.md](./.claude/skills/schedule-task/SKILL.md) - Calendar skill
- [.claude/skills/whatsapp-monitor/SKILL.md](./.claude/skills/whatsapp-monitor/SKILL.md) - WhatsApp skill
- [.claude/skills/linkedin-automation/SKILL.md](./.claude/skills/linkedin-automation/SKILL.md) - LinkedIn skill

### General
- [Hackathon Guide](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026-%20MARKDOWN.md)

## 🚀 Silver Tier Quick Start

Silver Tier skills are ready! To activate:

1. **Verify Installation**:
   ```bash
   # Windows
   verify_silver_tier.bat

   # Linux/Mac
   bash verify_silver_tier.sh
   ```

2. **Setup MCP Servers** (Required):
   - Follow [MCP_SETUP_GUIDE.md](./MCP_SETUP_GUIDE.md)
   - Configure Gmail and Google Calendar APIs
   - Authenticate with Google OAuth2

3. **Test Silver Tier Skills**:
   ```bash
   # Gmail monitoring
   claude /gmail-monitor check

   # Email sending
   claude /send-email status

   # Calendar scheduling
   claude /schedule-task list

   # WhatsApp monitoring
   claude /whatsapp-monitor check

   # LinkedIn automation
   claude /linkedin-automation status
   ```

4. **Read Documentation**:
   - [SILVER_TIER_README.md](./SILVER_TIER_README.md) - Complete guide
   - [MCP_SETUP_GUIDE.md](./MCP_SETUP_GUIDE.md) - Setup instructions

## 🚧 Next Steps (Gold Tier)

- [ ] Odoo ERP integration
- [ ] Social media automation (Twitter, Facebook)
- [ ] CEO briefing generation
- [ ] Advanced analytics and reporting
- [ ] Multi-agent coordination

## 🤝 Hackathon Information

- **Organization**: GIAIC (Governor's Initiative for Artificial Intelligence and Computing)
- **Hackathon**: Hackathon 0 - Building Autonomous FTEs
- **Quarter**: Q4
- **Meetings**: Every Wednesday 10:00 PM ([Zoom Link](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1))
- **Submission**: [Form Link](https://forms.gle/JR9T1SJq5rmQyGkGA)

## 🏆 Tech Stack

- **Brain**: Claude Code (Opus 4.6)
- **Memory/GUI**: Obsidian (Local Markdown)
- **Watchers**: Python 3.13 + watchdog
- **Package Manager**: UV
- **Architecture**: Local-first, Agent-driven

## 📄 License

Educational project for GIAIC Q4 Hackathon 0

---

**Bronze Tier Complete!** 🎉 Ready to deploy your first AI Employee.
