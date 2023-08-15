from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import database
from app import schemas
from app import models
from app import oauth2
from typing import List,Optional

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/",status_code=status.HTTP_202_ACCEPTED,response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #This normal sql query
    #cursor.execute(""" SELECT * FROM posts """)
    #posts=cursor.fetchall()


    #This is ORM
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createposts(post:schemas.PostCreate,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    #This is simple sql query
    '''cursor.execute("""INSERT INTO posts (title,content,published,created_at) VALUES(%s,%s,%s,'NOW()') RETURNING * """,(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()'''

    #This is using orm
    new_post=models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#title , str,content str


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    '''cursor.execute("""SELECT * from posts WHERE id = %s """,(str(id)))
    post=cursor.fetchone()'''

    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    #deleteing post
    '''cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id)))
    deleted_post=cursor.fetchone()
    conn.commit()'''

    deleted_post_query=db.query(models.Post).filter(models.Post.id==id)
    deleted_post=deleted_post_query.first()
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not exist")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    '''cursor.execute("""UPDATE posts SET title = %s, content = %s , published = %s , created_at= 'NOW()' WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()'''
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not exist") 
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()