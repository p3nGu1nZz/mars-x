#!/usr/bin/env python3
"""
Mars-X setup script for environment setup and build processes.
"""

import os
import sys
import subprocess
import glob
import shutil
import time
import tempfile
from pathlib import Path

# Add the project directory to the path so we can import our modules
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from mars_x.utils.setup_help import print_help
from mars_x.utils.constants import PROJECT_ROOT, VENV_DIR


def is_venv_present():
    """Check if virtual environment exists in the project root."""
    return VENV_DIR.exists()


def has_required_executables():
    """Check if the virtual environment has the required executables."""
    python_exe = get_python_executable()
    pip_exe = get_pip_executable()
    return os.path.exists(python_exe) and os.path.exists(pip_exe)


def safe_rmtree(path, retries=5, delay=1):
    """
    Safely remove a directory tree, with retries for Windows file locking issues.
    """
    for i in range(retries):
        try:
            if os.path.exists(path):
                if os.name == 'nt':  # Windows
                    # On Windows, sometimes we need to run a garbage collection to release file handles
                    import gc
                    gc.collect()
                shutil.rmtree(path)
            return True
        except (OSError, PermissionError) as e:
            if i == retries - 1:
                print(f"Warning: Failed to remove {path}: {e}")
                return False
            print(f"Retrying removal of {path} in {delay} seconds...")
            time.sleep(delay)
    return False


def cleanup_egg_info():
    """Clean up any existing .egg-info directories in the project root."""
    print("Cleaning up existing installation artifacts...")
    
    # Look for .egg-info directories in several places
    patterns = [
        os.path.join(PROJECT_ROOT, "*.egg-info"),
        os.path.join(PROJECT_ROOT, "*", "*.egg-info"),
        os.path.join(tempfile.gettempdir(), "pip-*-build", "*.egg-info"),
    ]
    
    for pattern in patterns:
        for egg_dir in glob.glob(pattern):
            print(f"Removing {os.path.basename(egg_dir)}")
            safe_rmtree(egg_dir)
    
    # Also clean up build directory if it exists
    build_dir = os.path.join(PROJECT_ROOT, "build")
    if os.path.exists(build_dir):
        print(f"Removing build directory")
        safe_rmtree(build_dir)
        
    # Remove any .eggs directory
    eggs_dir = os.path.join(PROJECT_ROOT, ".eggs")
    if os.path.exists(eggs_dir):
        print(f"Removing .eggs directory")
        safe_rmtree(eggs_dir)


def create_venv():
    """Create a virtual environment if it doesn't exist."""
    if not is_venv_present():
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
            print("Virtual environment created successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            print("If you need to recreate the environment, delete the .venv directory manually.")
            sys.exit(1)
    else:
        print("Virtual environment already exists.")
        if not has_required_executables():
            print("Warning: Virtual environment appears to be incomplete.")
            print("Consider deleting the .venv directory manually and running setup.py again.")
        return False


def get_python_executable():
    """Get the Python executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return VENV_DIR / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        return VENV_DIR / "bin" / "python"


def get_pip_executable():
    """Get the pip executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return VENV_DIR / "Scripts" / "pip.exe"
    else:  # Unix/Linux/Mac
        return VENV_DIR / "bin" / "pip"


def upgrade_pip(pip_executable):
    """Upgrade pip to the latest version."""
    print("Upgrading pip to the latest version...")
    
    # First try using python -m pip which is more reliable
    python_executable = get_python_executable()
    try:
        subprocess.run([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("Pip upgraded successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to upgrade pip using python -m pip: {e}")
    
    # Fallback to direct pip command if available
    try:
        subprocess.run([str(pip_executable), "install", "--upgrade", "pip"], check=True)
        print("Pip upgraded successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to upgrade pip: {e}")
        return False


def update_existing_venv():
    """Update the existing virtual environment."""
    print("Updating existing virtual environment...")
    
    if not has_required_executables():
        print("Virtual environment appears to be broken or incomplete.")
        print("Please delete the .venv directory manually and run setup.py again.")
        sys.exit(1)
    
    # Make sure we have a working Python in the venv
    python_executable = get_python_executable()
    pip_executable = get_pip_executable()
    
    # Upgrade pip first using the Python executable directly
    if not upgrade_pip(pip_executable):
        print("Warning: Failed to upgrade pip. Continuing with installation anyway.")
    
    # Clean up any existing egg-info directories
    cleanup_egg_info()
    
    # Try installation using python -m pip which is more reliable
    print("Updating dependencies...")
    try:
        subprocess.run([str(python_executable), "-m", "pip", "install", "--upgrade", "."], check=True)
        subprocess.run([str(python_executable), "-m", "pip", "install", "--upgrade", ".[dev]"], check=True)
        print("Virtual environment updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating dependencies: {e}")
        print("If you need to recreate the environment, delete the .venv directory manually and run setup.py again.")
        sys.exit(1)


def setup_dependencies():
    """Install project dependencies in the virtual environment."""
    print("Installing dependencies...")
    
    # Get the Python executable in the virtual environment
    python_executable = get_python_executable()
    pip_executable = get_pip_executable()
    
    # Upgrade pip first
    if not upgrade_pip(pip_executable):
        print("Warning: Failed to upgrade pip. Continuing with installation anyway.")
    
    # Clean up any existing egg-info directories
    cleanup_egg_info()
    
    # Install from pyproject.toml using python -m pip
    try:
        subprocess.run([str(python_executable), "-m", "pip", "install", "."], check=True)
        subprocess.run([str(python_executable), "-m", "pip", "install", ".[dev]"], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


def build_cython_modules():
    """Build Cython modules."""
    print("Building Cython modules...")
    python_executable = get_python_executable()
    
    # Clean up any existing egg-info directories first
    cleanup_egg_info()
    
    try:
        subprocess.run([str(python_executable), "-m", "pip", "install", "--no-deps", "--force-reinstall", "."], check=True)
        print("Cython modules built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Cython modules: {e}")
        sys.exit(1)


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("Checking if dependencies are up to date...")
    python_executable = get_python_executable()
    
    # Try to import key modules to verify installation
    check_script = """
import sys
try:
    import pysdl2
    import appdirs
    print("Core dependencies found.")
    sys.exit(0)
except ImportError as e:
    print(f"Missing dependencies: {e}")
    sys.exit(1)
"""
    
    try:
        result = subprocess.run(
            [str(python_executable), "-c", check_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print("Some dependencies appear to be missing.")
            print("Consider running with --update to install missing packages.")
            return False
        return True
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        return False


def main():
    """Main setup function."""
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        return
    
    # Check for virtual environment
    if is_venv_present():
        print("Found existing virtual environment.")
        
        if not has_required_executables():
            print("Virtual environment appears to be incomplete.")
            print("Please delete the .venv directory manually and run setup.py again.")
            sys.exit(1)
        
        if '--update' in sys.argv:
            # Update existing environment
            update_existing_venv()
        else:
            # Check if dependencies are installed and up to date
            deps_ok = check_dependencies()
            if not deps_ok:
                print("Run 'python setup.py --update' to install missing dependencies.")
                ask = input("Would you like to update the environment now? (y/n): ")
                if ask.lower().startswith('y'):
                    update_existing_venv()
            else:
                print("Environment appears to be properly set up.")
                print("Use --update if you want to refresh all dependencies.")
    else:
        print("No virtual environment found.")
        is_new = create_venv()
        if is_new:
            setup_dependencies()
    
    # Build Cython modules if requested
    if '--build' in sys.argv:
        build_cython_modules()


if __name__ == "__main__":
    main()
