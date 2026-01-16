"""CLI entry point for YNAB MCP Server."""

import sys
import argparse
from pathlib import Path
import shutil


def setup_skills():
    """Copy skill-creator to ~/.skills/ynab/ if it doesn't exist."""
    # Determine the skills source directory
    package_dir = Path(__file__).parent
    
    # Try multiple locations for the skills directory
    possible_locations = [
        package_dir.parent.parent / ".skills" / "skill-creator",  # Development mode
        package_dir / ".skills" / "skill-creator",  # If bundled with package
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
        if source_skills:
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source_skills, dest_skills)
                print(f"✓ Skill-creator installed to {dest_skills}")
                return 0
            except Exception as e:
                print(f"⚠ Could not copy skill-creator: {e}")
                return 1
        else:
            print(f"⚠ Skill-creator not found. Please manually copy from the repository:")
            print(f"  git clone --depth 1 https://github.com/rgarcia/ynab-mcp-server.git /tmp/ynab-mcp-server")
            print(f"  mkdir -p ~/.skills/ynab")
            print(f"  cp -r /tmp/ynab-mcp-server/.skills/skill-creator ~/.skills/ynab/")
            print(f"  rm -rf /tmp/ynab-mcp-server")
            return 1
    else:
        print(f"✓ Skill-creator already exists at {dest_skills}")
        return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="YNAB MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--setup-skills",
        action="store_true",
        help="Install skill-creator to ~/.skills/ynab/ and exit",
    )
    
    args = parser.parse_args()
    
    if args.setup_skills:
        sys.exit(setup_skills())
    
    # If no special flags, run the MCP server
    from ynab_mcp_server.server import mcp
    mcp.run()


if __name__ == "__main__":
    main()
