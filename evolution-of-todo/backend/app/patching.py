import sys
import types
from enum import Enum
import typing

# --- MONKEYPATCH FOR PYTHON 3.14 COMPATIBILITY ---
if hasattr(typing, '_eval_type'):
    original_eval_type = typing._eval_type
    def patched_eval_type(t, globalns=None, localns=None, type_params=None, **kwargs):
        # Python 3.14 _eval_type signature: (t, / , globalns=None, localns=None, *, ...)
        # Pydantic 2.12 sends: (t, globalns, localns, type_params=..., prefer_fwd_module=...)
        # We need to strip the extra keyword arguments that 3.14 doesn't like.
        try:
            return original_eval_type(t, globalns, localns, **{})
        except TypeError:
            # Fallback for even older Pydantic or different 3.14 alpha builds
            return original_eval_type(t, globalns, localns)
    typing._eval_type = patched_eval_type

class Format(Enum):
    VALUE = 1
    FORWARDREF = 2
    SOURCE = 3

def get_annotate_from_class_namespace(namespace):
    if '__annotate__' in namespace:
        annotate_func = namespace['__annotate__']
        def annotate(format=None):
            try:
                if callable(annotate_func):
                    return annotate_func(format)
            except Exception:
                try:
                    return annotate_func(1)
                except Exception:
                    pass
            return {}
        return annotate
    annotations = namespace.get('__annotations__')
    return (lambda format=None: annotations) if annotations is not None else None

def call_annotate_function(annotate, format):
    return annotate(format=format)

try:
    import annotationlib
except ImportError:
    annotationlib = types.ModuleType('annotationlib')
    sys.modules['annotationlib'] = annotationlib

if not hasattr(annotationlib, 'Format'):
    annotationlib.Format = Format
if not hasattr(annotationlib, 'get_annotate_from_class_namespace'):
    annotationlib.get_annotate_from_class_namespace = get_annotate_from_class_namespace
if not hasattr(annotationlib, 'call_annotate_function'):
    annotationlib.call_annotate_function = call_annotate_function
# ---------------------------------------------------
