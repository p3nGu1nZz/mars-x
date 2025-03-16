# Cython modules runtime hook for PyInstaller
import os
import sys
import importlib.util
import importlib.machinery
import types

def ensure_directory_exists(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def create_init_file(directory):
    """Create an empty __init__.py file in the directory if it doesn't exist."""
    init_file = os.path.join(directory, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Auto-generated __init__.py file for PyInstaller\n')
    return init_file

def load_binary_module(name, path):
    """Load a binary module (.pyd/.so) directly."""
    try:
        loader = importlib.machinery.ExtensionFileLoader(name, path)
        spec = importlib.util.spec_from_file_location(name, path, loader=loader)
        if spec:
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            print(f"Successfully loaded {name} from {path}")
            return module
    except Exception as e:
        print(f"Error loading {name} from {path}: {e}")
    return None

# This runs when the frozen application starts
if getattr(sys, 'frozen', False):
    # We're running in a PyInstaller bundle
    root_path = sys._MEIPASS
    
    # Set up the package structure
    cython_modules_path = os.path.join(root_path, "mars_x", "cython_modules")
    if os.path.exists(cython_modules_path):
        print(f"Found Cython modules directory: {cython_modules_path}")
        
        # Make sure mars_x package exists
        if 'mars_x' not in sys.modules:
            mars_x_module = types.ModuleType('mars_x')
            sys.modules['mars_x'] = mars_x_module
            mars_x_module.__path__ = [os.path.join(root_path, 'mars_x')]
            # Create package directory
            ensure_directory_exists(os.path.join(root_path, 'mars_x'))
            # Create __init__.py
            create_init_file(os.path.join(root_path, 'mars_x'))
        
        # Make sure mars_x.cython_modules package exists
        if 'mars_x.cython_modules' not in sys.modules:
            cython_module = types.ModuleType('mars_x.cython_modules')
            sys.modules['mars_x.cython_modules'] = cython_module
            cython_module.__path__ = [cython_modules_path]
            # Create __init__.py
            init_file = create_init_file(cython_modules_path)
        
        # Load all the compiled modules
        module_files = [
            ('vector', os.path.join(cython_modules_path, 'vector.cp312-win_amd64.pyd')),
            ('rigidbody', os.path.join(cython_modules_path, 'rigidbody.cp312-win_amd64.pyd')),
            ('collision', os.path.join(cython_modules_path, 'collision.cp312-win_amd64.pyd')),
            ('matrix', os.path.join(cython_modules_path, 'matrix.cp312-win_amd64.pyd')),
            ('quaternion', os.path.join(cython_modules_path, 'quaternion.cp312-win_amd64.pyd'))
        ]
        
        # Ensure all extensions are considered (.pyd for Windows, .so for Unix)
        extensions = ['.pyd', '.so']
        
        # Try to load all modules
        for module_name, module_path in module_files:
            # Try with the specific path
            if os.path.exists(module_path):
                full_name = f'mars_x.cython_modules.{module_name}'
                load_binary_module(full_name, module_path)
            else:
                # Try with different extensions
                for ext in extensions:
                    generic_path = os.path.join(cython_modules_path, f'{module_name}{ext}')
                    if os.path.exists(generic_path):
                        full_name = f'mars_x.cython_modules.{module_name}'
                        load_binary_module(full_name, generic_path)
                        break
