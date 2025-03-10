import os
import sys
import subprocess
import sdl2
import sdl2.ext

from mars_x.engine.window import Window
from mars_x.engine.renderer import VulkanRenderer
from mars_x.engine.input import InputManager
from mars_x.game.game_world import GameWorld

def find_project_root():
    """Find the project root directory (where .venv is located)"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up to find project root (where .venv should be)
    while current_dir and os.path.basename(current_dir) != "mars-x":
        parent = os.path.dirname(current_dir)
        if parent == current_dir:  # Reached filesystem root without finding project
            return None
        current_dir = parent
    return current_dir

def ensure_venv():
    """Ensure we're running in the virtual environment, restart if not"""
    # Check if we're already in a virtual environment
    if sys.prefix != sys.base_prefix:
        return  # Already in a venv
    
    project_root = find_project_root()
    if not project_root:
        return  # Can't find project root, continue anyway
    
    venv_dir = os.path.join(project_root, '.venv')
    if not os.path.isdir(venv_dir):
        print("Warning: Virtual environment not found. Run 'python setup.py' first.")
        return
    
    # Determine the path to the Python executable in the virtual environment
    if sys.platform == 'win32':
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_path = os.path.join(venv_dir, "bin", "python")
    
    if os.path.exists(python_path):
        print(f"Activating virtual environment in {venv_dir}...")
        # Re-execute the current script with the venv python
        args = [python_path, "-m", "mars_x.main"] + sys.argv[1:]
        os.execv(python_path, args)
    else:
        print(f"Warning: Virtual environment Python not found at {python_path}")

def main():
    # Initialize SDL systems
    sdl2.ext.init()
    
    # Create window, renderer and input manager
    window = Window("Mars-X", 1280, 720)
    renderer = VulkanRenderer(window)
    input_manager = InputManager()
    
    # Create game world
    game_world = GameWorld(renderer)
    
    # Main game loop
    running = True
    while running:
        # Process input
        for event in input_manager.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
            
            # Handle other events
            game_world.process_input(event)
        
        # Update game state
        game_world.update()
        
        # Render
        renderer.begin_frame()
        game_world.render()
        renderer.end_frame()
    
    # Clean up
    renderer.cleanup()
    window.cleanup()
    sdl2.ext.quit()

if __name__ == "__main__":
    ensure_venv()  # Check and activate venv if needed
    main()
