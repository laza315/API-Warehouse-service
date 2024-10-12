from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from schemas import ProductBase
from logs import log
from fastapi import BackgroundTasks

router =  APIRouter(
    prefix="/templates",
    tags=['templates']
)

templates  = Jinja2Templates(directory='templatesfolder')

@router.post('/product/{id}', response_class=HTMLResponse)
def get_product(id: str, product: ProductBase, 
                request: Request, 
                bt: BackgroundTasks):
    # this will be logged after response is sent, as a Background task
    bt.add_task(log_template_call, f'Template read for product with id {id}')
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id": id,
            "title": product.title,
            "description": product.description,
            "price": product.price
        }
    )

def log_template_call(message: str):
    log("MyApi", message)