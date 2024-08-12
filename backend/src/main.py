from dotenv import load_dotenv, find_dotenv
from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
import requests, os

load_dotenv(find_dotenv())

app = FastAPI()

@app.middleware('http')
async def check_authorization(request: Request, call_next):
    response = requests.get(
        url=os.getenv('VALIDATE_URL'),
        headers={
            'Authorization': request.headers.get('Authorization'),
        },
    )

    if response.status_code == 200:
        request.state.login = response.json()

        return await call_next(request)

    return JSONResponse(status_code=401, content='Unauthorized')

@app.post('/')
async def hello_world():
    return 'hello world!'
