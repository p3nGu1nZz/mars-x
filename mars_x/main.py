"""
Main entry point for Mars-X game.
"""
import os
import sys
import logging
from pathlib import Path

# Import engine components
from mars_x.engine.window import Window
from mars_x.engine.input import InputManager
from mars_x.game.game_world import GameWorld

# Import project constants - direct import with no fallback
from mars_x.utils.constants import (
    GAME_NAME, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT
)

def setup_logger():
    """Set up logging to write to a file next to the executable."""
    # Determine the log file location (next to the executable)
    if getattr(sys, 'frozen', False):
        # Running as bundled exe
        base_path = Path(sys.executable).parent
    else:
        # Running in development
        base_path = Path(__file__).resolve().parent.parent
        
    log_file = base_path / "mars-x.log"
    
    # Configure logging
    logging.basicConfig(
        filename=str(log_file),
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add console handler to print logs to stdout as well
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    return log_file

def main():
    """Main function to test SDL2 initialization."""
    log_file = setup_logger()
    
    logging.info(f"Starting {GAME_NAME} test... Log file: {log_file}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current directory: {os.getcwd()}")

    # Print environment variables
    logging.info(f"PYSDL2_DLL_PATH: {os.environ.get('PYSDL2_DLL_PATH', 'not set')}")
    
    try:
        # Try to import and initialize SDL2
        import sdl2
        import sdl2.ext
        
        logging.info("SDL2 module imported successfully")
        logging.info(f"SDL2 version: {sdl2.SDL_MAJOR_VERSION}.{sdl2.SDL_MINOR_VERSION}.{sdl2.SDL_PATCHLEVEL}")
        
        # Initialize SDL2
        logging.info("Initializing SDL2...")
        ret = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_EVENTS)
        if ret != 0:
            error = sdl2.SDL_GetError()
            logging.error(f"Error initializing SDL2: {error.decode() if hasattr(error, 'decode') else error}")
            return 1
        
        logging.info("SDL2 initialized successfully")
        
        # Create window using our Window class
        logging.info("Creating window...")
        window = Window(GAME_NAME, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        
        # Get the SDL window handle for renderer creation
        sdl_window = window.get_sdl_window()
        
        # Create a renderer
        renderer = sdl2.SDL_CreateRenderer(sdl_window, -1, sdl2.SDL_RENDERER_ACCELERATED)
        if not renderer:
            error = sdl2.SDL_GetError()
            logging.error(f"Error creating renderer: {error.decode() if hasattr(error, 'decode') else error}")
            window.cleanup()
            sdl2.SDL_Quit()
            return 1
        
        logging.info("Renderer created successfully")
        
        # Create input manager
        input_manager = InputManager()
        
        # Create game world with our renderer
        game_world = GameWorld(renderer)
        
        # Main game loop variables
        running = True
        
        while running:
            # Process events with our input manager
            if input_manager.process_input():
                running = False
                break
            
            # Handle fullscreen toggle with F11 using Window class
            if input_manager.is_action_just_pressed('toggle_fullscreen'):
                is_fullscreen = window.toggle_fullscreen()
                logging.info(f"Fullscreen toggled to: {is_fullscreen}")
            
            # Update game world (handles all entity updates including player)
            game_world.update(input_manager, 1/60.0)
            
            # Clear the renderer
            sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
            sdl2.SDL_RenderClear(renderer)
            
            # Let game world render all entities
            game_world.render()
            
            sdl2.SDL_RenderPresent(renderer)
            
            # Small delay to reduce CPU usage
            sdl2.SDL_Delay(16)  # Roughly 60 FPS
        
        # Clean up
        sdl2.SDL_DestroyRenderer(renderer)
        window.cleanup()  # Use window class cleanup instead of direct SDL2 call
        sdl2.SDL_Quit()
        logging.info("SDL2 quit successfully")
        
        return 0
    
    except ImportError as e:
        logging.error(f"Error importing SDL2: {e}")
        return 1
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
