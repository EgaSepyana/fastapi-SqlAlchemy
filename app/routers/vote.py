from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session

from app import models
from ..database import get_db
from .. import oauth2 , schemas
router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/")
async def create_vote(vote:schemas.vote, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    get_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    founded_vote = vote_query.first()
    if vote.dir:
        if not get_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your try to Vote None Data")
        if founded_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="You Already Vote this Post")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"massage" : "Vote Succesfull to send"}
    # print(vote.post_id)
    # print(vote.dir)
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Vote does Not Exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"massege" : "Vote Succesful To Delete"}