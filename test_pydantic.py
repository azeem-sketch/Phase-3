import sys
import types
import typing
import enum

print("DEBUG: Diagnostic script start")

# 1. Patch typing._eval_type
if hasattr(typing, '_eval_type'):
    print("DEBUG: Patching typing._eval_type")
    original_eval_type = typing._eval_type
    def patched_eval_type(t, globalns=None, localns=None, type_params=None, **kwargs):
        try:
            return original_eval_type(t, globalns, localns, type_params)
        except TypeError:
            return original_eval_type(t, globalns, localns)
    typing._eval_type = patched_eval_type

# 2. Reconstruct annotationlib
class Format(enum.Enum):
    VALUE = 1
    FORWARDREF = 2
    SOURCE = 3

def get_annotate_from_class_namespace(namespace):
    ann = namespace.get('__annotations__', {})
    return lambda format=None: ann

def call_annotate_function(annotate, format):
    return annotate(format=format)

new_ann = types.ModuleType('annotationlib')
new_ann.Format = Format
new_ann.ForwardRef = typing.ForwardRef
new_ann.get_annotate_from_class_namespace = get_annotate_from_class_namespace
new_ann.call_annotate_function = call_annotate_function
def get_annotations(obj, *, globals=None, locals=None, eval_str=False, format=Format.VALUE):
    return getattr(obj, '__annotations__', {})
new_ann.get_annotations = get_annotations
sys.modules['annotationlib'] = new_ann

print("DEBUG: Patching complete. Attempting pydantic import...")

try:
    import pydantic
    print(f"DEBUG: pydantic imported! Version: {pydantic.VERSION}")
    print(f"DEBUG: BaseModel: {pydantic.BaseModel}")
except Exception as e:
    print(f"DEBUG: pydantic import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from pydantic import BaseModel
    print("DEBUG: Successfully imported BaseModel from pydantic")
except ImportError as e:
    print(f"DEBUG: Failed to import BaseModel from pydantic: {e}")
    import pydantic
    print(f"DEBUG: Dir(pydantic): {dir(pydantic)}")
