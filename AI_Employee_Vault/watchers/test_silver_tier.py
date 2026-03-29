#!/usr/bin/env python3
"""Comprehensive test script for Silver Tier - Tests all watchers and configurations"""
import sys
import json
from pathlib import Path

# Fix Windows encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

def print_success(text):
    """Print success message."""
    print(f"[OK] {text}")

def print_error(text):
    """Print error message."""
    print(f"[FAIL] {text}")

def print_warning(text):
    """Print warning message."""
    print(f"[WARN] {text}")

def test_directory_structure():
    """Test that all required directories exist."""
    print_header("Testing Directory Structure")

    vault_path = Path(__file__).parent.parent
    required_dirs = [
        'Config',
        'Reports',
        'Logs',
        'Needs_Action',
        'Pending_Approval',
        'Approved',
        'Rejected',
        'Done',
        'Plans',
        'Inbox'
    ]

    all_exist = True
    for dir_name in required_dirs:
        dir_path = vault_path / dir_name
        if dir_path.exists():
            print_success(f"{dir_name}/ exists")
        else:
            print_error(f"{dir_name}/ missing")
            all_exist = False

    return all_exist

def test_configuration_files():
    """Test that all configuration files exist and are valid JSON."""
    print_header("Testing Configuration Files")

    vault_path = Path(__file__).parent.parent
    config_files = [
        'gmail_rules.json',
        'email_settings.json',
        'calendar_settings.json',
        'whatsapp_rules.json',
        'linkedin_settings.json'
    ]

    all_valid = True
    for config_file in config_files:
        config_path = vault_path / 'Config' / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    json.load(f)
                print_success(f"{config_file} exists and is valid JSON")
            except json.JSONDecodeError as e:
                print_error(f"{config_file} has invalid JSON: {e}")
                all_valid = False
        else:
            print_error(f"{config_file} missing")
            all_valid = False

    return all_valid

def test_python_dependencies():
    """Test that required Python packages are installed."""
    print_header("Testing Python Dependencies")

    dependencies = {
        'watchdog': 'File system monitoring',
        'google.auth': 'Google authentication',
        'google_auth_oauthlib': 'Google OAuth2',
        'googleapiclient': 'Google API client',
        'playwright': 'Browser automation'
    }

    all_installed = True
    for package, description in dependencies.items():
        try:
            __import__(package.replace('.', '_'))
            print_success(f"{package} installed ({description})")
        except ImportError:
            print_error(f"{package} not installed ({description})")
            all_installed = False

    return all_installed

def test_credentials():
    """Test that credentials.json exists."""
    print_header("Testing Credentials")

    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / 'credentials.json'

    if credentials_path.exists():
        try:
            with open(credentials_path, 'r') as f:
                creds = json.load(f)

            if 'installed' in creds:
                print_success("credentials.json exists and has correct structure")

                # Check for required fields
                required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
                has_all_fields = all(field in creds['installed'] for field in required_fields)

                if has_all_fields:
                    print_success("All required OAuth2 fields present")
                    return True
                else:
                    print_error("Missing required OAuth2 fields")
                    return False
            else:
                print_error("credentials.json has incorrect structure")
                return False
        except json.JSONDecodeError:
            print_error("credentials.json has invalid JSON")
            return False
    else:
        print_warning("credentials.json not found (required for Gmail watcher)")
        print("  Place credentials.json in project root")
        print("  See MCP_SETUP_GUIDE.md for instructions")
        return False

def test_watcher_files():
    """Test that all watcher Python files exist."""
    print_header("Testing Watcher Files")

    watchers_path = Path(__file__).parent
    watcher_files = [
        'base_watcher.py',
        'filesystem_watcher.py',
        'gmail_watcher.py',
        'whatsapp_watcher.py',
        'linkedin_watcher.py'
    ]

    all_exist = True
    for watcher_file in watcher_files:
        watcher_path = watchers_path / watcher_file
        if watcher_path.exists():
            print_success(f"{watcher_file} exists")
        else:
            print_error(f"{watcher_file} missing")
            all_exist = False

    return all_exist

