from fastapi import FastAPI,HTTPException,Depends,status
from  pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title:str
    content:str
    user_id:int

class userBase(BaseModel):
    username:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]


@app.post("/users/",status_code=status.HTTP_201_CREATED)

async def create_user(user:userBase,db: db_dependency):

        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()

@app.get("/users/{username}",status_code=status.HTTP_200_OK)

async def read_user(username: str, db:db_dependency):
    user = db.query(models.User).filter(models.User.username==username).first()

    if user is None:
          raise HTTPException(status_code=404,detail="User not found")
    
    return user

@app.post("/users/post/{username}",status_code=status.HTTP_200_OK)

async def create_post(username: str, post:PostBase,db:db_dependency):
     db_post = models.post(**post.dict())
     db.add(db_post)
     db.commit()

@app.get("/posts/{user_id}",status_code=status.HTTP_200_OK)

def get_post(user_id:int,db:db_dependency):
    post = db.query(models.post).filter(models.post.user_id==user_id).first()

    if post is None:
         raise HTTPException(status_code=404,detail="Post not found")
    return post

@app.delete("/posts/delete/{post_id}",status_code=status.HTTP_200_OK)

def delete_post(post_id:int,db:db_dependency):
     post = db.query(models.post).filter(models.post.id==post_id).first()
     if post is None:
         raise HTTPException(status_code=404,detail="Post not found")
     db.delete(post)
     db.commit()
