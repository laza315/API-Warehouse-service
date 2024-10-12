from fastapi import FastAPI
from router import blog_post
from router import blog_get
from fastapi import Request
from db import  models
from db.database import engine
from router import user
from router import article
from router import product
from router import file
from router import dependecies
from exceptions import StoryException
from fastapi.responses import  JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from fastapi.staticfiles import StaticFiles
from templatesfolder import template
import time
from client import html
from fastapi.websockets import WebSocket


app  = FastAPI()
app.include_router(dependecies.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_post.router)
app.include_router(blog_get.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(template.router)



@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )

@app.middleware('http')
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    response.headers['duration'] = str(duration) #dodajem headers samom responsu
    return response


hosts = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = hosts,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket('/chat')
async def websocker_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


models.Base.metadata.create_all(engine)


app.mount('/data', StaticFiles(directory="data"), name='data')
app.mount('/templatesfolder/static', StaticFiles(directory='templatesfolder/static'), name='static')






 