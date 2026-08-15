import os
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def delete_file(file_path: str | Path) -> bool:
    """Safely deletes a single file."""
    try:
        path = Path(file_path)
        if path.exists() and path.is_file():
            path.unlink()
            return True
    except Exception as e:
        logger.error(f"Error removing file {file_path}: {e}")
    return False

def clean_temp_directory(temp_dir: Path, max_age_seconds: int = 3600) -> None:
    """Removes leftover temporary files older than max_age_seconds."""
    now = time.time()
    if not temp_dir.exists():
        return
    for item in temp_dir.iterdir():
        if item.is_file():
            try:
                if now - item.stat().st_mtime > max_age_seconds:
                    item.unlink()
            except Exception as e:
                logger.error(f"Failed to purge old temp file {item}: {e}")
