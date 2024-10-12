from fastapi import APIRouter, Depends
from typing import  Optional
from router.blog_post import required_funcionality
from enum import Enum

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('type/{type}')
def get_blog_type(type: BlogType):
    return {'message': f'Blog type {type}'}



@router.get('/all', summary='Retrieve all blogs', response_description='The list of posts')
def get_blogs(page=1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_funcionality)):
    return {'message': f'All {page_size} blogs on {page}', 
            'req': req_parameter}