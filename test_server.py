"""
Minimal test server to diagnose the issue
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="OpenHealth Test")

@app.get("/")
def root():
    return {"status": "test server working"}

@app.get("/health")
def health():
    return {"status": "healthy", "test": True}

if __name__ == "__main__":
    import uvicorn
    print("Starting minimal test server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
