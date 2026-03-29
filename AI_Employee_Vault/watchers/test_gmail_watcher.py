#!/usr/bin/env python3
"""Test script for Gmail Watcher - Silver Tier"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gmail_watcher import GmailWatcher

def test_gmail_watcher():
    """Test Gmail watcher functionality."""
    print("=" * 60)
    print("Gmail Watcher Test - Silver Tier")
    print("=" * 60)
    print()

    # Get vault path
    vault_path = Path(__file__).parent.parent

    print(f"Vault path: {vault_path}")
    print()

    # Create watcher instance
    print("Creating Gmail watcher instance...")
    watcher = GmailWatcher(str(vault_path))
    print("✓ Watcher created successfully")
    print()

    # Test configuration loading
    print("Testing configuration...")
    print(f"Check interval: {watcher.config['check_interval']} seconds")
    print(f"Max emails per check: {watcher.config['max_emails_per_check']}")
    print(f"High priority keywords: {', '.join(watcher.config['priority_keywords']['high'][:3])}...")
    print("✓ Configuration loaded successfully")
    print()

    # Test authentication
    print("Testing Gmail authentication...")
    print("(This will open a browser window for OAuth2 if first time)")
    print()

    try:
        service = watcher._connect_gmail()
        if service:
            print("✓ Gmail authentication successful!")
            print()

            # Test fetching emails
            print("Testing email fetching...")
            emails = watcher.check_for_updates()
            print(f"✓ Found {len(emails)} new emails")
            print()

            if emails:
                print("Creating task files...")
                for email in emails:
                    task_file = watcher.create_action_file(email)
                    print(f"✓ Created: {task_file.name}")
                print()

            print("=" * 60)
            print("Gmail Watcher Test PASSED!")
            print("=" * 60)
            print()
            print("Next steps:")
            print("1. Check AI_Employee_Vault/Needs_Action/ for created tasks")
            print("2. Run: claude /ai-employee process")
            print("3. Review tasks and approve/reject as needed")
            print()

        else:
            print("✗ Gmail authentication failed")
            print()
            print("Troubleshooting:")
            print("1. Ensure credentials.json is in project root")
            print("2. Check Gmail API is enabled in Google Cloud Console")
            print("3. Verify OAuth2 credentials are correct")
            print()
            return False

    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == '__main__':
    success = test_gmail_watcher()
    sys.exit(0 if success else 1)
