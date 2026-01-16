"""Post-install script to set up skills directory."""

import os
import shutil
from pathlib import Path
import sys


def main():
    """Copy skill-creator to ~/.skills/ynab/ if it doesn't exist."""
    # Determine the skills source directory
    # When installed via pip/uv tool, skills are in the package data
    package_dir = Path(__file__).parent
    
    # Try multiple locations for the skills directory
    possible_locations = [
        package_dir.parent.parent / ".skills" / "skill-creator",  # Development mode
        package_dir / ".skills" / "skill-creator",  # If bundled with package
        Path(sys.prefix) / "share" / "ynab-mcp-server" / ".skills" / "skill-creator",  # Standard data location
    ]
    
    source_skills = None
    for location in possible_locations:
        if location.exists():
            source_skills = location
            break
    
    # Determine the destination directory
    home = Path.home()
    dest_dir = home / ".skills" / "ynab"
    dest_skills = dest_dir / "skill-creator"
    
    # Only copy if destination doesn't exist
    if not dest_skills.exists():
        if source_skills and source_skills.exists():
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source_skills, dest_skills)
                print(f"✓ Skill-creator installed to {dest_skills}")
            except Exception as e:
                print(f"⚠ Could not copy skill-creator: {e}")
        else:
            print(f"⚠ Skill-creator not found. Please manually copy from the repository:")
            print(f"  git clone --depth 1 https://github.com/rgarcia/ynab-mcp-server.git /tmp/ynab-mcp-server")
            print(f"  mkdir -p ~/.skills/ynab")
            print(f"  cp -r /tmp/ynab-mcp-server/.skills/skill-creator ~/.skills/ynab/")
            print(f"  rm -rf /tmp/ynab-mcp-server")
    else:
        print(f"✓ Skill-creator already exists at {dest_skills}")


if __name__ == "__main__":
    main()
