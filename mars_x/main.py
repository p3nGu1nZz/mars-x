"""
Minimal SDL2 test for Mars-X.
"""
import os
import sys
import ctypes
import logging
import time
from pathlib import Path

# Import project constants
try:
    from mars_x.utils.constants import GAME_NAME, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT
except ImportError:
    # Fallback values if constants not available
    GAME_NAME = "Mars-X Test"
    DEFAULT_SCREEN_WIDTH = 800
    DEFAULT_SCREEN_HEIGHT = 600

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
        ret = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        if ret != 0:
            error = sdl2.SDL_GetError()
            logging.error(f"Error initializing SDL2: {error.decode() if hasattr(error, 'decode') else error}")
            return 1
        
        logging.info("SDL2 initialized successfully")
        
        # Create a window
        logging.info("Creating window...")
        window = sdl2.SDL_CreateWindow(
            GAME_NAME.encode('utf-8'),  # Use the constant for game name 
            sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
            DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, sdl2.SDL_WINDOW_SHOWN
        )
        
        if not window:
            error = sdl2.SDL_GetError()
            logging.error(f"Error creating window: {error.decode() if hasattr(error, 'decode') else error}")
            sdl2.SDL_Quit()
            return 1
        
        logging.info("Window created successfully")
        
        # Create a renderer
        renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)
        if not renderer:
            error = sdl2.SDL_GetError()
            logging.error(f"Error creating renderer: {error.decode() if hasattr(error, 'decode') else error}")
            sdl2.SDL_DestroyWindow(window)
            sdl2.SDL_Quit()
            return 1
        
        logging.info("Renderer created successfully")
        
        # Keep the window open until user closes it
        logging.info("Window open - close it manually to exit")
        running = True
        event = sdl2.SDL_Event()
        
        while running:
            # Process events
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                
            # Clear and present the renderer
            sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
            sdl2.SDL_RenderClear(renderer)
            
            # Draw a simple rectangle
            sdl2.SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
            rect = sdl2.SDL_Rect(400 - 25, 300 - 25, 50, 50)
            sdl2.SDL_RenderFillRect(renderer, ctypes.byref(rect))
            
            sdl2.SDL_RenderPresent(renderer)
            
            # Small delay to reduce CPU usage
            sdl2.SDL_Delay(16)  # Roughly 60 FPS
        
        # Clean up
        sdl2.SDL_DestroyRenderer(renderer)
        sdl2.SDL_DestroyWindow(window)
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
