from fastapi import APIRouter, Header, Cookie, Form
from typing import Optional, List
from fastapi.responses import Response, HTMLResponse, PlainTextResponse

router = APIRouter(
    prefix='/product',
    tags=['products']
)

products = ['watch', 'camera', 'phone']

@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products

@router.get('/all')
def get_all_prods():
    data = " ".join(products)
    response =  Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value='test_cookie_value')
    return response

@router.get('/withheader')
def get_products(
    response: Response, 
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None)):
    if custom_header:
        response.headers['custom_response_header'] = ", ".join(custom_header)
    return {
        "data": products,
        "custom_header": custom_header,
        "my_cookie": test_cookie
        }



@router.get('/{id}', responses = {
    200: {
        "content": {
            "text/html": {
                "<div>Product</div>"
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "Product not available"
            }
        },
        "description": "Clear error message"
    }

})
def get_single_prod(id: int):
    if id > len(products):
       out = "Product not available"
       return PlainTextResponse(status_code=404,content=out, media_type='text/plain')
    else:
        product = products[id]
        out = """
        <head>
        <style>
        .product {{width: 500px;
                    height:30px;
                    border: 2px inset green;
                    background_color: lightblue;
                    text-align: center;
            }}
        </style>
        </head>
        <div class="product"> {product} </div>
        """
    return HTMLResponse(content=out, media_type='text/html')