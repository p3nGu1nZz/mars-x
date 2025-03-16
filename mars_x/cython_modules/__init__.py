"""
Mars-X cython modules initialization.
This file ensures proper importing of compiled Cython modules.
"""

# Don't import Cython modules at top level - this causes issues with PyInstaller
# Instead, define a function to import them conditionally when needed
def get_modules():
    try:
        from .vector import Vector2, Vector3, Vector4
        from .rigidbody import Entity, update_positions, apply_force, apply_torque
        from .collision import detect_collision
        from .matrix import Matrix4
        from .quaternion import Quaternion
        
        print("Successfully loaded Cython modules.")
        return {
            'Vector2': Vector2,
            'Vector3': Vector3,
            'Vector4': Vector4,
            'Entity': Entity,
            'update_positions': update_positions,
            'apply_force': apply_force,
            'apply_torque': apply_torque,
            'detect_collision': detect_collision,
            'Matrix4': Matrix4,
            'Quaternion': Quaternion
        }
    except ImportError as e:
        print(f"Error importing Cython modules: {e}")
        raise ImportError(
            "Failed to load compiled Cython modules. Make sure they are properly compiled."
        ) from e

# Create module-level variables for direct imports
# These will be populated when the modules are first accessed
Vector2 = None
Vector3 = None
Vector4 = None
Entity = None
update_positions = None
apply_force = None
apply_torque = None
detect_collision = None
Matrix4 = None
Quaternion = None

# Import the modules immediately if not being analyzed by PyInstaller
import sys
if not getattr(sys, 'frozen', False):
    try:
        modules = get_modules()
        for name, obj in modules.items():
            globals()[name] = obj
    except ImportError:
        pass
