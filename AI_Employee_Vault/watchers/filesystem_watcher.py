"""File system watcher for monitoring drop folder."""
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handler for file system events in the drop folder."""

    def __init__(self, vault_path: Path, logger):
        self.vault_path = vault_path
        self.needs_action = vault_path / 'Needs_Action'
        self.logger = logger
        self.processed_files = set()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Skip if already processed
        if source.name in self.processed_files:
            return

        # Skip hidden files and system files
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        try:
            # Wait a moment to ensure file is fully written
            import time
            time.sleep(0.5)

            # Copy file to Needs_Action
            dest = self.needs_action / f'FILE_{source.name}'
            shutil.copy2(source, dest)

            # Create metadata file
            self.create_metadata(source, dest)

            self.processed_files.add(source.name)
            self.logger.info(f'Processed new file: {source.name}')

        except Exception as e:
            self.logger.error(f'Error processing file {source.name}: {e}')

    def create_metadata(self, source: Path, dest: Path):
        """Create a markdown metadata file for the dropped file."""
        meta_path = dest.with_suffix(dest.suffix + '.md')

        # Get file stats
        stats = source.stat()
        size_kb = stats.st_size / 1024

        content = f"""---
type: file_drop
original_name: {source.name}
size: {size_kb:.2f} KB
created: {datetime.now().isoformat()}
status: pending
priority: medium
---

## New File Dropped for Processing

**File**: {source.name}
**Size**: {size_kb:.2f} KB
**Location**: {dest.relative_to(self.vault_path)}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or forward as needed
- [ ] Move to /Done when complete

## Notes
Add any relevant notes or observations here.
"""
        meta_path.write_text(content, encoding='utf-8')


class FileSystemWatcher(BaseWatcher):
    """Watcher for monitoring a drop folder for new files."""

    def __init__(self, vault_path: str, drop_folder: str = None):
        super().__init__(vault_path, check_interval=5)

        # Use Inbox as default drop folder
        if drop_folder is None:
            self.drop_folder = self.vault_path / 'Inbox'
        else:
            self.drop_folder = Path(drop_folder)

        # Create drop folder if it doesn't exist
        self.drop_folder.mkdir(parents=True, exist_ok=True)

        # Set up file system observer
        self.observer = Observer()
        self.event_handler = DropFolderHandler(self.vault_path, self.logger)

    def check_for_updates(self) -> list:
        """Not used in this implementation - using observer pattern instead."""
        return []

    def create_action_file(self, item) -> Path:
        """Not used in this implementation - handled by event handler."""
        pass

    def run(self):
        """Start monitoring the drop folder."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring drop folder: {self.drop_folder}')
        self.logger.info(f'Vault path: {self.vault_path}')

        # Schedule the observer
        self.observer.schedule(self.event_handler, str(self.drop_folder), recursive=False)
        self.observer.start()

        self.logger.info('File system watcher is now active')
        self.logger.info('Drop files into the Inbox folder to trigger processing')

        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info('Stopping file system watcher...')
            self.observer.stop()

        self.observer.join()
        self.logger.info('File system watcher stopped')


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default to parent directory of watchers folder
        vault_path = Path(__file__).parent.parent

    # Create and run the watcher
    watcher = FileSystemWatcher(str(vault_path))
    watcher.run()
