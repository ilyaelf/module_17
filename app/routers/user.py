from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import User
from app.schemas import CreateUser,UpdateUser
from sqlalchemy import insert,select,update,delete
from slugify import slugify

router = APIRouter(prefix='/user',tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session,Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(user_id: int,db: Annotated[Session,Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    else:
        return user


@router.post('/create')
async def create_user(create_user: CreateUser,db: Annotated[Session,Depends(get_db)]):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username,create_user.firstname),))
    db.commit()
    return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Sucsessful"
            }

@router.put('/update')
async def update_user(update_user: UpdateUser, user_id: int,db: Annotated[Session,Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    else:
        db.execute(update(User).where(User.id == user_id).values(
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age))
        db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "user updated sucsessfully"
        }

@router.delete('/delete')
async def delete_user(user_id: int,db: Annotated[Session,Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    else:
        db.execute(delete(User).where(User.id == user_id))
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "user deleted sucsessfully"
        }
