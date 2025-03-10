#!/usr/bin/env python3
"""
Build script for Mars-X game executable.
"""

import os
import sys
import subprocess
import re
import shutil
from pathlib import Path
import time
import datetime

# Path constants - now defined relative to this file's location
UTILS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = UTILS_DIR.parent.parent
VENV_DIR = PROJECT_ROOT / ".venv"
BUILD_DIR = PROJECT_ROOT / "build"

def format_size(size_bytes):
    """Format size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024 or unit == 'GB':
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

def format_time(seconds):
    """Format time in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes} min {secs:.1f} sec"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours} hr {minutes} min"

def build_game():
    """Build the game executable."""
    # Start timer for build telemetry
    build_start = datetime.datetime.now()
    build_start_time = time.time()
    build_files_count = 0
    
    # Create a build log file
    build_log_path = BUILD_DIR / "build_log.txt"
    if not BUILD_DIR.exists():
        os.makedirs(BUILD_DIR)
    
    # Log initial build information
    with open(build_log_path, "a") as log:
        log.write(f"\n\n--- Build started at {build_start.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    
    # Check if virtual environment exists, if not create it
    if not VENV_DIR.exists():
        print("Virtual environment not found. Creating one first...")
        # Import and call manage_venv from setup.py
        sys.path.insert(0, str(PROJECT_ROOT))
        from setup import manage_venv
        manage_venv()
    else:
        # Make sure we have the latest requirements
        print("Updating dependencies in existing virtual environment...")
        if os.name == 'nt':
            python_exe = VENV_DIR / "Scripts" / "python.exe"
        else:
            python_exe = VENV_DIR / "bin" / "python"
        
        req_file = PROJECT_ROOT / "requirements.txt"
        subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(req_file)], check=True)
    
    # Get the Python executable from the virtual environment
    if os.name == 'nt':
        python_exe = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"
    
    if not python_exe.exists():
        print(f"Error: Python executable not found at {python_exe}")
        print("The virtual environment appears to be corrupted.")
        print("Please delete it and run 'python setup.py' again.")
        sys.exit(1)

    # Create build directory if it doesn't exist
    if not BUILD_DIR.exists():
        os.makedirs(BUILD_DIR)
    
    # Create resources directory if it doesn't exist
    resources_dir = PROJECT_ROOT / "resources"
    if not resources_dir.exists():
        print("Creating resources directory...")
        os.makedirs(resources_dir)
    
    print("Building game executable...")
    
    # First, compile Cython modules
    print("Compiling Cython modules...")
    try:
        # Check if cython is installed before installing
        result = subprocess.run(
            [str(python_exe), "-c", "import cython; print('installed')"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        if "installed" not in result.stdout:
            print("Installing Cython...")
            subprocess.run([str(python_exe), "-m", "pip", "install", "cython"], check=True)
            
        cython_dirs = ["mars_x/engine", "mars_x/game"]
        
        for cython_dir in cython_dirs:
            dir_path = PROJECT_ROOT / cython_dir
            if dir_path.exists():
                pyx_files = list(dir_path.glob("**/*.pyx"))
                if pyx_files:
                    for pyx_file in pyx_files:
                        print(f"Compiling {pyx_file}")
                        subprocess.run([
                            str(python_exe), "-m", "cython", 
                            "-3", "--cplus", str(pyx_file)
                        ], check=True)
                        build_files_count += 1
                else:
                    print(f"No .pyx files found in {dir_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Cython modules: {e}")
        sys.exit(1)

    # Then, build executable with PyInstaller
    print("Building executable with PyInstaller...")
    try:
        # Check if pyinstaller is installed before installing
        result = subprocess.run(
            [str(python_exe), "-c", "import PyInstaller; print('installed')"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        if "installed" not in result.stdout:
            print("Installing PyInstaller...")
            subprocess.run([str(python_exe), "-m", "pip", "install", "pyinstaller"], check=True)
        
        # Find the SDL2 DLL files directly - improving the detection
        print("Locating SDL2 libraries...")
        sdl2_dll_cmd = """
import os, sys, glob, site

def find_sdl2_dlls():
    # First check if pysdl2-dll package is installed
    try:
        # Try direct approach with sdl2dll
        from sdl2dll import get_dll_path
        dll_path = get_dll_path()
        dlls = glob.glob(os.path.join(dll_path, "*.dll"))
        if dlls:
            return dll_path, [os.path.basename(dll) for dll in dlls]
    except ImportError:
        pass
    
    # Try alternate approach - check site-packages/sdl2dll
    for site_dir in site.getsitepackages():
        sdl2dll_path = os.path.join(site_dir, "sdl2dll", "dll")
        if os.path.exists(sdl2dll_path):
            dlls = glob.glob(os.path.join(sdl2dll_path, "*.dll"))
            if dlls:
                return sdl2dll_path, [os.path.basename(dll) for dll in dlls]
    
    # Check other common locations
    for site_dir in site.getsitepackages():
        # Look for SDL2 DLLs in pysdl2 directory
        sdl2_path = os.path.join(site_dir, "sdl2")
        if os.path.exists(sdl2_path):
            dlls = glob.glob(os.path.join(sdl2_path, "*.dll"))
            if dlls:
                return sdl2_path, [os.path.basename(dll) for dll in dlls]
    
    return None, []

path, dlls = find_sdl2_dlls()
if path:
    print(f"FOUND_DLLS:{path}")
    for dll in dlls:
        print(f"DLL:{dll}")
else:
    print("NO_DLLS_FOUND")
"""
        result = subprocess.run(
            [str(python_exe), "-c", sdl2_dll_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        sdl2_dll_path = None
        sdl2_dlls = []
        
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("FOUND_DLLS:"):
                sdl2_dll_path = line[11:].strip()
                print(f"Found SDL2 DLL directory: {sdl2_dll_path}")
            elif line.startswith("DLL:"):
                dll_name = line[4:].strip()
                sdl2_dlls.append(dll_name)
                print(f"Found SDL2 DLL: {dll_name}")
        
        # If no DLLs found through script, try downloading them directly
        if not sdl2_dll_path or not sdl2_dlls:
            print("Downloading SDL2 DLLs directly...")
            try:
                # Create a directory for SDL2 DLLs
                sdl2_dir = PROJECT_ROOT / "build" / "sdl2_dlls"
                if not os.path.exists(sdl2_dir):
                    os.makedirs(sdl2_dir)
                
                # Install pysdl2-dll to get the DLLs
                subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pysdl2-dll"], check=True)
                
                # Try to copy the DLLs to our directory
                copy_dlls_cmd = f"""
import os, sys, shutil, glob
from sdl2dll import get_dll_path

dll_path = get_dll_path()
target_dir = r"{sdl2_dir}"

dll_files = glob.glob(os.path.join(dll_path, "*.dll"))
for dll in dll_files:
    print(f"Copying {{os.path.basename(dll)}}")
    shutil.copy2(dll, os.path.join(target_dir, os.path.basename(dll)))
print(f"FOUND_DLLS:{{target_dir}}")
"""
                dll_result = subprocess.run(
                    [str(python_exe), "-c", copy_dlls_cmd],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
                
                # Check if we found DLLs now
                for line in dll_result.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("FOUND_DLLS:"):
                        sdl2_dll_path = line[11:].strip()  # Fixed from .trip() to .strip()
                        print(f"Created SDL2 DLL directory: {sdl2_dll_path}")
                        # Get the DLLs in the directory
                        if os.path.exists(sdl2_dll_path):
                            for dll_file in os.listdir(sdl2_dll_path):
                                if dll_file.endswith(".dll"):
                                    sdl2_dlls.append(dll_file)
                                    print(f"Found SDL2 DLL: {dll_file}")
            except Exception as e:
                print(f"Failed to download SDL2 DLLs: {e}")
                
        # Create a better runtime hook file for SDL2
        runtime_hooks_dir = PROJECT_ROOT / "build" / "hooks"
        if not runtime_hooks_dir.exists():
            os.makedirs(runtime_hooks_dir)
            
        sdl2_hook_file = runtime_hooks_dir / "hook-sdl2.py"
        with open(sdl2_hook_file, "w") as f:
            f.write("""
# SDL2 runtime hook for PyInstaller
import os
import sys
import ctypes

# Set SDL2 DLL path BEFORE importing sdl2
if getattr(sys, 'frozen', False):
    # We're running in a PyInstaller bundle
    dll_path = sys._MEIPASS
    os.environ["PYSDL2_DLL_PATH"] = dll_path
    print(f"Set PYSDL2_DLL_PATH to {dll_path}")
    
    # Try to manually load the DLLs
    try:
        for dll_name in ["SDL2.dll", "SDL2_ttf.dll", "SDL2_image.dll", "SDL2_mixer.dll"]:
            dll_path = os.path.join(sys._MEIPASS, dll_name)
            if os.path.exists(dll_path):
                ctypes.CDLL(dll_path)
                print(f"Loaded {dll_name}")
    except Exception as e:
        print(f"Warning: Error loading SDL2 DLLs manually: {e}")

# Do not import sdl2 here - it will be imported by the application
""")

        # Add binary-specific options
        binaries = []
        
        # If we found SDL2 DLLs, add them explicitly
        if sdl2_dll_path and sdl2_dlls:
            for dll in sdl2_dlls:
                dll_path = os.path.join(sdl2_dll_path, dll)
                if os.path.exists(dll_path):
                    binaries.append((dll_path, '.'))
                    print(f"Adding SDL2 binary: {dll_path}")
        
        # Create spec file if needed
        spec_file = PROJECT_ROOT / "mars_x.spec"
        if not spec_file.exists():
            # Handle resources path correctly
            resources_path = str(resources_dir)
            resources_target = "resources"
            
            if os.name == 'nt':  # Windows
                resources_arg = f"{resources_path};{resources_target}"
            else:  # Unix/Linux/Mac
                resources_arg = f"{resources_path}:{resources_target}"
            
            # Build PyInstaller command with all necessary options
            pyinstaller_cmd = [
                str(python_exe), "-m", "PyInstaller",
                "--name=mars-x",
                "--onefile",
                # Change --windowed to --console to see output
                "--console",  # Show console window for debugging
                "--add-data", resources_arg,
                "--runtime-hook", str(sdl2_hook_file),
                "--hidden-import", "sdl2.dll",
                "--hidden-import", "sdl2.sdlttf",
                "--hidden-import", "sdl2.sdlimage",
                "--hidden-import", "sdl2.sdlmixer",
                "--hidden-import", "ctypes",  # Added ctypes which is needed
            ]
            
            # Add all binaries
            for src, dst in binaries:
                pyinstaller_cmd.extend(["--add-binary", f"{src};{dst}" if os.name == 'nt' else f"{src}:{dst}"])
            
            # Add the main script
            pyinstaller_cmd.append(str(PROJECT_ROOT / "mars_x" / "main.py"))
            
            # Run PyInstaller
            print("Running PyInstaller with these options:")
            print(" ".join(pyinstaller_cmd))
            subprocess.run(pyinstaller_cmd, check=True)
        else:
            # Use existing spec file
            subprocess.run(
                [str(python_exe), "-m", "PyInstaller", "mars_x.spec"],
                check=True
            )
        
        # Move built executable to build directory
        if os.name == 'nt':
            exe_name = "mars-x.exe"
        else:
            exe_name = "mars-x"
            
        dist_exe = PROJECT_ROOT / "dist" / exe_name
        warn_file = PROJECT_ROOT / "build" / "mars-x" / "warn-mars-x.txt"
        
        if dist_exe.exists():
            target_path = BUILD_DIR / exe_name
            shutil.copy2(dist_exe, target_path)
            
            # Calculate build telemetry data
            build_end_time = time.time()
            build_end = datetime.datetime.now()
            build_duration = build_end_time - build_start_time
            
            # Get executable size and format it
            exe_size = os.path.getsize(target_path)
            size_str = format_size(exe_size)
            
            # Create a telemetry section in the build log
            with open(build_log_path, "a") as log:
                log.write(f"Build completed at: {build_end.strftime('%Y-%m-%d %H:%M:%S')}\n")
                log.write(f"Build duration: {format_time(build_duration)}\n")
                log.write(f"Executable size: {size_str} ({exe_size:,} bytes)\n")
                log.write(f"Files processed: {build_files_count}\n")
                if warn_file.exists():
                    with open(warn_file, "r") as wf:
                        warnings = wf.read()
                    log.write("\n--- Build Warnings ---\n")
                    log.write(warnings)
            
            # Display build summary
            print("\n" + "="*50)
            print(" BUILD SUMMARY ".center(50, "="))
            print("="*50)
            print(f"Build time:      {format_time(build_duration)}")
            print(f"Executable size: {size_str}")
            print(f"Files processed: {build_files_count}")
            print(f"Build log:       {build_log_path}")
            print("="*50 + "\n")
            
            # Display simple information
            print(f"Executable built successfully: {target_path}")
            
            # Cleanup only PyInstaller's temporary artifacts, not our build dir
            if os.path.exists(PROJECT_ROOT / "dist"):
                shutil.rmtree(PROJECT_ROOT / "dist")
            
            # Don't delete the main build directory, just PyInstaller's temp files
            pyinstaller_build = PROJECT_ROOT / "build" / "mars-x"
            if os.path.exists(pyinstaller_build):
                shutil.rmtree(pyinstaller_build)
            
            # Keep the spec file for future builds
        else:
            print(f"Error: Expected executable not found at {dist_exe}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        sys.exit(1)

    print(f"\nBuild completed successfully. Executable available at: {BUILD_DIR / exe_name}")
    print("\nRun the game directly from the build directory or use 'python setup.py --build' to rebuild.")
    
    # Offer to run the executable
    if os.name == 'nt':  # Only on Windows for now
        run_exe = input("Would you like to run the executable now? (y/n): ")
        if run_exe.lower().startswith('y'):
            try:
                subprocess.Popen([str(BUILD_DIR / exe_name)])
                print("Application started.")
            except Exception as e:
                print(f"Error starting application: {e}")

# Allow direct execution of this script
if __name__ == "__main__":
    build_game()
