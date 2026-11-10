"""Extract student names from LMS-exported ZIP filenames."""
from pathlib import Path
import re


def extract_student_name(filename):
    stem = Path(filename.replace('\\', '/')).stem
    # LMS format: 98073-118636 - JAVEN ONG JUN KAI _ - Oct 29, 2026 ...
    match = re.match(r'^\s*\d+(?:-\d+)+\s*-\s*(.+?)\s*(?:_\s*)?-\s*(?:[A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})\b', stem)
    if match:
        name = match.group(1).strip(' _-')
    else:
        # Some exports have no date; retain original if the name is ambiguous.
        match = re.match(r'^\s*\d+(?:-\d+)+\s*-\s*([^_]+?)(?:\s+_\s*-|$)', stem)
        name = match.group(1).strip(' _-') if match else stem.strip()
    # Convert all-uppercase names to title case; preserve mixed-case names.
    return name.title() if name.isupper() else name
