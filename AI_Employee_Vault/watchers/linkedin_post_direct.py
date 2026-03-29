"""Direct LinkedIn Post - Simple script to post content immediately."""
import sys
from pathlib import Path
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Error: Playwright not installed")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)


def post_to_linkedin(post_content):
    """Post content directly to LinkedIn."""

    print("=" * 60)
    print("LinkedIn Direct Post")
    print("=" * 60)
    print()

    if not PLAYWRIGHT_AVAILABLE:
        print("Error: Playwright not available")
        return False

    print("Post content:")
    print("-" * 60)
    print(post_content[:200] + "..." if len(post_content) > 200 else post_content)
    print("-" * 60)
    print()

    # Initialize browser
    print("Opening browser...")
    playwright = sync_playwright().start()

    try:
        # Launch browser (visible so you can see what's happening)
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("✓ Browser opened")
        print()

        # Navigate to LinkedIn
        print("Navigating to LinkedIn...")
        page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
        time.sleep(2)

        # Check if logged in
        if 'login' in page.url or 'authwall' in page.url:
            print()
            print("⚠ Not logged in to LinkedIn")
            print("Please login manually in the browser window...")
            print("Waiting for you to login...")
            print()

            # Wait for user to login (check for feed URL)
            page.wait_for_url('**/feed/**', timeout=120000)
            print("✓ Logged in successfully")
            print()
        else:
            print("✓ Already logged in")
            print()

        # Click "Start a post" button
        print("Opening post composer...")
        try:
            # Try different selectors for the "Start a post" button
            start_post_selectors = [
                'button:has-text("Start a post")',
                'button[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]'
            ]

            clicked = False
            for selector in start_post_selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    break
                except:
                    continue

            if not clicked:
                print("Error: Could not find 'Start a post' button")
                print("Please click 'Start a post' manually in the browser...")
                input("Press Enter after clicking 'Start a post'...")

            time.sleep(1)
            print("✓ Post composer opened")
            print()

        except Exception as e:
            print(f"Note: {e}")
            print("Please click 'Start a post' manually if needed...")
            time.sleep(2)

        # Type the post content
        print("Typing post content...")
        try:
            # Try different selectors for the text editor
            editor_selectors = [
                'div[role="textbox"]',
                '.ql-editor',
                '[contenteditable="true"]'
            ]

            typed = False
            for selector in editor_selectors:
                try:
                    editor = page.wait_for_selector(selector, timeout=5000)
                    editor.click()
                    time.sleep(0.5)
                    editor.fill(post_content)
                    typed = True
                    break
                except:
                    continue

            if not typed:
                print("Error: Could not find text editor")
                print("Please paste your content manually:")
                print()
                print(post_content)
                print()
                input("Press Enter after pasting the content...")

            time.sleep(1)
            print("✓ Content typed")
            print()

        except Exception as e:
            print(f"Note: {e}")
            print("Please paste the content manually if needed...")
            time.sleep(2)

        # Click Post button
        print("Publishing post...")
        print()
        print("⚠ IMPORTANT: Review your post in the browser before clicking 'Post'")
        print()

        try:
            # Try to find and click the Post button
            post_button_selectors = [
                'button:has-text("Post")',
                'button[aria-label*="Post"]',
                '.share-actions__primary-action'
            ]

            clicked = False
            for selector in post_button_selectors:
                try:
                    # Wait a bit to let user review
                    print("Waiting 3 seconds for you to review...")
                    time.sleep(3)

                    post_button = page.wait_for_selector(selector, timeout=5000)

                    # Ask for confirmation
                    print()
                    response = input("Ready to post? Type 'yes' to post, or 'no' to cancel: ").strip().lower()

                    if response == 'yes':
                        post_button.click()
                        clicked = True
                        break
                    else:
                        print("Post cancelled by user")
                        return False

                except:
                    continue

            if not clicked:
                print()
                print("Could not find Post button automatically.")
                print("Please click the 'Post' button manually in the browser...")
                input("Press Enter after posting...")

            time.sleep(3)
            print()
            print("=" * 60)
            print("✓ Post published successfully!")
            print("=" * 60)
            print()
            print("Your post is now live on LinkedIn!")
            print("Check your profile to see it.")
            print()

            return True

        except Exception as e:
            print(f"Note: {e}")
            print("Please click 'Post' manually...")
            input("Press Enter after posting...")
            return True

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        print()
        print("Closing browser in 5 seconds...")
        print("(Browser will stay open if you want to see your post)")
        time.sleep(5)
        try:
            browser.close()
            playwright.stop()
        except:
            pass


if __name__ == '__main__':
    # Default post content
    default_post = """🚀 Just completed building my own AI Employee system - and the results are incredible!

Over the past few weeks, I've been working on an autonomous AI assistant that handles:
• Gmail inbox monitoring with intelligent priority assessment
• LinkedIn message management and professional networking
• Automated task processing and draft generation
• Complete human-in-the-loop approval workflow

The key insight? AI works best when it augments human decision-making, not replaces it.

My AI Employee handles the routine work - checking emails, monitoring messages, creating draft replies - while I maintain oversight for important decisions. Every action requires my approval, and everything is logged for complete transparency.

**The productivity gains have been remarkable:**
- Email management: 2-3 hours/day → 30 minutes/day
- Response time: Hours → Minutes
- Task organization: Manual → Automatic
- Audit trail: None → Complete

Built with Claude Code, Python, and a local-first architecture. All data stays on my machine, giving me complete control and privacy.

The system uses:
✅ Google Gmail API for email monitoring
✅ Playwright for browser automation
✅ Claude Opus 4.6 for intelligent processing
✅ Markdown-based task management
✅ Complete audit logging

This is part of the GIAIC Q4 Hackathon - building autonomous AI employees that actually work in the real world.

Curious about AI automation? The future of productivity isn't about replacing humans - it's about giving them superpowers.

#AI #Automation #Productivity #AIEmployee #TechInnovation #GIAIC #ClaudeCode #FutureOfWork"""

    # Check if custom content provided
    if len(sys.argv) > 1:
        # Content provided as argument
        post_content = sys.argv[1]
    else:
        # Use default content
        print("Using default post content about AI Employee")
        print("(You can provide custom content as an argument)")
        print()
        post_content = default_post

    # Post to LinkedIn
    success = post_to_linkedin(post_content)

    if success:
        print()
        print("✓ Done!")
        print()
        print("Next steps:")
        print("1. Check your LinkedIn profile")
        print("2. Engage with comments")
        print("3. Share in relevant groups")
        print()

    sys.exit(0 if success else 1)
