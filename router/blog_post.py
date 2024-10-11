from pydantic import BaseModel
from fastapi import APIRouter, Query, Body, Path, status, Response
from typing import Optional, List, Dict


router  = APIRouter(
    prefix='/blog', 
    tags=['blog']
    )

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str 
    nb_comments: int 
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'val1'}
    image: Optional[Image] = None




@router.post('/new/{id}')
def createblog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'data': blog,
        'version': version
    }



@router.post('/new/{id}/comment/{comment_id}')
def createcomment(blog: BlogModel, 
                  id: int, 
                  comment_title: int = Query(None,
                                        title='Title of the comment',
                                        description='Some description',
                                        alias='commentTitle',
                                        depricated=True),
                  content:  str = Body(..., 
                                        min_length=10, 
                                        max_length=20),
                                        # regex='⌃[a-z\s]*S'),
                  v: Optional[List[str]] = Query([1.0, 1.1, 2.0]),
                  comment_id: int = Path(gt=5, ls=10)
                ):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'content': content,
        'version': v,
        'comment_id': comment_id
    }


def required_funcionality():
    return {"message": 'Learn'}