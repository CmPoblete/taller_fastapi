from fastapi import FastAPI

from src.apps.properties.controller import router as PropertyRouter

app = FastAPI()
app.include_router(PropertyRouter)


@app.get("/")
def hello_world():
    return {"hello": "world"}
