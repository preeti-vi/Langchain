import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from backend_code import ask_ai_2_queries_in_loop
import logging


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.ERROR)

@app.get("/", response_class=HTMLResponse)
async def get_form():
    logging.debug("in get_form")
    with open("static/index.html", "r") as file:
        return file.read()

@app.get("/submit")
async def handle_submit(user_input: str):   # UserInput):
    response = ask_ai_2_queries_in_loop(user_input)

    # Return the response as JSON
    return {"response_list": response}

if __name__ == "main":
    uvicorn.run(app, "127.0.0.1", 8000, reload=false)