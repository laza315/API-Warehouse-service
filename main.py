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
from exceptions import StoryException
from fastapi.responses import  JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from fastapi.staticfiles import StaticFiles



app  = FastAPI()
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_post.router)
app.include_router(blog_get.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )

hosts = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = hosts,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

models.Base.metadata.create_all(engine)


app.mount('/data', StaticFiles(directory="data"), name='data')






 