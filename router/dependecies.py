from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.param_functions import Depends
from logs import log


"""
Dependecy injection 

It can be applied or on APP(all routers) or on just specific router. 
Cannot be on both - also known as Global dependecy

"""

router = APIRouter(
    prefix='/dependecies',
    tags=['dependecy'],
    dependencies=[Depends(log)]
)

def convert_params(request: Request, separator: str):
    query = []
    for key,value in request.query_params.items():
        query.append(f"{key} {separator} {value}")
    return query

def convert_headers(request: Request, separator: str, query = Depends(convert_params)):
    """
    Zelimo da konvertujemo sve sto dolazi u headersu iz requesta
    """
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} {separator} {value}")
    return {
        'headers': out_headers,
        'query': query
    }

@router.get('')
def get_items(additional_query: str, separator: str = '--', headers = Depends(convert_headers)):
    return {
        'items': ['a', 'b', 'c'],
        'headers': headers
    }

class Account:

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    
@router.post('/user')
def create_user(name: str, 
                email: str, 
                password: str, 
                account: Account = Depends()): #ako ne prosleidmo nista u depends, 
                                          # pozvace prvobitno prosledjen type(Accounts)
    return {
        'name': account.name,
        'email': account.email
    }

