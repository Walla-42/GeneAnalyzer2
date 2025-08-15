#!/usr/bin/env python3
import shutil
import os
from pathlib import Path
import subprocess

def main():
    repo_root = Path(__file__).resolve().parent.parent
    git_dir = repo_root / ".git"
    hooks_dir = git_dir / "hooks"
    githooks_dir = repo_root / ".githooks"

    if not git_dir.exists():
        print("No .git directory found. Skipping hook installation.")
        return

    # Copy hooks
    for hook in githooks_dir.iterdir():
        target = hooks_dir / hook.name
        shutil.copy(hook, target)
        os.chmod(target, 0o755)

    # Set commit template
    subprocess.run(
        ["git", "config", "commit.template", str(repo_root / ".gitmessage.txt")],
        check=True
    )

    print("Git hooks and commit template installed successfully.")

if __name__ == "__main__":
    main()
