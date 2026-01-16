import sys
import uvicorn
import traceback

# --- MONKEYPATCH FOR PYTHON 3.14 ALPHA ---
try:
    import annotationlib
    if not hasattr(annotationlib, 'get_annotate_from_class_namespace'):
        print("PATCHING: Adding dummy get_annotate_from_class_namespace to annotationlib")
        
        def get_annotate_from_class_namespace(*args, **kwargs):
             # Log args to see what's happening
             print(f"DEBUG PATCH: called with args={args} kwargs={kwargs}")
             # Return a dummy callable that returns empty dict
             return lambda: {}
             
        annotationlib.get_annotate_from_class_namespace = get_annotate_from_class_namespace
except ImportError:
    pass
# -----------------------------------------

if __name__ == "__main__":
    # Import app after patching
    try:
        from app.main import app
        print("Starting server with Python 3.14 compat patch...")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception:
        traceback.print_exc()
