"""Post approved LinkedIn content using browser automation."""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_watcher import LinkedInWatcher

def post_to_linkedin(post_file_path):
    """Post content to LinkedIn."""
    print("=" * 60)
    print("LinkedIn Post Publisher")
    print("=" * 60)
    print()

    # Read the post file
    post_file = Path(post_file_path)
    if not post_file.exists():
        print(f"Error: Post file not found: {post_file_path}")
        return False

    # Parse the post content
    content = post_file.read_text(encoding='utf-8')

    # Extract post content (between ## Post Content and ---)
    lines = content.split('\n')
    post_content = []
    in_content = False

    for line in lines:
        if '## Post Content' in line:
            in_content = True
            continue
        if in_content and line.strip() == '---':
            break
        if in_content and line.strip():
            post_content.append(line)

    post_text = '\n'.join(post_content).strip()

    if not post_text:
        print("Error: Could not extract post content")
        return False

    print("Post content extracted:")
    print("-" * 60)
    print(post_text[:200] + "..." if len(post_text) > 200 else post_text)
    print("-" * 60)
    print()

    # Initialize LinkedIn watcher for browser automation
    vault_path = Path(__file__).parent.parent
    watcher = LinkedInWatcher(str(vault_path))

    print("Initializing browser...")
    if not watcher._init_browser():
        print("Error: Failed to initialize browser")
        return False

    print("Browser initialized successfully")
    print()

    # Load saved session
    if not watcher._load_session():
        print("Warning: No saved session found")
        print("Attempting to login...")
        if not watcher._login_linkedin():
            print("Error: Login failed")
            watcher._cleanup_browser()
            return False

    print("Logged in to LinkedIn successfully")
    print()

    try:
        # Navigate to LinkedIn feed
        print("Navigating to LinkedIn feed...")
        watcher.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
        watcher.page.wait_for_timeout(2000)

        # Click "Start a post" button
        print("Opening post composer...")
        start_post_button = watcher.page.wait_for_selector('button[aria-label*="Start a post"]', timeout=10000)
        start_post_button.click()
        watcher.page.wait_for_timeout(1000)

        # Type the post content
        print("Typing post content...")
        editor = watcher.page.wait_for_selector('div[role="textbox"]', timeout=10000)
        editor.click()
        editor.fill(post_text)
        watcher.page.wait_for_timeout(1000)

        # Click Post button
        print("Publishing post...")
        post_button = watcher.page.wait_for_selector('button[aria-label*="Post"]', timeout=10000)
        post_button.click()
        watcher.page.wait_for_timeout(3000)

        print()
        print("=" * 60)
        print("✓ Post published successfully!")
        print("=" * 60)
        print()
        print("Your post is now live on LinkedIn!")
        print("Check your LinkedIn profile to see it.")
        print()

        # Move post file to Done folder
        done_folder = vault_path / 'Done'
        done_folder.mkdir(exist_ok=True)
        done_file = done_folder / f"POSTED_{post_file.name}"
        post_file.rename(done_file)
        print(f"Post file moved to: {done_file}")

        # Log the action
        log_file = vault_path / 'Logs' / f"{datetime.now().strftime('%Y-%m-%d')}_linkedin_log.json"
        log_file.parent.mkdir(exist_ok=True)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": "linkedin_post_published",
            "post_file": post_file.name,
            "post_preview": post_text[:100] + "..." if len(post_text) > 100 else post_text,
            "status": "success"
        }

        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
            logs.append(log_entry)
        else:
            logs = [log_entry]

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        print(f"Action logged to: {log_file}")

        return True

    except Exception as e:
        print(f"Error posting to LinkedIn: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        watcher._cleanup_browser()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python post_to_linkedin.py <path_to_post_file>")
        print()
        print("Example:")
        print("  python post_to_linkedin.py ../Approved/LINKEDIN_POST_20260307_AI_Employee.md")
        sys.exit(1)

    post_file = sys.argv[1]
    success = post_to_linkedin(post_file)
    sys.exit(0 if success else 1)