def test_gmail_watcher_import():
    """Test that Gmail watcher can be imported."""
    print_header("Testing Gmail Watcher Import")

    try:
        from gmail_watcher import GmailWatcher
        print_success("Gmail watcher imported successfully")

        # Test instantiation
        vault_path = Path(__file__).parent.parent
        watcher = GmailWatcher(str(vault_path))
        print_success("Gmail watcher instantiated successfully")

        # Test configuration
        if watcher.config:
            print_success("Gmail watcher configuration loaded")

        return True
    except ImportError as e:
        print_error(f"Failed to import Gmail watcher: {e}")
        return False
    except Exception as e:
        print_error(f"Failed to instantiate Gmail watcher: {e}")
        return False

def test_linkedin_watcher_import():
    """Test that LinkedIn watcher can be imported."""
    print_header("Testing LinkedIn Watcher Import")

    try:
        from linkedin_watcher import LinkedInWatcher
        print_success("LinkedIn watcher imported successfully")

        # Test instantiation
        vault_path = Path(__file__).parent.parent
        watcher = LinkedInWatcher(str(vault_path))
        print_success("LinkedIn watcher instantiated successfully")

        # Test configuration
        if watcher.config:
            print_success("LinkedIn watcher configuration loaded")

        return True
    except ImportError as e:
        print_error(f"Failed to import LinkedIn watcher: {e}")
        return False
    except Exception as e:
        print_error(f"Failed to instantiate LinkedIn watcher: {e}")
        return False

def test_skills_directory():
    """Test that all Silver Tier skills exist."""
    print_header("Testing Silver Tier Skills")

    project_root = Path(__file__).parent.parent.parent
    skills_path = project_root / '.claude' / 'skills'

    silver_skills = [
        'gmail-monitor',
        'send-email',
        'schedule-task',
        'whatsapp-monitor',
        'linkedin-automation'
    ]

    all_exist = True
    for skill in silver_skills:
        skill_path = skills_path / skill
        skill_md = skill_path / 'SKILL.md'
        prompt_md = skill_path / 'prompt.md'

        if skill_path.exists() and skill_md.exists() and prompt_md.exists():
            print_success(f"{skill} skill complete (SKILL.md + prompt.md)")
        else:
            print_error(f"{skill} skill incomplete or missing")
            all_exist = False

    return all_exist

def main():
    """Run all tests."""
    print_header("Silver Tier Comprehensive Test Suite")
    print("Testing all components of Silver Tier implementation...")

    results = {
        'Directory Structure': test_directory_structure(),
        'Configuration Files': test_configuration_files(),
        'Python Dependencies': test_python_dependencies(),
        'Credentials': test_credentials(),
        'Watcher Files': test_watcher_files(),
        'Gmail Watcher': test_gmail_watcher_import(),
        'LinkedIn Watcher': test_linkedin_watcher_import(),
        'Silver Tier Skills': test_skills_directory()
    }

    # Print summary
    print_header("Test Summary")

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print_header("✓ All Tests Passed!")
        print("Silver Tier is ready to use!")
        print("\nNext steps:")
        print("1. Run setup script: bash setup_silver_tier.sh (or .bat on Windows)")
        print("2. Test Gmail watcher: uv run python test_gmail_watcher.py")
        print("3. Test LinkedIn watcher: uv run python test_linkedin_watcher.py")
        print("4. Read SILVER_TIER_README.md for usage instructions")
        return 0
    else:
        print_header("✗ Some Tests Failed")
        print("Please fix the issues above before using Silver Tier.")
        print("\nCommon fixes:")
        print("- Run setup script: bash setup_silver_tier.sh")
        print("- Install dependencies: cd AI_Employee_Vault/watchers && uv sync")
        print("- Add credentials.json to project root")
        print("- See MCP_SETUP_GUIDE.md for detailed setup")
        return 1

if __name__ == '__main__':
    sys.exit(main())
