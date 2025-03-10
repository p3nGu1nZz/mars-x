# Mars-X

A top-down 2D pixel-style space flight game built with Python, Cython, SDL2, and Vulkan.

## Requirements

- Python 3.12 or higher
- pip (Python package installer)
- Vulkan-compatible graphics hardware and drivers

## Quick Setup

Mars-X comes with a built-in setup script that handles the creation of a virtual environment and installation of all dependencies.

### Setup

1. Clone the repository:

```bash
git clone https://github.com/p3nGu1nZz/mars-x.git
cd mars-x
```

1. Run the setup script:

```bash
# Standard setup
python setup.py

# Or for development mode
python setup.py --dev
```

This will:

- Create a new virtual environment in the `.venv` directory
- Install all required dependencies from `requirements.txt`
- Build the Cython extensions
- Set up the game in development mode

### Activating the Virtual Environment

After setup is complete, activate the virtual environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

## Running the Game

With the virtual environment activated, simply run:

```bash
mars-x
```

That's it! The game will launch immediately.

## Project Structure

- `mars_x/` - Main game package
  - `engine/` - Game engine components (window management, rendering, input)
  - `game/` - Game-specific logic and entities
  - `cython_modules/` - Performance-critical components written in Cython
  - `assets/` - Game assets (graphics, sounds, etc.)

## Development

### Building Cython Modules

To rebuild the Cython modules after making changes:

```bash
# Quick rebuild of Cython modules without recreating the environment
python setup.py --build

# Alternative method (does the same thing but more verbose)
python setup.py build_ext --inplace
```

The `--build` command will rebuild all Cython modules in place, which is useful during development when you've made changes to the `.pyx` or `.pxd` files.

### Dependencies

All dependencies are listed in `requirements.txt`:

- PySDL2 - Window management and input handling
- Vulkan - Graphics rendering
- Numpy - Mathematical operations
- Cython - Performance optimization for critical components

## Controls

- W/A/S/D - Move ship
- Mouse - Aim
- Escape - Menu/Exit

## License

Apache License 2.0
