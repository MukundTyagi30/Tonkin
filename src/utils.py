"""Utility functions for the Tonkin Knowledge Finder."""

import os
import platform
import webbrowser
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def open_file(file_path: str) -> bool:
    """
    Open a file using the system's default application.
    Works cross-platform (Windows/Mac/Linux).
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        system = platform.system()
        
        if system == "Windows":
            # Use os.startfile on Windows
            os.startfile(file_path)
        elif system == "Darwin":  # macOS
            # Use 'open' command on macOS
            subprocess.run(["open", file_path], check=True)
        else:  # Linux and other Unix-like systems
            # Use 'xdg-open' on Linux
            subprocess.run(["xdg-open", file_path], check=True)
        
        logger.info(f"Opened file: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to open file {file_path}: {str(e)}")
        # Fallback: try using webbrowser module
        try:
            webbrowser.open(f"file://{os.path.abspath(file_path)}")
            return True
        except Exception as e2:
            logger.error(f"Fallback method also failed: {str(e2)}")
            return False


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable file size."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def format_date(date_obj, format_str: str = "%Y-%m-%d") -> str:
    """Format a date object to string."""
    if date_obj is None:
        return "Unknown"
    
    if isinstance(date_obj, str):
        try:
            # Try to parse ISO format
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except ValueError:
            return date_obj  # Return as-is if can't parse
    
    if isinstance(date_obj, datetime):
        return date_obj.strftime(format_str)
    
    return str(date_obj)


def get_relative_time(date_obj) -> str:
    """Get relative time description (e.g., '2 days ago', 'last month')."""
    if date_obj is None:
        return "Unknown"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except ValueError:
            return date_obj
    
    if not isinstance(date_obj, datetime):
        return str(date_obj)
    
    now = datetime.now()
    if date_obj.tzinfo:
        # If date has timezone info, make now timezone-aware
        from datetime import timezone
        now = now.replace(tzinfo=timezone.utc)
    
    diff = now - date_obj
    
    if diff.days == 0:
        if diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.days == 1:
        return "Yesterday"
    elif diff.days < 7:
        return f"{diff.days} days ago"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif diff.days < 365:
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove common document artifacts
    text = text.replace('\x0c', ' ')  # Form feed
    text = text.replace('\x0b', ' ')  # Vertical tab
    text = text.replace('\r\n', '\n')  # Windows line endings
    text = text.replace('\r', '\n')   # Mac line endings
    
    return text.strip()


def extract_names(text: str) -> List[str]:
    """Extract person names from text (simple heuristic)."""
    if not text:
        return []
    
    import re
    
    # Simple pattern for names (Title Case words)
    name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    names = re.findall(name_pattern, text)
    
    # Filter out common non-names
    common_words = {
        'Project', 'Manager', 'Leader', 'Director', 'Engineer', 'Team',
        'Department', 'Company', 'Client', 'South', 'Australia', 'New',
        'South Wales', 'Western Australia', 'Northern Territory',
        'Australian Capital Territory', 'Victoria', 'Tasmania', 'Queensland'
    }
    
    filtered_names = []
    for name in names:
        if len(name.split()) >= 2 and name not in common_words:
            # Check if it's likely a person's name
            words = name.split()
            if all(len(word) > 1 for word in words):  # No single letters
                filtered_names.append(name)
    
    return list(set(filtered_names))  # Remove duplicates


def create_trust_badges(doc: Dict[str, Any]) -> List[Dict[str, str]]:
    """Create trust badges for a document."""
    badges = []
    
    # Has reviewer badge
    if doc.get('project_reviewer'):
        badges.append({
            'text': 'Has Reviewer',
            'color': 'green',
            'icon': '✓'
        })
    
    # Complete header badge
    required_fields = ['project_name', 'project_number', 'project_leader', 'client']
    if all(doc.get(field) for field in required_fields):
        badges.append({
            'text': 'Complete Header',
            'color': 'blue',
            'icon': '📋'
        })
    
    # Recent document badge
    if doc.get('modified_date'):
        try:
            if isinstance(doc['modified_date'], str):
                mod_date = datetime.fromisoformat(doc['modified_date'].replace('Z', '+00:00'))
            else:
                mod_date = doc['modified_date']
            
            days_old = (datetime.now() - mod_date.replace(tzinfo=None)).days
            if days_old < 365:
                badges.append({
                    'text': 'Recent',
                    'color': 'orange',
                    'icon': '🕒'
                })
        except:
            pass
    
    # Content completeness
    content_fields = ['background', 'scope_of_work', 'deliverables']
    if all(doc.get(field) for field in content_fields):
        badges.append({
            'text': 'Complete Content',
            'color': 'purple',
            'icon': '📄'
        })
    
    # Region specified
    if doc.get('program_region'):
        badges.append({
            'text': 'Region Specified',
            'color': 'teal',
            'icon': '🌏'
        })
    
    # High trust score
    trust_score = doc.get('trust_score', 0)
    if trust_score >= 0.8:
        badges.append({
            'text': 'High Quality',
            'color': 'gold',
            'icon': '⭐'
        })
    
    return badges


def highlight_query_terms(text: str, query: str, max_highlights: int = 3) -> str:
    """Highlight query terms in text (for snippet display)."""
    if not text or not query:
        return text
    
    import re
    
    query_words = [word.lower() for word in query.split() if len(word) > 2]
    highlighted_text = text
    
    for word in query_words[:max_highlights]:
        # Case-insensitive highlighting
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted_text = pattern.sub(f"**{word}**", highlighted_text)
    
    return highlighted_text


def validate_file_type(file_path: str, supported_extensions: List[str] = None) -> bool:
    """Validate if file type is supported."""
    if supported_extensions is None:
        supported_extensions = ['.docx', '.pdf']
    
    file_ext = Path(file_path).suffix.lower()
    return file_ext in supported_extensions


def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """Get basic file metadata."""
    if not os.path.exists(file_path):
        return {}
    
    stat = os.stat(file_path)
    path_obj = Path(file_path)
    
    return {
        'name': path_obj.name,
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'created': datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'extension': path_obj.suffix.lower()
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename


def create_progress_callback(total_items: int, description: str = "Processing"):
    """Create a progress callback function for long operations."""
    def callback(current: int):
        percentage = (current / total_items) * 100
        print(f"\r{description}: {current}/{total_items} ({percentage:.1f}%)", end="", flush=True)
        if current == total_items:
            print()  # New line when complete
    
    return callback


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Setup logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def main():
    """Test utility functions."""
    # Test file opening
    test_file = "/Users/mukundtyagi/Desktop/tonkin protoype /SF84_Project_Basis_Report_V1.pdf"
    if os.path.exists(test_file):
        print(f"Testing file open: {test_file}")
        # print(f"Success: {open_file(test_file)}")
        
        # Test metadata
        metadata = get_file_metadata(test_file)
        print(f"File metadata: {metadata}")
    
    # Test date formatting
    now = datetime.now()
    print(f"Current time: {format_date(now)}")
    print(f"Relative time: {get_relative_time(now - timedelta(days=5))}")
    
    # Test text cleaning
    dirty_text = "  This   is\r\n  messy    text\x0c  "
    clean = clean_text(dirty_text)
    print(f"Cleaned text: '{clean}'")


if __name__ == "__main__":
    main()
