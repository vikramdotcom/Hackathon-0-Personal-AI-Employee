# Personal AI Employee - Bronze Tier ✅

**GIAIC Q4 Hackathon 0** - Building Autonomous FTEs in 2026

A local-first autonomous AI Employee built with Claude Code and Obsidian that manages personal and business tasks while maintaining human oversight.

## 🎯 Project Status

**Tier**: Bronze (Complete) ✅
**Estimated Time**: 8-12 hours
**Architecture**: Local-first, Human-in-the-loop, Agent-driven

## ✨ Bronze Tier Features (Complete)

✅ Obsidian vault with Dashboard.md and Company_Handbook.md
✅ File System Watcher monitoring Inbox folder
✅ Claude Code integration reading/writing to vault
✅ Folder structure: /Inbox, /Needs_Action, /Done, /Plans, /Logs
✅ All AI functionality implemented as Agent Skills
✅ Human-in-the-loop approval workflow
✅ Comprehensive logging and audit trail

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
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Dashboard.md            # System status
│   ├── Company_Handbook.md     # Rules & guidelines
│   ├── Inbox/                  # Drop folder (monitored)
│   ├── Needs_Action/          # Tasks to process
│   ├── Done/                  # Completed tasks
│   ├── Plans/                 # Task plans
│   ├── Logs/                  # Activity logs
│   ├── Pending_Approval/      # Awaiting approval
│   └── watchers/              # Python scripts
├── .claude/skills/ai-employee/ # Claude Code skill
├── start_watcher.sh/bat       # Start scripts
├── test_system.sh/bat         # Test scripts
└── DEMO.md                    # Complete walkthrough
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

- [DEMO.md](./DEMO.md) - Complete step-by-step demo
- [AI_Employee_Vault/README.md](./AI_Employee_Vault/README.md) - Vault docs
- [Hackathon Guide](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026-%20MARKDOWN.md)

## 🚧 Next Steps (Silver Tier)

- [ ] Gmail watcher for email monitoring
- [ ] WhatsApp watcher for messages
- [ ] LinkedIn automation
- [ ] MCP server for email sending
- [ ] Automated scheduling

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
