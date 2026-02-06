import sys
import types
import typing

# 1. Patch typing._eval_type
if hasattr(typing, '_eval_type'):
    original_eval_type = typing._eval_type
    def patched_eval_type(t, globalns=None, localns=None, type_params=None, **kwargs):
        try:
            return original_eval_type(t, globalns, localns, type_params)
        except TypeError:
            return original_eval_type(t, globalns, localns)
    typing._eval_type = patched_eval_type

# 2. Reconstruct annotationlib
class Format:
    VALUE = 1
    FORWARDREF = 2
    SOURCE = 3
    STRING = 4

def get_annotate_from_class_namespace(namespace):
    # This is what Pydantic calls
    ann = namespace.get('__annotations__', {})
    return lambda format=None: ann

def call_annotate_function(annotate, format, owner=None):
    try:
        if owner is not None and hasattr(owner, '__annotations__'):
            return owner.__annotations__
        return annotate(format=format)
    except Exception:
        if owner is not None:
            return getattr(owner, '__annotations__', {})
        return {}

def annotations_to_string(annotations):
    return {k: str(v) for k, v in annotations.items()}

new_ann = types.ModuleType('annotationlib')
new_ann.Format = Format
new_ann.ForwardRef = typing.ForwardRef
new_ann.get_annotate_from_class_namespace = get_annotate_from_class_namespace
new_ann.call_annotate_function = call_annotate_function
new_ann.annotations_to_string = annotations_to_string
def get_annotations(obj, *, globals=None, locals=None, eval_str=False, format=1):
    return getattr(obj, '__annotations__', {})
new_ann.get_annotations = get_annotations
sys.modules['annotationlib'] = new_ann

# Test
from pydantic import BaseModel
class User(BaseModel):
    name: str

print(f"User fields: {User.model_fields}")
print(f"SUCCESS")
