
if __name__ == "__main__":
    import uvicorn
    print("Starting server with Python 3.12 (Standard Mode)...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
