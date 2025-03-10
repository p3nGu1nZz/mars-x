# Mars-X Game

A 2D top-down space flight game built with Python and SDL2.

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

2. Run the setup script:

```bash
# Standard setup
python setup.py
```

This will:

- Create a new virtual environment in the `.venv` directory
- Install all required dependencies from `requirements.txt`
- Set up the game in development mode

### Building the Executable

To build a standalone executable:

```bash
python setup.py --build
```

This will:

- Ensure the virtual environment is set up correctly
- Compile any Cython modules
- Build a standalone executable in the `build` directory
- No manual activation of the environment is required

## Running the Game

After building, you can simply run the executable from the `build` directory:

```bash
# Windows
build\mars-x.exe
```

- simple wasd controls and escape accesses the settings.
- Window can be closed by clicking the close button
- The example displays a red square in a black window it! The game will launch immediately.

## License

This dataset is licensed under the Apache License 2.0.

## Citations

Please use the following BibTeX entry to cite this dataset:

```bibtex
@software{Mars-X,
  author = {K. Rawson},
  title = {A simple 2d space game engine writen in python, cython, vulkan and sdl2},
  year = {2025},
  howpublished = {\url{https://github.com/p3nGu1nZz/mars-x}},
  note = {Accessed: 2025-03-11}
}
```

## Acknowledgements

Special thanks to our contributors:

- **p3nGu1nZz** - Lead Engineer

## Contact

For questions or support, please contact us at:

- **Email**: <rawsonkara@gmail.com>
- **Discord**: [Join our Discord](https://discord.gg/2xpqjDUkHD)
