from fastapi import FastAPI
import uvicorn
import sys

# Minimal patch
import typing
if hasattr(typing, '_eval_type'):
    original_eval_type = typing._eval_type
    def patched_eval_type(t, globalns=None, localns=None, *args, **kwargs):
        return original_eval_type(t, globalns, localns)
    typing._eval_type = patched_eval_type

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    print("Starting minimal server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
