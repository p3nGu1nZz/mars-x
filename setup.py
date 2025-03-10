#!/usr/bin/env python3
"""
Mars-X setup script for environment setup and package installation.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from mars_x.utils.setup_help import print_help  # Use the help function from setup_help.py

# Path to virtual environment
VENV_DIR = Path(__file__).resolve().parent / ".venv"
PROJECT_ROOT = Path(__file__).resolve().parent

def find_python_3_12():
    """Find Python 3.12 using 'py -0p' to list available installations."""
    try:
        output = subprocess.check_output(["py", "-0p"], text=True)
        for line in output.splitlines():
            line = line.strip()
            match = re.match(r"^-V:3\.12(?:-64|-32)?\s+(\S+)", line)
            if match:
                python_path = Path(match.group(1))
                print(f"Found Python 3.12 at: {python_path}")
                return python_path
        print("Python 3.12 not found.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'py -0p': {e}")
        return None

def manage_venv():
    """Set up and manage the virtual environment."""
    python_3_12_path = find_python_3_12()
    if not python_3_12_path:
        print("Python 3.12 not found. Please install it and try again.")
        sys.exit(1)

    if not VENV_DIR.exists():
        print("Creating virtual environment...")
        try:
            subprocess.run([str(python_3_12_path), "-m", "venv", str(VENV_DIR)], check=True)
            print("Virtual environment created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            sys.exit(1)
    else:
        print("Using existing virtual environment.")
    
    if os.name == 'nt':
        python_exe = VENV_DIR / "Scripts" / "python.exe"
        pip_exe = VENV_DIR / "Scripts" / "pip.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"
        pip_exe = VENV_DIR / "bin" / "pip"
    
    if not python_exe.exists():
        print(f"Error: Python executable not found at {python_exe}")
        sys.exit(1)

    # Upgrade pip and install dependencies from requirements.txt
    print("Setting up virtual environment...")
    subprocess.run([str(python_exe), "-m", "ensurepip", "--upgrade"], check=True)
    subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Install requirements from requirements.txt
    req_file = PROJECT_ROOT / "requirements.txt"
    subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(req_file)], check=True)
    
    print("Setup complete.")
    
    # Print activation instructions
    if os.name == 'nt':
        activate_cmd = str(VENV_DIR / "Scripts" / "activate.bat")
    else:
        activate_cmd = f"source {VENV_DIR / 'bin' / 'activate'}"
    
    print(f"\nTo activate the virtual environment, run:\n{activate_cmd}\n")

def main():
    """Main entry point."""
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        return
        
    # Manage the virtual environment
    manage_venv()

if __name__ == "__main__":
    main()
