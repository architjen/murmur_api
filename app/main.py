from fastapi import FastAPI

app = FastAPI(title="Faster Whisperers 🐍")

@app.get('/')
def hello():
    return {"msg": "Hello Whisperers!"}
