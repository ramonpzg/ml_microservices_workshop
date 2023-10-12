from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to the home page!"}

@app.get("/translation")
async def translation():
    return {"message": "Welcome to the translation page!"}

@app.get("/summarization")
async def summarization():
    return {"message": "Welcome to the summarization page!"}

