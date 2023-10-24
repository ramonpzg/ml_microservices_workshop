
from fastapi import FastAPI
import pyjokes

app = FastAPI()

@app.get("/joke")
def get_joke():
    joke = pyjokes.get_joke()
    return {"joke": joke}
