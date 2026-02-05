import sys
import os
import types
from enum import Enum
import typing
import logging

# Suppress logs
logging.basicConfig(level=logging.ERROR)
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# --- MONKEYPATCH FOR PYTHON 3.14 COMPATIBILITY ---
if hasattr(typing, '_eval_type'):
    original_eval_type = typing._eval_type
    def patched_eval_type(*args, **kwargs):
        kwargs.pop('prefer_fwd_module', None)
        kwargs.pop('type_params', None)
        return original_eval_type(*args, **kwargs)
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
            except NotImplementedError:
                try:
                    return annotate_func(1)
                except Exception:
                    pass
            except Exception:
                pass
            return {}
        return annotate
    annotations = namespace.get('__annotations__')
    if annotations is None:
        return None
    def annotate(format=None):
        return annotations
    return annotate

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
# --- END MONKEYPATCH ---

sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.database import engine
from app.models.user import User

def list_users():
    try:
        with Session(engine) as session:
            users = session.exec(select(User)).all()
            print(f"\nFOUND {len(users)} USERS:")
            for user in users:
                print(f"EMAIL: {user.email} | ID: {user.id}")
            print("DONE\n")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    list_users()
