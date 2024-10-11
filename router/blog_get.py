from fastapi import APIRouter, Depends
from typing import  Optional
from router.blog_post import required_funcionality

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.get('/all', summary='Retrieve all blogs', response_description='The list of posts')
def get_blogs(page=1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_funcionality)):
    return {'message': f'All {page_size} blogs on {page}', 
            'req': req_parameter}