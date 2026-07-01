"""
ELUSoC_2026 - Bandit Security Audit script.
Automates running the Bandit vulnerability linter and analyzing outputs.
"""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    print("Executing security check scan on agentwatch modules...")
    # Execute bandit command on source files using sys.executable to ensure portability
    result = subprocess.run(
        [sys.executable, "-m", "bandit", "-r", "agentwatch", "-ll"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"Security audit failed! Fix vulnerability warnings. Code: {result.returncode}")
        sys.exit(result.returncode)
        
    print("Security audit passed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
