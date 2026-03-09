from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

port = int(os.environ.get("PORT", 8000))

uvicorn.run(app, host="0.0.0.0", port=port)
