from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import User
from db.hash import Hash
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


def create_user(db: Session, request: UserBase):
    new_user = User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_username(db: Session, username: str):
    user =  db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with {username} username, not found")
    return user

def update_user(db: Session, id: int, request: UserBase):
    try:
        user = db.query(User).filter(User.id == id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.update({
        User.username: request.username,
        User.email: request.email,
        User.password: Hash.bcrypt(request.password)
        })
        db.commit()
        return {'message': 'User has been updated successfully'}
    except Exception as e:
       logger.error(f"Error updating user: {e}")
    raise HTTPException(status_code=500, detail="Internal Server Error")
   
def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id {id} not found')
    db.delete(user)
    db.commit()
    return 'Deleted'
