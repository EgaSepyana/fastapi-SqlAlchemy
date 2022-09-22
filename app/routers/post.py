from turtle import mode
from .. import models , schemas , oauth2
from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy import func
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/post",
    tags=['post']
)

@router.get("/",response_model=List[schemas.PostAllOut])
# @router.get("/")
async def get_post(db: Session = Depends(get_db) , Current_user: int = Depends(oauth2.get_current_user), limit = 10, skip:int = 0, search:Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).filter(models.Post.owner_id == Current_user.id).limit(limit).offset(skip).all()

    join_query = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).filter(models.Post.owner_id == Current_user.id).limit(limit).offset(skip).all()
    return join_query

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Postout)
async def Create_post(post: schemas.Post,db: Session = Depends(get_db), Current_user: int = Depends(oauth2.get_current_user)):
    # post_data = post.dict()
    # cursor.execute(f"""
    #     INSERT INTO posts (\"title\",\"Content\",\"published\",\"rating\") 
    #     VALUES ('{post_data['title']}','{post_data['Content']}','{post_data['published']}',{post_data['rating']}) RETURNING * 
    # """)
    # new_post = cursor.fetchone()
    # con.commit()
    data = models.Post(owner_id=Current_user.id,**post.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.get("/{id}",response_model=schemas.PostAllOut)
async def get_by_id(id:int,db: Session = Depends(get_db),Current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f"""
    #     SELECT * FROM posts WHERE id = {id}
    # """)
    # Post = cursor.fetchall()
    Post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id , isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Has Not Found")

    if Post[0].owner_id != Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="No authorize to perform request action")
    return Post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(id:int,db: Session = Depends(get_db),Current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f""" 
    #     DELETE FROM posts WHERE id = {id} RETURNING *
    # """)
    
    # Deleted_post = cursor.fetchone()

    # con.commit()

    Deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if not Deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You try to delete a None Data")

    if Deleted_post.first().owner_id != Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="No authorize to perform request action")

    Deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Postout)
async def update_by_id(id:int,post:schemas.updatedPost,db: Session = Depends(get_db),Current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(f"""SELECT "title","Content","published","rating" FROM posts WHERE id ={id} """)
    
    # data = cursor.fetchone()

    # if not data:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You try to update a None Data")

    # data = json.dumps(data)
    # old_data = json.loads(data)
    # new_data = post.dict()
    
    # title = old_data['title'] if not new_data['title'] else new_data['title']
    # Content = old_data['Content'] if not new_data['Content'] else new_data['Content']
    # published = old_data['published'] if not new_data['published'] else new_data['published']
    # rating = old_data['rating'] if not new_data['rating'] else new_data['rating']

    # cursor.execute(f"""
    #         UPDATE posts SET "title" = '{title}' , "Content" = '{Content}' , "published" = {published} , "rating" = {rating} WHERE id = {id} RETURNING *
    # """)

    # updated_data = cursor.fetchone()

    # con.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    old_post = post_query.first()
    new_post = post.dict()

    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You Try To Updated None Data")

    if old_post.owner_id != Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="No authorize to perform request action")

    data = {
        "title" : old_post.title if not new_post['title'] else new_post['title'],
        "Content" : old_post.Content if not new_post['Content'  ] else new_post['Content'],
        "published" : old_post.published if not new_post['published'] else new_post['published'],
        "rating" : old_post.rating if not new_post['rating'] else new_post['rating']
    }

    post_query.update(data,synchronize_session=False)
    db.commit()
    db.refresh(old_post)

    return old_post