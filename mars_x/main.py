"""
Main entry point for Mars-X game.
"""
import os
import sys
import ctypes
import logging
import time
from pathlib import Path
import sdl2

# Import engine components
from mars_x.engine.window import Window
from mars_x.engine.renderer import VulkanRenderer
from mars_x.engine.input import InputManager
from mars_x.game.game_world import GameWorld

# Import project constants
try:
    from mars_x.utils.constants import (
        GAME_NAME, GAME_VERSION, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT
    )
except ImportError:
    # Fallback values if constants not available
    GAME_NAME = "Mars-X Test"
    GAME_VERSION = "0.1.0"
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

class Game:
    """Main game class that coordinates all engine components."""
    def __init__(self):
        self.running = False
        self.window = None
        self.renderer = None
        self.input_manager = None
        self.game_world = None
        
        # Frame rate control
        self.target_fps = 60
        self.frame_delay = 1000 / self.target_fps  # ms per frame
        self.last_frame_time = 0
        self.delta_time = 0  # Time between frames in seconds
    
    def initialize(self):
        """Initialize the game and all engine components."""
        logging.info(f"Initializing {GAME_NAME} {GAME_VERSION}...")
        
        # Initialize SDL2
        logging.info("Initializing SDL2...")
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_EVENTS) != 0:
            error = sdl2.SDL_GetError()
            logging.error(f"Error initializing SDL2: {error.decode() if hasattr(error, 'decode') else error}")
            return False
        
        logging.info("SDL2 initialized successfully")
        
        # Create engine components
        try:
            # Create window
            logging.info("Creating window...")
            self.window = Window(GAME_NAME, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
            
            # Create renderer
            logging.info("Creating renderer...")
            self.renderer = VulkanRenderer(self.window)
            
            # Create input manager
            logging.info("Creating input manager...")
            self.input_manager = InputManager()
            
            # Create game world
            logging.info("Creating game world...")
            self.game_world = GameWorld(self.renderer)
            
            logging.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logging.exception(f"Error during initialization: {e}")
            self.cleanup()
            return False
    
    def run(self):
        """Run the main game loop."""
        self.running = True
        logging.info(f"Entering main game loop (target FPS: {self.target_fps})")
        
        # Initialize timing
        last_frame_time = sdl2.SDL_GetTicks()
        
        try:
            # Main game loop
            while self.running:
                # Calculate frame timing
                current_time = sdl2.SDL_GetTicks()
                self.delta_time = (current_time - last_frame_time) / 1000.0  # Convert to seconds
                
                # Process input - get input state for this frame
                if self.input_manager.process_input():
                    self.running = False
                    break
                
                # Handle window fullscreen toggle
                if self.input_manager.is_action_just_pressed('toggle_fullscreen'):
                    self.window.toggle_fullscreen()
                
                # Update game state with current input and delta time
                self.game_world.update(self.input_manager, self.delta_time)
                
                # Render the current frame
                self.renderer.begin_frame()
                self.game_world.render()
                self.renderer.end_frame()
                
                # Calculate how long this frame took
                frame_time = sdl2.SDL_GetTicks() - current_time
                
                # If we're running faster than our target FPS, delay to maintain consistent framerate
                if frame_time < self.frame_delay:
                    sdl2.SDL_Delay(int(self.frame_delay - frame_time))
                
                # Update last frame time for next iteration
                last_frame_time = current_time
                
                # Display FPS every second (for debug/performance monitoring)
                if current_time % 1000 < 20:  # Roughly every second
                    current_fps = 1.0 / self.delta_time if self.delta_time > 0 else 0
                    logging.debug(f"FPS: {current_fps:.1f}")
                
        except Exception as e:
            logging.exception(f"Error in game loop: {e}")
        
        logging.info("Exiting main game loop")
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources and shut down."""
        logging.info("Cleaning up resources...")
        
        # Clean up game components in reverse order of creation
        if self.game_world:
            logging.info("Cleaning up game world...")
            # No cleanup method yet, but we could add one
            self.game_world = None
        
        if self.input_manager:
            logging.info("Cleaning up input manager...")
            # No cleanup method needed for input manager
            self.input_manager = None
        
        if self.renderer:
            logging.info("Cleaning up renderer...")
            self.renderer.cleanup()
            self.renderer = None
        
        if self.window:
            logging.info("Cleaning up window...")
            self.window.cleanup()
            self.window = None
        
        # Quit SDL
        logging.info("Quitting SDL2...")
        sdl2.SDL_Quit()
        
        logging.info("Cleanup complete")
    
def main():
    """Main function that serves as the entry point."""
    log_file = setup_logger()
    
    logging.info(f"Starting {GAME_NAME} {GAME_VERSION}")
    logging.info(f"Log file: {log_file}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current directory: {os.getcwd()}")
    
    # Print environment variables
    logging.info(f"PYSDL2_DLL_PATH: {os.environ.get('PYSDL2_DLL_PATH', 'not set')}")
    
    try:
        # Create and run the game
        game = Game()
        if game.initialize():
            game.run()
            return 0
        else:
            return 1
    
    except ImportError as e:
        logging.error(f"Error importing required modules: {e}")
        return 1
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
