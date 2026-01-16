import sys
import types
from enum import Enum
import typing

# --- MONKEYPATCH FOR PYTHON 3.14 COMPATIBILITY ---
# Patch typing._eval_type which Pydantic uses with incompatible arguments in 3.14
if hasattr(typing, '_eval_type'):
    print("PATCHING: Wrapping typing._eval_type for compatibility")
    original_eval_type = typing._eval_type
    def patched_eval_type(*args, **kwargs):
        # Remove arguments that 3.14's _eval_type doesn't accept but Pydantic sends
        kwargs.pop('prefer_fwd_module', None)
        kwargs.pop('type_params', None) # Pydantic sends this too?
        return original_eval_type(*args, **kwargs)
    typing._eval_type = patched_eval_type

# Pydantic tries to import these from `annotationlib` in Python 3.14,
# but the alpha version installed might not match what Pydantic expects.

class Format(Enum):
    VALUE = 1
    FORWARDREF = 2
    SOURCE = 3

def get_annotate_from_class_namespace(namespace):
    # PEP 649 / Python 3.14: Annotations are in a function called __annotate__
    if '__annotate__' in namespace:
        annotate_func = namespace['__annotate__']
        def annotate(format=None):
            # Verify if it's callable and call it
            try:
                if callable(annotate_func):
                    return annotate_func(format)
            except NotImplementedError:
                # Python 3.14 alpha might fail on SOURCE (3), try VALUE (1)
                try:
                    return annotate_func(1)
                except Exception:
                    pass
            except Exception as e:
                import traceback
                print(f"Error calling __annotate__ with format={format}: {e}")
                traceback.print_exc()
            return {}
        return annotate

    # Legacy / Stringified
    annotations = namespace.get('__annotations__')
    if annotations is None:
        return None
        
    def annotate(format=None):
        return annotations
        
    return annotate

def call_annotate_function(annotate, format):
    return annotate(format=format)

# Check if annotationlib exists
try:
    import annotationlib
except ImportError:
    # Create dummy module if it doesn't exist
    annotationlib = types.ModuleType('annotationlib')
    sys.modules['annotationlib'] = annotationlib

# Patch the missing attributes
if not hasattr(annotationlib, 'Format'):
    annotationlib.Format = Format
if not hasattr(annotationlib, 'get_annotate_from_class_namespace'):
    annotationlib.get_annotate_from_class_namespace = get_annotate_from_class_namespace
if not hasattr(annotationlib, 'call_annotate_function'):
    annotationlib.call_annotate_function = call_annotate_function

# ----------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    print("Starting server with Python 3.14 compatibility patch...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
