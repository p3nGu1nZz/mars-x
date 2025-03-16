#!/usr/bin/env python3
"""
Mars-X setup script for environment setup and package installation.
"""

import os
import sys
import subprocess
import re
import shutil
from pathlib import Path
import time

# Path to virtual environment
VENV_DIR = Path(__file__).resolve().parent / ".venv"
PROJECT_ROOT = Path(__file__).resolve().parent
BUILD_DIR = PROJECT_ROOT / "build"

def print_help():
    print("""
Mars-X Setup Utility
--------------------
Usage: python setup.py [options]

Options:
  --build     Build the game executable
  --help      Show this help message and exit
    """)


def find_python_3_12():
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
    python_3_12_path = find_python_3_12()
    if not python_3_12_path:
        print("Python 3.12 not found. Please install it and try again.")
        sys.exit(1)

    # Create venv only if it doesn't exist
    if not VENV_DIR.exists():
        print("Creating virtual environment with Python 3.12...")
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
    # Use pip directly instead of any UV command
    subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(req_file)], check=True)
    
    print("Setup complete.")
    
    # Print activation instructions
    if os.name == 'nt':
        activate_cmd = str(VENV_DIR / "Scripts" / "activate.bat")
    else:
        activate_cmd = f"source {VENV_DIR / 'bin' / 'activate'}"
    
    print(f"""
Next steps:
-----------
1. To build the game executable:
   python setup.py --build

2. To activate the virtual environment and develop:
   {activate_cmd}

3. To get help:
   python setup.py --help
""")

# Add this section to setup.py to compile Cython modules before building

def compile_cython_modules():
    """Compile all Cython modules in the project."""
    from setuptools.extension import Extension
    from setuptools import setup
    from Cython.Build import cythonize
    import shutil
    import sys
    
    # Save the original command line arguments
    old_argv = sys.argv.copy()
    
    # Replace with minimal arguments for setup
    sys.argv = [sys.argv[0], 'build_ext', '--inplace']
    
    try:
        # Define the extensions
        extensions = [
            Extension(
                "mars_x.cython_modules.vector", 
                ["mars_x/cython_modules/vector.pyx"]
            ),
            Extension(
                "mars_x.cython_modules.collision", 
                ["mars_x/cython_modules/collision.pyx"]
            ),
            Extension(
                "mars_x.cython_modules.matrix", 
                ["mars_x/cython_modules/matrix.pyx"]
            ),
            Extension(
                "mars_x.cython_modules.quaternion", 
                ["mars_x/cython_modules/quaternion.pyx"]
            ),
            Extension(
                "mars_x.cython_modules.rigidbody", 
                ["mars_x/cython_modules/rigidbody.pyx"]
            ),
        ]
        
        # Compile
        print("Compiling Cython modules...")
        setup(
            name="mars_x_cython_modules",
            ext_modules=cythonize(
                extensions,
                compiler_directives={
                    'language_level': 3,
                    'boundscheck': False,
                    'wraparound': False
                }
            )
        )
    finally:
        # Restore original command line arguments
        sys.argv = old_argv
    
    # Move the compiled files to the correct location if needed
    print("Checking for compiled modules...")
    # Check both common locations: direct in package or in build directory
    
    # First check if files were built in-place (--inplace option)
    cython_dir = PROJECT_ROOT / "mars_x" / "cython_modules"
    modules_found = False
    
    for ext in ['.pyd', '.so']:
        if list(cython_dir.glob(f"*{ext}")):
            modules_found = True
            break
    
    # If not found in-place, check build directory
    if not modules_found:
        build_dirs = [d for d in (PROJECT_ROOT / "build").glob("lib.*")]
        if build_dirs:
            source_path = build_dirs[0] / "mars_x" / "cython_modules"
            if source_path.exists():
                dest_path = PROJECT_ROOT / "mars_x" / "cython_modules"
                for ext in ['.pyd', '.so']:
                    for file in source_path.glob(f"*{ext}"):
                        target = dest_path / file.name
                        print(f"Moving {file} to {target}")
                        shutil.copy2(file, target)
                modules_found = True
    
    if modules_found:
        print("Cython modules compiled successfully.")
    else:
        print("Warning: Could not find compiled Cython modules.")

# Function to activate the virtual environment and get the Python executable
def get_venv_python():
    if os.name == 'nt':
        python_exe = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"
    
    if not python_exe.exists():
        print(f"Error: Python executable not found at {python_exe}")
        print("Please run 'python setup.py' first to create the virtual environment.")
        sys.exit(1)
        
    return python_exe

def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        return
    
    if '--build' in sys.argv:
        # Make sure venv exists
        if not VENV_DIR.exists():
            print("Virtual environment not found. Creating it first...")
            manage_venv()
        
        # Get Python executable from venv
        python_exe = get_venv_python()
        
        # Import the build_game function from the new location
        try:
            # Make sure mars_x is in the path
            sys.path.insert(0, str(PROJECT_ROOT))
            
            # Run build_game.py using the venv Python
            build_script = PROJECT_ROOT / "mars_x" / "utils" / "build_game.py"
            if build_script.exists():
                print(f"Running build script with {python_exe}")
                result = subprocess.run(
                    [str(python_exe), str(build_script)],
                    check=True
                )
                return
            else:
                # Fallback to importing the function if script not found
                from mars_x.utils.build_game import build_game
                compile_cython_modules()
                build_game()
        except ImportError as e:
            print(f"Error importing build_game module: {e}")
            print("Make sure the mars_x/utils directory exists and contains build_game.py")
            sys.exit(1)
        return
        
    manage_venv()

if __name__ == "__main__":
    main()
