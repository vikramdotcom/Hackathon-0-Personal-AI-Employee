#!/usr/bin/env python3
"""Test script for LinkedIn Watcher - Silver Tier"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_watcher import LinkedInWatcher

def test_linkedin_watcher():
    """Test LinkedIn watcher functionality."""
    print("=" * 60)
    print("LinkedIn Watcher Test - Silver Tier")
    print("=" * 60)
    print()

    # Get vault path
    vault_path = Path(__file__).parent.parent

    print(f"Vault path: {vault_path}")
    print()

    # Create watcher instance
    print("Creating LinkedIn watcher instance...")
    watcher = LinkedInWatcher(str(vault_path))
    print("✓ Watcher created successfully")
    print()

    # Test configuration loading
    print("Testing configuration...")
    print(f"Check interval: {watcher.config['check_messages_interval']} seconds")
    print(f"Max messages per check: {watcher.config['max_messages_per_check']}")
    print(f"Headless mode: {watcher.config['headless']}")
    print("✓ Configuration loaded successfully")
    print()

    # Test browser initialization and LinkedIn check
    print("Testing LinkedIn message checking...")
    print("(This will open a browser window)")
    print("(First time will require manual LinkedIn login)")
    print()

    try:
        messages = watcher.check_for_updates()
        print(f"✓ Found {len(messages)} new messages")
        print()

        if messages:
            print("Creating task files...")
            for msg in messages:
                task_file = watcher.create_action_file(msg)
                print(f"✓ Created: {task_file.name}")
            print()

        print("=" * 60)
        print("LinkedIn Watcher Test PASSED!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Check AI_Employee_Vault/Needs_Action/ for created tasks")
        print("2. Run: claude /ai-employee process")
        print("3. Review tasks and approve/reject as needed")
        print()

        return True

    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Ensure Playwright is installed: pip install playwright")
        print("2. Install browsers: playwright install chromium")
        print("3. Login to LinkedIn manually when browser opens")
        print("4. Session will be saved for future automated checks")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_linkedin_watcher()
    sys.exit(0 if success else 1)
