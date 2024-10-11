from typing import  List
from pydantic import BaseModel

# article for user
class ArticleforUser(BaseModel):
    title: str
    content: str
    published: bool
    class Confiq():
        orm_mode = True

class UserBase(BaseModel): 
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[ArticleforUser] = []
    class Confiq():
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int 

# user inside article display
class User(BaseModel):
    id: int 
    username: str
    class Confiq():
        orm_mode = True

class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    class Confiq():
        orm_mode = True 
